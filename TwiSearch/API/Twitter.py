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

tweets = importlib.import_module("tweetfreq")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ShadowSlash247",
    database="mydatabase"
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
        args = request.args
        return get_results(args["query"])
    except KeyError as e:
        return f"Error: {str(e)} is a required parameter and was not provided", 400
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return "An error occurred while processing the request", 500


@app.route('/results')
def get_results(query=None):
    #check if query has already been searched before
    sql = "SELECT EXISTS(SELECT * from saved_result_queries WHERE search_query = %s)"
    val = ([query])
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(sql, val)
    mycursor.close()
    exists = mycursor.fetchone()[0]
    # print(exists)

    # if query already has stored results then return them
    if exists == 1:
        mycursor = mydb.cursor(buffered=True)
        table_name = "result_" + query.replace(" ", "_").lower()
        sql = "SELECT * FROM {table_name}".format(table_name=table_name)
        mycursor.execute(sql)
        data = mycursor.fetchall()
        final_results = [dict(
            zip(("id", "url", "title", "description", "date", "frequency", "cosine_similarity", "score", "ranking"), x))
            for x in data]
        final_results = sorted(final_results, key=lambda x: x["ranking"])
        mycursor.close()
        return final_results
    
    # otherwise need to find relevant results
    else:
        table_name = "result_" + query.replace(" ", "_").lower()
        sql = "CREATE TABLE {table_name} (url_id INT PRIMARY KEY,url TEXT,title TEXT,description TEXT,date datetime,frequency INT,cosine_similarity FLOAT,score FLOAT,ranking INT)".format(
            table_name=table_name)

        mycursor = mydb.cursor(buffered=True)

        mycursor.execute(sql)

        mydb.commit()

        mycursor.close()
        
        start_time = time.time()
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

        in_params = ','.join(['%s'] * len(url_ids))
        sql = "SELECT url_id,words,date FROM text_words WHERE url_id IN (%s)" % in_params
        # sql = "SELECT url_id,words,date FROM text_words"
        # mycursor.execute(sql)
        mycursor.execute(sql, url_ids)
        data = mycursor.fetchall()

        mycursor.close()
        # list = []
        ids = []
        # dates = []
        data_dict = {}
        for i in data:
            ids.append(i[0])
            # list.append(i[1])
            # dates.append({i[0]: i[2]})
            data_dict[i[0]] = {"words": i[1], "date": i[2]}
        # print(testresults)
        end_time = time.time()
        elapsed_time = end_time - start_time

        app.logger.info(f"Test 1 - Elapsed time: {elapsed_time} seconds")
        print(f"Test 1 - Elapsed time: {elapsed_time} seconds")
        # print(testresults.keys())
        terms_list = []
        start_time = time.time()
        for key, value in data_dict.items():
            doc = json.loads(value['words'])
            terms_list.append(" ".join([term for term in doc.keys() for i in range(doc[term])]))

        end_time = time.time()
        elapsed_time = end_time - start_time

    
        #create TF-IDF vectors for terms list and query
        vectorizer = TfidfVectorizer()

        tfidf = vectorizer.fit_transform(terms_list)
        
        query_tfidf = vectorizer.transform([query])

        # calculate cosine similarities for each document(webpage) in relation to the query
        cosine_similarities = cosine_similarity(tfidf, query_tfidf)
        
        sorted_indices = np.argsort(cosine_similarities, axis=0)[::-1].flatten()
        # sorted_indices = cosine_similarities.flatten()
        # print(sorted_indices)
        # app.logger.info(sorted_indices)
        sorted_urls = []
        for idx in sorted_indices:
            # app.logger.info(f"hello :{ids[idx]}, CS: {cosine_similarities[idx]}")
            sorted_urls.append(ids[idx])
        end_time = time.time()
        elapsed_time = end_time - start_time

        app.logger.info(f"Test 5 - Elapsed time: {elapsed_time} seconds")
        print(f"Test 5 - Elapsed time: {elapsed_time} seconds")

        # app.logger.info(sorted_urls)
        start_time = time.time()
        in_params = ','.join(['%s'] * len(sorted_urls))
        mycursor2 = mydb.cursor(buffered=True)
        # sql = "SELECT url_id ,url, title, description,frequency FROM urltest"
        sql = "SELECT url_id ,url, title, description,frequency FROM urltest WHERE url_id IN (%s)" % in_params
        mycursor2.execute(sql, sorted_urls)
        # mycursor2.execute(sql)
        data = mycursor2.fetchall()
        mycursor2.close()
        end_time = time.time()
        elapsed_time = end_time - start_time

        app.logger.info(f"Test 6 - Elapsed time: {elapsed_time} seconds")
        print(f"Test 6 - Elapsed time: {elapsed_time} seconds")
        # app.logger.info(rank_webpages(cosine_similarities, data, dates, terms_list))
        start_time = time.time()

        rank = rank_webpages(cosine_similarities, data, data_dict)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Test 7 - Elapsed time: {elapsed_time} seconds")

        # start_time = time.time()
        sql = "INSERT INTO saved_result_queries (search_query) VALUES (%s)"
        val = ([query.lower()])
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        final_results = remove_duplicates(rank)
        # save_to_db(final_results,table_name)
        task = save_to_db.delay(final_results, table_name)
        # thread = Thread(target=save_to_db(final_results, table_name))
        # thread.start()
        # end_time = time.time()
        # elapsed_time = end_time - start_time
        #
        # app.logger.info(f"Test 7 - Elapsed time: {elapsed_time} seconds")
        # print(f"Test 8 - Elapsed time: {elapsed_time} seconds")

        return final_results
    # return 


@celery.task()
def save_to_db(results, table_name):
    start_time = time.time()
    mycursor = mydb.cursor(buffered=True)

    for idx, result in enumerate(results):
        # app.logger.info(result)
        result["rank"] = idx + 1
        sql = "INSERT INTO {table_name} (url_id, url, title, description, date, frequency, cosine_similarity, score, ranking) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)".format(
            table_name=table_name)
        # app.logger.info(sql)
        val = (
            [result['id'], result['url'], result['title'], result['description'], result['date'], result['frequency'],
             result['cosine_similarity'], result['score'], result['rank']])
        mycursor.execute(sql, val)
        mydb.commit()
    mycursor.close()
    end_time = time.time()
    elapsed_time = end_time - start_time

    app.logger.info(f"Test 7 - Elapsed time: {elapsed_time} seconds")
    print(f"Test 8 - Elapsed time: {elapsed_time} seconds")
    # time.sleep(10)
    # import pandas as pd
    # pd.DataFrame(['sameple data']).to_csv('./success.csv')
    # return print('large function completed')


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
                    {"id": i[0], "url": i[1], "title": i[2], "description": ' '.join(i[3].split()[:20]) + '...',
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
    print(args)
    url_tweets = tweets.get_tweets(args["id"], args["query"])
    return url_tweets


if __name__ == '__main__':
    app.run(debug=True)
