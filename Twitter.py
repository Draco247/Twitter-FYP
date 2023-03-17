import requests
import tweepy
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
# from bs4 import BeautifulSoup
import mysql.connector
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import snscrape.modules.twitter as sntwitter
# from openpyxl import Workbook,load_workbook
import pandas as pd
# from scrapy.crawler import CrawlerRunner, CrawlerProcess
# from twitterlinkscraper.twitterlinkscraper.spiders.linkscraper import LinkscraperSpider
import json
from threading import Thread
import time
from datetime import datetime, timedelta
import logging
# from scrapy.utils.project import get_project_settings
# from scrapy.settings import Settings
# import os
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import random
from difflib import SequenceMatcher
import numpy as np
import importlib
from sklearn.metrics.pairwise import cosine_similarity
import math

tweets = importlib.import_module("tweetfreq")

# settings = Settings()
# settings_file_path = 'twitterlinkscraper.twitterlinkscraper.settings'
# os.environ['SCRAPY_SETTINGS_MODULE'] = settings_file_path
# settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
# settings.setmodule(settings_module_path, priority='project')

# crawl_runner = CrawlerProcess(settings)
# spider = LinkscraperSpider
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
    # return perform_search_3(args["query"])
    # return perform_search(args["query"])

@app.route('/results')
def get_results(query):
    #get every crawled webpage
    start_time = time.time()
    mycursor = mydb.cursor(buffered=True)
    sql = "SELECT url_id,words,date FROM text_words"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    list = []
    ids = []
    dates = []
    testresults = {}
    for i in data:
        ids.append(i[0])
        list.append(i[1])
        dates.append({i[0]: i[2]})
        testresults[i[0]] = {"words": i[1], "date": i[2]}
    # print(testresults)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Test 1 - Elapsed time: {elapsed_time} seconds")
    # print(testresults.keys())
    terms_list = []
    # for doc in list:
    #     doc = json.loads(doc)
    #     terms_list.append(" ".join([term for term in doc.keys() for i in range(doc[term])]))
    #
    start_time = time.time()
    for key, value in testresults.items():
        doc = json.loads(value['words'])
        terms_list.append(" ".join([term for term in doc.keys() for i in range(doc[term])]))

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Test 2 - Elapsed time: {elapsed_time} seconds")

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

    print(f"Test 3 - Elapsed time: {elapsed_time} seconds")
    # print(query_tfidf)
    # app.logger.info(query_tfidf)

    #calculate cosine similarities for each document(webpage) in relation to the query
    start_time = time.time()
    cosine_similarities = cosine_similarity(tfidf, query_tfidf)
    print(cosine_similarities)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Test 5 - Elapsed time: {elapsed_time} seconds")

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

    print(f"Test 3 - Elapsed time: {elapsed_time} seconds")

    # app.logger.info(sorted_urls)
    start_time = time.time()
    in_params = ','.join(['%s'] * len(sorted_urls))
    mycursor2 = mydb.cursor(buffered=True)
    # sql = "SELECT url_id ,url, title, description,frequency FROM urltest"
    sql = "SELECT url_id ,url, title, description,frequency FROM urltest WHERE url_id IN (%s)" % in_params
    mycursor2.execute(sql, sorted_urls)
    # mycursor2.execute(sql)
    data = mycursor2.fetchall()
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Test 4 - Elapsed time: {elapsed_time} seconds")
    # app.logger.info(rank_webpages(cosine_similarities, data, dates, terms_list))
    return rank_webpages(cosine_similarities, data, dates, testresults)


def rank_webpages(cosine_similarities, data, dates, testresults, w1=0.8, w2=0.5):
    # Calculate tweet frequency weights with exponential decay
    # max_freq = 0
    # weights = {}
    sorted_scores = []
    now = datetime.now()
    # print(cosine_similarities)
    date_set = set()
    for d in dates:
        date_set.update(d.keys())

    #iterate through every url that is somewhat related to the query and rank them
    for idx ,i in enumerate(data):
        if i[2] != "N/A" and i[3] != "N/A" and cosine_similarities[idx] > 0.1:
            url = i[1]
            
            freq = i[4]
            # print(testresults.get(i[0]))
            # approx_date = testresults[i[0]]['date']
            if i[0] in date_set:
                approx_date = next((d[i[0]] for d in dates if i[0] in d), None)

                time_diff = (now - approx_date).days

                # the older a result is the lower its score will be
                decayed_freq = freq / (1 + time_diff)
                # app.logger.info(cosine_similarities[idx][0])
                score = w1 * cosine_similarities[idx] + w2 * decayed_freq
                sorted_scores.append(
                    {"id": i[0], "url": i[1], "title": i[2], "description": ' '.join(i[3].split()[:20]) + '...',
                    "date": approx_date, "frequency": i[4], "score": score[0]})

            # print(score)
        # sorted_scores.sort(reverse=True)
    # sort urls by score
    sorted_scores = sorted(sorted_scores, key=lambda x: x["score"], reverse=True)
    # app.logger.info(ascii(sorted_scores))
    return sorted_scores


@app.route('/tweets', methods=['GET'])
def get_url_tweets():
    args = request.args
    print(args)
    url_tweets = tweets.get_tweets(args["id"], args["query"])
    return url_tweets



if __name__ == '__main__':
    app.run(debug=True)
