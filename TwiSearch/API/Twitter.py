from flask import Flask, request
from flask_cors import CORS
import mysql.connector
import json
import time
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import importlib
from sklearn.metrics.pairwise import cosine_similarity
import urllib.parse
from celery import Celery

tweets = importlib.import_module("tweet_analysis")

mydb = mysql.connector.connect(
    host="placeholder",
    user="placeholder",
    password="placeholder",
    database="placeholder"
)

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672/'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

CORS(app)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/search', methods=['GET'])
def search():
    try:
        #need to exclude symbols and numbers
        args = request.args
        query = args["query"]
        print(query)
        if query is None or len(query) == 0:
            return "Error: query can't be empty", 400
        return get_results(query)

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return "An error occurred while processing the request", 500


@app.route('/results')
def get_results(query=None):
    try:

        # check if query has already been searched before
        sql = "SELECT EXISTS(SELECT * from saved_result_queries WHERE search_query = %s)"
        val = ([query])
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(sql, val)
        mycursor.close()
        exists = mycursor.fetchone()[0]
        print(exists)
    except mysql.connector.Error as err:
        # Handle MySQL errors here
        print("MySQL error: ", err)
        return "An error occurred while executing the SQL query", 500
    except Exception as e:
        # Handle any other unhandled exceptions here
        print("An error occurred: ", str(e))
        return "An error occurred while processing the request", 500

    # if query already has stored results then return them
    if exists == 1:
        try:
            mycursor = mydb.cursor(buffered=True)
            table_name = "result_" + query.replace(" ", "_").lower()
            sql = "SELECT * FROM {table_name}".format(table_name=table_name)
            mycursor.execute(sql)
            data = mycursor.fetchall()
            final_results = [dict(
                zip(("id", "url", "title", "description", "date", "frequency", "cosine_similarity", "score", "ranking"),
                    x))
                for x in data]
            final_results = sorted(final_results, key=lambda x: x["ranking"])
            mycursor.close()
            return final_results

        except mysql.connector.Error as err:
            # Handle MySQL errors here
            print("MySQL error: ", err)
            return "An error occurred while executing the SQL query", 500

        except Exception as e:
            # Handle any other unhandled exceptions here
            print("An error occurred: ", str(e))
            return "An error occurred while processing the request", 500

    # otherwise need to find relevant results
    else:

        mycursor = mydb.cursor(buffered=True)
        url_ids = []

        query_words = query.split()
        for word in query_words:
            sql = "SELECT url_ids FROM inverted_index WHERE word = %s"
            val = (word,)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()

            if result is not None:
                url_ids_str = result[0]
                url_ids = url_ids_str.split(',')
        url_ids = list(dict.fromkeys(url_ids))
        mycursor.close()

        if len(url_ids) == 0:
            return "No matching documents found", 404

        mycursor = mydb.cursor(buffered=True)
        in_params = ','.join(['%s'] * len(url_ids))
        sql = "SELECT url_id,words,date FROM text_words WHERE url_id IN (%s)" % in_params
        mycursor.execute(sql, url_ids)
        data = mycursor.fetchall()

        mycursor.close()
        if len(data) == 0:
            # handle empty data list
            return "No matching documents found",404
        ids = []
        data_dict = {}
        for i in data:
            ids.append(i[0])
            data_dict[i[0]] = {"words": i[1], "date": i[2]}

        terms_list = []

        for key, value in data_dict.items():
            doc = json.loads(value['words'])
            terms_list.append(" ".join([term for term in doc.keys() for i in range(doc[term])]))

        # create TF-IDF vectors for terms list and query
        vectorizer = TfidfVectorizer()

        tfidf = vectorizer.fit_transform(terms_list)

        query_tfidf = vectorizer.transform([query])

        # calculate cosine similarities for each document(webpage) in relation to the query
        cosine_similarities = cosine_similarity(tfidf, query_tfidf)

        sorted_indices = np.argsort(cosine_similarities, axis=0)[::-1].flatten()
        sorted_urls = []
        for idx in sorted_indices:
            sorted_urls.append(ids[idx])

        in_params = ','.join(['%s'] * len(sorted_urls))
        mycursor = mydb.cursor(buffered=True)
        sql = "SELECT url_id ,url, title, description,frequency FROM urls WHERE url_id IN (%s)" % in_params
        mycursor.execute(sql, sorted_urls)
        data = mycursor.fetchall()
        mycursor.close()

        rank = rank_webpages(cosine_similarities, data, data_dict)

        sql = "INSERT INTO saved_result_queries (search_query) VALUES (%s)"
        val = ([query.lower()])
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()

        table_name = "result_" + query.replace(" ", "_").lower()
        sql = "CREATE TABLE IF NOT EXISTS {table_name} (url_id INT PRIMARY KEY,url TEXT,title TEXT,description TEXT,date datetime,frequency INT,cosine_similarity FLOAT,score FLOAT,ranking INT)".format(
            table_name=table_name)

        mycursor = mydb.cursor(buffered=True)
        try:
            mycursor.execute(sql)
            mydb.commit()
        except Exception as e:
            mydb.rollback()
            raise Exception(f"Error creating table {table_name}: {e}")
        mycursor.close()
        final_results = remove_duplicates(rank)
        task = save_to_db.delay(final_results, table_name)
        return final_results


@celery.task()
def save_to_db(results, table_name):
    mycursor = mydb.cursor(buffered=True)

    for idx, result in enumerate(results):
        result["rank"] = idx + 1
        sql = "INSERT INTO {table_name} (url_id, url, title, description, date, frequency, cosine_similarity, score, ranking) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)".format(
            table_name=table_name)
        val = (
            [result['id'], result['url'], result['title'], result['description'], result['date'], result['frequency'],
             result['cosine_similarity'], result['score'], result['rank']])
        mycursor.execute(sql, val)
        mydb.commit()
    mycursor.close()


def rank_webpages(cosine_similarities, data, data_dict, w1=0.8, w2=0.5):
    sorted_scores = []
    now = datetime.now()

    # iterate through every url that is somewhat related to the query and rank them
    for idx, i in enumerate(data):
        if i[2] != "N/A" and i[3] != "N/A" and cosine_similarities[idx] > 0.1:
            url = i[1]
            freq = i[4]
            if i[0] in data_dict:
                approx_date = data_dict.get(i[0])['date']

                time_diff = (now - approx_date).days

                # the older a result is the lower its score will be
                decayed_freq = freq / (1 + time_diff)
                score = w1 * cosine_similarities[idx] + w2 * decayed_freq
                sorted_scores.append(
                    {"id": i[0], "url": url, "title": i[2], "description": ' '.join(i[3].split()[:20]) + '...',
                     "date": approx_date, "frequency": i[4], "cosine_similarity": cosine_similarities[idx][0],
                     "score": score[0]})
    # sort urls by score
    sorted_scores = sorted(sorted_scores, key=lambda x: x["score"], reverse=True)
    return sorted_scores


def remove_duplicates(data):
    seen_urls = set()
    new_data = []
    for item in data:
        url = item['url']
        parsed_url = urllib.parse.urlparse(url)._replace(query='')
        normalized_url = urllib.parse.urlunparse(parsed_url)
        if normalized_url not in seen_urls:
            new_data.append(item)
            seen_urls.add(normalized_url)

    return new_data


@app.route('/tweets', methods=['GET'])
def get_url_tweets():
    args = request.args
    id_ = int(args["id"])
    query = args["query"]

    if id_ == "":
        return "Error: id can't be empty", 400
    elif not isinstance(id_, int):
        return "Error: id must be an int", 400

    if query == "":
        return "Error: query can't be empty", 400

    if id_ == "" and query == "":
        return "Error: id and query can't be empty",

    url_tweets = tweets.get_tweets(args["id"], args["query"])
    return url_tweets


if __name__ == '__main__':
    app.run(debug=True)
