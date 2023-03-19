from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import mysql.connector
import json
import time
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import importlib
from sklearn.metrics.pairwise import cosine_similarity
import urllib.parse

tweets = importlib.import_module("tweetfreq")

scrape_in_progress = False
scrape_complete = False

results = []

# all the api keys
api_key = "H2stUS5brlYYEoznyxOPTNctW"
api_secret = "2eMQ4ZTV6ThlcRYPVW8cNHh5mGOhi26JcXcxLtOihYALaWSXTm"
access_token = "1504482408392904709-N5ILpyFmffn0IEZLqpTaEnMg8pSp6R"
access_secret = "VYKgAoBPh7bIkvNuMFRI0ixiG97egPe3v7ZyKwXNQgBpG"
bearer_token = 'AAAAAAAAAAAAAAAAAAAAANUmhAEAAAAAUeYWyb%2BJ1ulqC9p0SFHVW%2FgOL0c%3DTrvOfpDNEdQ18gFWw2dDnnzb5umsM1h93SmsN2rtBUUv8SXSFQ'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ShadowSlash247",
    database="mydatabase"
)

app = Flask(__name__)

CORS(app)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/search', methods=['GET'])
def search():
    args = request.args
    return get_results(args["query"])

@app.route('/results')
def get_results(query):
    #get every crawled webpage
    sql = "SELECT EXISTS(SELECT * from saved_result_queries WHERE search_query = %s)"
    val = ([query])
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(sql,val)
    mycursor.close()
    exists = mycursor.fetchone()[0]
    if exists == 1:
        app.logger.info("Success")
        mycursor = mydb.cursor(buffered=True)
        table_name = "result_" + query.replace(" ", "_").lower()
        sql = "SELECT * FROM {table_name}".format(table_name=table_name)
        mycursor.execute(sql)
        data = mycursor.fetchall()
        results = [dict(zip(("id", "url", "title","description", "date", "frequency", "cosine_similarity", "score", "ranking"), x)) for x in data]
        app.logger.info(results)
        results = sorted(results, key=lambda x: x["ranking"])
        mycursor.close()
        return results
    else:
        table_name = "result_" + query.replace(" ", "_").lower()
        # sql = "INSERT INTO mytable (id, url, title, description, date, frequency, cosine_similarity, score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        sql = "CREATE TABLE {table_name} (url_id INT PRIMARY KEY,url TEXT,title TEXT,description TEXT,date datetime,frequency INT,cosine_similarity FLOAT,score FLOAT,ranking INT)".format(table_name=table_name)
        
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute(sql)

        mydb.commit()

        # mycursor.execute(sql)
        mycursor.close()
        # mydb.commit()
        # app.logger.info(exists)
        start_time = time.time()
        mycursor = mydb.cursor(buffered=True)
        sql = "SELECT url_id,words,date FROM text_words"
        mycursor.execute(sql)
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
        # print(testresults.keys())
        terms_list = []
        # for doc in list:
        #     doc = json.loads(doc)
        #     terms_list.append(" ".join([term for term in doc.keys() for i in range(doc[term])]))
        #
        start_time = time.time()
        for key, value in data_dict.items():
            doc = json.loads(value['words'])
            terms_list.append(" ".join([term for term in doc.keys() for i in range(doc[term])]))

        end_time = time.time()
        elapsed_time = end_time - start_time

        app.logger.info(f"Test 2 - Elapsed time: {elapsed_time} seconds")

        vectorizer = TfidfVectorizer()

        # calculate tfidf values
        start_time = time.time()
        tfidf = vectorizer.fit_transform(terms_list)
        # print(tfidf)
        # app.logger.info(tfidf)

        #calculate tfidf values for query
        query_tfidf = vectorizer.transform([query])
        end_time = time.time()
        elapsed_time = end_time - start_time

        app.logger.info(f"Test 3 - Elapsed time: {elapsed_time} seconds")
        # print(query_tfidf)
        # app.logger.info(query_tfidf)

        #calculate cosine similarities for each document(webpage) in relation to the query
        start_time = time.time()
        cosine_similarities = cosine_similarity(tfidf, query_tfidf)
        print(cosine_similarities)
        end_time = time.time()
        elapsed_time = end_time - start_time

        app.logger.info(f"Test 4 - Elapsed time: {elapsed_time} seconds")

        # print the cosine similarities
        # app.logger.info(cosine_similarities)
        sorted_indices = cosine_similarities.argsort(axis=0)[::-1].flatten()
        sorted_indices = np.argsort(cosine_similarities, axis=0)[::-1].flatten()
        # sorted_indices = cosine_similarities.flatten()
        print(sorted_indices)
        # app.logger.info(sorted_indices)
        sorted_urls = []
        for idx in sorted_indices:
            # app.logger.info(f"hello :{ids[idx]}, CS: {cosine_similarities[idx]}")
            sorted_urls.append(ids[idx])
        end_time = time.time()
        elapsed_time = end_time - start_time

        app.logger.info(f"Test 5 - Elapsed time: {elapsed_time} seconds")

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
        # app.logger.info(rank_webpages(cosine_similarities, data, dates, terms_list))
        start_time = time.time()

        rank = rank_webpages(cosine_similarities, data, data_dict)
        sql = "INSERT INTO saved_result_queries (search_query) VALUES (%s)"
        val = ([query.lower()])
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(sql,val)
        mydb.commit()
        mycursor.close()
        results = remove_duplicates(rank)
        mycursor = mydb.cursor(buffered=True)
        
        for idx, result in enumerate(results):
            # app.logger.info(result)
            result["rank"] = idx + 1
            sql = "INSERT INTO {table_name} (url_id, url, title, description, date, frequency, cosine_similarity, score, ranking) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)".format(table_name=table_name)
            # app.logger.info(sql)
            val = ([result['id'], result['url'], result['title'], result['description'], result['date'], result['frequency'], result['cosine_similarity'], result['score'], result['rank']])
            mycursor.execute(sql,val)
            mydb.commit()
        mycursor.close()
        end_time = time.time()
        elapsed_time = end_time - start_time

        app.logger.info(f"Test 7 - Elapsed time: {elapsed_time} seconds")

        return results
    # return 


def rank_webpages(cosine_similarities, data, data_dict, w1=0.8, w2=0.5):
    # Calculate tweet frequency weights with exponential decay
    # max_freq = 0
    # weights = {}
    sorted_scores = []
    now = datetime.now()
    # print(cosine_similarities)
    # date_set = set()
    # for d in dates:
    #     date_set.update(d.keys())

    #iterate through every url that is somewhat related to the query and rank them
    for idx ,i in enumerate(data):
        if i[2] != "N/A" and i[3] != "N/A" and cosine_similarities[idx] > 0.1:
            url = i[1]
            
            freq = i[4]
            # app.logger.info(cosine_similarities[idx])
            # print(testresults.get(i[0]))
            # approx_date = testresults[i[0]]['date']
            # if i[0] in date_set:
            #     approx_date = next((d[i[0]] for d in dates if i[0] in d), None)
            if i[0] in data_dict:
                approx_date = data_dict.get(i[0])['date']

                time_diff = (now - approx_date).days

                # the older a result is the lower its score will be
                decayed_freq = freq / (1 + time_diff)
                # app.logger.info(cosine_similarities[idx][0])
                score = w1 * cosine_similarities[idx] + w2 * decayed_freq
                sorted_scores.append(
                    {"id": i[0], "url": i[1], "title": i[2], "description": ' '.join(i[3].split()[:20]) + '...',
                    "date": approx_date, "frequency": i[4], "cosine_similarity":cosine_similarities[idx][0], "score": score[0]})

            # print(score)
        # sorted_scores.sort(reverse=True)
    # sort urls by score
    sorted_scores = sorted(sorted_scores, key=lambda x: x["score"], reverse=True)
    # app.logger.info(ascii(sorted_scores))
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
