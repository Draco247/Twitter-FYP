import requests
import tweepy
from flask import Flask,request, jsonify, make_response
from flask_cors import CORS
# from bs4 import BeautifulSoup
import mysql.connector
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import snscrape.modules.twitter as sntwitter
# from openpyxl import Workbook,load_workbook
import pandas as pd
from scrapy.crawler import CrawlerRunner, CrawlerProcess
# from twitterlinkscraper.twitterlinkscraper.spiders.linkscraper import LinkscraperSpider
import json
from threading import Thread
import time
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import os
from nltk.stem import PorterStemmer
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
import random
from difflib import SequenceMatcher

settings = Settings()
settings_file_path = 'twitterlinkscraper.twitterlinkscraper.settings'
os.environ['SCRAPY_SETTINGS_MODULE'] = settings_file_path
settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
settings.setmodule(settings_module_path, priority='project')

crawl_runner = CrawlerProcess(settings)
# spider = LinkscraperSpider
scrape_in_progress = False
scrape_complete = False

results = []

# all the api keys
api_key = "H2stUS5brlYYEoznyxOPTNctW"
api_secret = "2eMQ4ZTV6ThlcRYPVW8cNHh5mGOhi26JcXcxLtOihYALaWSXTm"
access_token = "1504482408392904709-N5ILpyFmffn0IEZLqpTaEnMg8pSp6R"
access_secret = "VYKgAoBPh7bIkvNuMFRI0ixiG97egPe3v7ZyKwXNQgBpG"
bearer_token='AAAAAAAAAAAAAAAAAAAAANUmhAEAAAAAUeYWyb%2BJ1ulqC9p0SFHVW%2FgOL0c%3DTrvOfpDNEdQ18gFWw2dDnnzb5umsM1h93SmsN2rtBUUv8SXSFQ'

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
    return perform_search_3(args["query"])
    # return perform_search(args["query"])

def perform_search(query):
    client = tweepy.Client(bearer_token=bearer_token)
    query = "brexit"

    # links = {}
    # {1: {'url': 'http://www.drpeppersnapplegroup.com/', 'name': 'Dr. Pepper-Snapple Group', 'frequency': 57}, 2: {'url': 'http://www.rccolainternational.com/', 'name': 'Royal Crown Cola', 'frequency': 41}}
    search = "has:links -has:images -has:videos  "+query
    print(search)
    tweets = tweepy.Paginator(client.search_recent_tweets, query=search,tweet_fields=['entities','created_at'],expansions=['entities.mentions.username','author_id'] ,user_fields=['username'], max_results=100).flatten(limit=200)

    urls = []
    count = 0
    for tweet in tweets:
        # print(ascii(tweet.text))
       
        if tweet.entities is not None and 'mentions' in tweet.entities:
            if 'urls' in tweet.entities:
                # print(tweet.entities)
                
                print(check_if_in_db(tweet.entities['urls'][0]['expanded_url'],tweet.created_at,tweet.entities['mentions'][0]['username']))
                if 'twitter' not in tweet.entities['urls'][0]['expanded_url'] and check_if_in_db(tweet.entities['urls'][0]['expanded_url'],tweet.created_at,tweet.entities['mentions'][0]['username']):
                    # clean_text(ascii(tweet.text))
                    print("clear")
                    # urls.append(tweet.entities['mentions'][0]['username'])
                    # urls.append(tweet.entities['urls'][0]['expanded_url'])
                    to_db(tweet.entities['urls'][0]['expanded_url'],tweet.created_at,ascii(tweet.text),query,tweet.entities['mentions'][0]['username'])
                # if 'twitter' not in tweet.entities['urls'][0]['expanded_url'] and check_if_in_db(tweet.entities['urls'][0]['expanded_url'],tweet.created_at) == True:
                #     # freq_update(tweet.entities['urls'][0]['expanded_url'])
                #     print("not clear")
                # if 'twitter' not in tweet.entities['urls'][0]['expanded_url'] and tweet.entities['urls'][0]['expanded_url'] not in urls:
                #     # urls.append(tweet.entities['urls'][0]['expanded_url'])
                #     # links.update({"url":tweet.entities['urls'][0]['expanded_url'], "frequency":1})
                #     urls.append({"entry":{"url":tweet.entities['urls'][0]['expanded_url'], "frequency":1}})
                #     count+=1
                    # urls.append({"entry"+str(count):{"url":tweet.entities['urls'][0]['expanded_url'], "frequency":1}})

                    # clean_text(ascii(tweet.text)
                    # to_db(tweet.entities['urls'][0]['expanded_url'],tweet.created_at,ascii(tweet.text),query)
                # if tweet.entities['urls'][0]['expanded_url'] in urls:
                    # links[tweet.entities['urls'][0]['expanded_url']] += 1
                    # freq_update(tweet.entities['urls'][0]['expanded_url'])
    
    # print(urls)
    # print("£------------------------------£")
    # print(links
    
    return urls

def perform_search_2(query):
    # wb = Workbook()
    # ws = wb.active
    # ws.title = "Sheet1"
    # ws.append(["Link"])
    global scrape_complete

    links = []
    # links2 = []
    maxTweets =100
    # need to change date range to a week from current date
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query+' since:2023-02-07 until:2023-02-08 lang:"en" ').get_items()):
        if i>maxTweets:
            break
        if tweet.links:
            if 'twitter' not in tweet.links[0].url and check_if_in_db(tweet.links[0].url, tweet.date, tweet.user.username):
                to_db(tweet.links[0].url,tweet.date,tweet.rawContent,query,tweet.user.username,tweet.id)
                links.append([str(tweet.links[0].url)])
                # links2.append([str(tweet)])

    linksdf = pd.DataFrame(links, columns=['links'])
    # print(linksdf)
    linksdf.to_csv('links.csv',index=False)
    time.sleep(10)
    # might need to leave some time for crawler to load the links
    perform_webcrawl()
    testthread = Thread(target=task)
    testthread.start()
    testthread.join()
    results = get_results()
    # clean_text(query,results)
    return results
    # return links

def perform_search_3(query):
    #first need to search for all tweets in the database that were found using the same or similiar query
    # print(f"query = {query}")
    mycursor = mydb.cursor()
    sql = "SELECT DISTINCT(url_id) FROM tweettest2 WHERE query = %s"
    mycursor.execute(sql,(query,))
    data = mycursor.fetchall()
    print(data)
    url_ids = [item for t in data for item in t]
    mycursor2 = mydb.cursor()
    # # val2 = [[list([item]) for item in url_ids]]
    sql2 = "INSERT into to_crawl (url_id) VALUES (%s)"
    mycursor2.executemany(sql2,data)
    mydb.commit()
    # print()
    # url_parts = get_urls(url_ids)
    # print(ascii(url_parts))
    time.sleep(5)
    perform_webcrawl()
    # task()
    # get_results(query)
    # then need to perform keyword extracion on these tweets aswell as crawl the unique links in these tweets to extract the page content of these tweets
    # then need to rank the related links and have them returned while also using the ranks to return highly rated tweets that referenced them as well as keywords related to the query taken from these tweets
    # return data

def get_urls(url_ids):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ShadowSlash247",
    database="mydatabase"
    )
    curr = conn.cursor()
    urls = []
    for i in url_ids:
        # print(i)
        sql = "SELECT url FROM urltest WHERE url_id = %s" 
        val = (i,)
        curr.execute(sql,val)
        data = curr.fetchone()
        # print(f"data is here {ascii(data)}")
        urls.append(data[0])
    # urls = [item for t in data for item in t]
    # print(ascii(urls))
    return urls
    # print("-------------")
    # print(data)
    # # print(f"urls = {urls[0]}")
    # print("--------------------")
    # start_urls = []
    # ids = []
    # for i in data:
    #     id = i[0]
    #     print(f"id = {id}")
    #     ids.append(i[0])
    #     start_urls.append(i[1])
    # print(start_urls)
    
def check_if_in_db(url, created_at,username):

    mycursor = mydb.cursor()
    val = (url,created_at,username)
    sql = "SELECT * FROM test WHERE url = %s AND created_at = %s AND user = %s"
    # mycursor.execute("SELECT ame FROM workers WHERE symbol=%s", (name,))
    # val = (url, created_at
    mycursor.execute(sql, val)
    # print(mycursor.statement)
    # print(mycurs

    data = mycursor.fetchall()

    # print(data)

    if len(data) == 0:
        return True
    else:
        return False

def to_db(url,created_at,tweet_text,query,username,tweet_id):
    # print(url)
    # print(created_at)
    # print(tweet_text)
    # print(query)
    # print(username)
    
    
    mycursor = mydb.cursor()
    sql = "INSERT INTO test (url,created_at,tweet,query,user,tweet_id) VALUES (%s,%s,%s,%s,%s,%s)"
    val = ([url,created_at,tweet_text,query,username,tweet_id])
    mycursor.execute(sql, val)
    mydb.commit()

def freq_update(url):
    print(url)
    # print("fgoeijgeogiheg")
    mycursor = mydb.cursor()
    sql = "UPDATE test SET frequency = frequency + 1 WHERE url = %s"
    val = ([url])
    mycursor.execute(sql, val)
    mydb.commit()

def clean_text(query,results):
    for result in results:
        # stemmer = PorterStemmer()
        # stop_words = set(stopwords.words("english"))
        # query = [stemmer.stem(w) for w in word_tokenize(query) if w not in stop_words]
        # query = " ".join(query)
        # documents = [
        #     " ".join([stemmer.stem(w) for w in word_tokenize(doc) if w not in stop_words])
        #     for doc in result
        # ]
        # # Compute TF-IDF scores
        # tfidf_vectorizer = TfidfVectorizer()
        # tfidf_matrix = tfidf_vectorizer.fit_transform([query] + documents)
        # query_tfidf = tfidf_matrix[0]
        # document_tfidfs = tfidf_matrix[1:]
        # # Compute cosine similarities
        # cosine_similarities = np.dot(document_tfidfs, query_tfidf.T)
        # # Rank documents by cosine similarity
        # ranked_indices = np.argsort(-cosine_similarities)
        # for i in ranked_indices:
        #     print(documents[i])
        # Return top N results
        # print([documents[i] for i in ranked_indices[:num_results]])
        # return [documents[i] for i in ranked_indices[:num_results]]
        # print(result['content'])

        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(result['content'])
        # converts the words in word_tokens to lower case and then checks whether 
        #they are present in stop_words or not
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        #with no lower case conversion
        filtered_sentence = []
        
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        
        print(word_tokens)
        print(filtered_sentence)

# def send
# @app.route('/crawl')
def task():
    global scrape_complete
    while scrape_complete == False:
        time.sleep(5)
        # print("apples: ",scrape_complete)
    print("done")

# @app.route('/crawl')
def perform_webcrawl():
    global scrape_in_progress
    global scrape_complete
    

    if not scrape_in_progress:
        # global results
        scrape_in_progress = True
        # crawl_runner.crawl(LinkscraperSpider)
        # crawl_runner.start()
        # eventual = crawl_runner.crawl(LinkscraperSpider,results=results)
        eventual = crawl_runner.crawl(LinkscraperSpider)
        eventual.addCallback(finished_scrape)
        return 'SCRAPING'
    elif scrape_complete:
        # get_results()
        return 'SCRAPE COMPLETE'
    return 'SCRAPE IN PROGRESS'

@app.route('/results')
def get_results():
    """
    Get the results only if a spider has results
    """
    results2 = []
    global scrape_complete
    if scrape_complete:
        # print("donzo")
        mycursor = mydb.cursor()
        sql = "SELECT url_id,words FROM text_words"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        # print(data[1][1])
        # trying = dict((y, x) for x, y in data[1][1])
        # trying = json.loads("[" + data[1][1] + "]")
        list = []
        ids = []
        for i in data:
            ids.append(i[0])
            list.append(i[1])
        # print(f"ids = {ids}")
        vals = []
        sums = []
        tests = []
        finalresults = {}
        # print(trying)
        count = 0
        for i in list:
            sum = 0
            totalsum = 0
            # print(i)
            # vals.append(i)
            for j in json.loads(i):
                # if "ukraine" in
                totalsum += json.loads(i)[j]
                if SequenceMatcher(None, a="ukraine",b=j).ratio() > 0.74:
                    # print(json.loads(i)[j])
                    sum += json.loads(i)[j]
                    if sum > 0:
                        sums.append(sum)
                        vals.append({sum:json.loads(i)})
            # print(sum)
            # print(totalsum)
            if sum != 0:
                # print(f"{ids[count]} : {sum/totalsum}")
                finalresults[ids[count]] = sum/totalsum 
                tests.append(sum/totalsum)
            # print("*---------------------------")
            count += 1
        # df = pd.DataFrame.from_dict(finalresults, orient='columns')
        df = pd.Series(finalresults).reset_index()
        df.columns = ['url_id', 'tf']
        # print(df)
        sorted_df = df.sort_values(by=['tf'], ascending=False)
        sorted_df['rank'] = sorted_df['tf'].rank(ascending=False)
        print(sorted_df)
        # tests.sort(reverse=True)
        # # print(tests)
        # in_params = ','.join(['%s'] * len(ids))
        # sql = "SELECT url_id, url FROM urltest WHERE url_id IN (%s)" % in_params
        # mycursor.execute(sql, ids)
        # data = mycursor.fetchall()
        # # print(data)
        # sorted_ids = []
        # # count2 = 0
        # for i in tests:
        #     # print(f"{id}:{tf}")
        #     for id, tf in finalresults.items():
        #         print(i)
        #         print(tf)
        #         print("------------------------")
        #         if i == tf and id not in sorted_ids:
        #             sorted_ids.append(id)
        #             break
        # print(sorted_ids)
        # sorted_urls = []

        # dicty = dict((y, x) for x, y in data)
        
        # for i in sorted_ids:
        #     # print(f"{id}:{url}")
        #     for url, id in dicty.items():
        #         if i == id:
        #             print(f"{id}:{finalresults.get(id)}")
        #             sorted_urls.append(url)
        
        # for i in sorted_ids:
        #     for j in dicty:


        # for i in vals:
        
            #     if SequenceMatcher(None, a="ukraine",b=item2).ratio() > 0.80:
            # if "ukraine" in json.loads(i[1]):
            #     vals.append(json.loads(i[1]))
        # random.shuffle(vals)
        # ranked_urls = []
        # sql = "SELECT url FROM urltest WHERE url_id IN (%s)"
        # placeholders = ', '.join(['%s'] * len(vals))
        # formatted_query = sql % placeholders

        # # execute the query with the list of IDs as parameters
        # mycursor.execute(formatted_query, vals)
        # rows = mycursor.fetchall()

        # # print out the rows
        # for row in rows:
        #     ranked_urls.append(row[0])
            # print(row)
        # for i in vals:
        # for i in trying:
        #     if "ukraine" in json.loads(i):
        #         # print(type(json.loads(i)))
        #         # print(f"freq = {json.loads(i)['ukraine']}")
        #         vals.append(json.loads(i)['ukraine'])
        #         vals.sort()
        #         # print(f"{i.key} --> freq = {json.loads(i)["ukraine"]}")
        # print("pear")
        # # print(type(results[0]))
        # for line in open('result.json', 'r'):
        #     results2.append(json.loads(line))
        # with open('C://Users//dan//Documents//GitHub//Twitter-FYP//twitterlinkscraper//result.json') as test_file:
        #     data = json.load(test_file)
        # return result.json()
        # return "hello"
        # print(trying.keys())
        # print(vals)
        # random.shuffle(ranked_urls)
        # sums.sort()
        # print(sums)
        # print(finalresults)
        # dicty = json.dumps(dicty)
        return df
        # return sorted_urls
        # for result in results:
        #     return jsonify(result)
    return 'Scrape Still Progress'

def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global scrape_complete
    scrape_complete = True


if __name__ == '__main__':
    from sys import stdout
    from twisted.logger import globalLogBeginner, textFileLogObserver
    from twisted.web import server, wsgi
    from twisted.internet import endpoints, reactor

    # start the logger
    # globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    # start the WSGI server
    root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    factory = server.Site(root_resource)
    http_server = endpoints.TCP4ServerEndpoint(reactor, 9000)
    http_server.listen(factory)

    # start event loop
    reactor.run()
    # to_db()
#    app.run(debug = True)




