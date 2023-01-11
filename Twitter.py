import requests
import tweepy
from flask import Flask,request, jsonify, make_response
from flask_cors import CORS
from bs4 import BeautifulSoup

# all the api keys
api_key = "H2stUS5brlYYEoznyxOPTNctW"
api_secret = "2eMQ4ZTV6ThlcRYPVW8cNHh5mGOhi26JcXcxLtOihYALaWSXTm"
access_token = "1504482408392904709-N5ILpyFmffn0IEZLqpTaEnMg8pSp6R"
access_secret = "VYKgAoBPh7bIkvNuMFRI0ixiG97egPe3v7ZyKwXNQgBpG"
bearer_token='AAAAAAAAAAAAAAAAAAAAANUmhAEAAAAAUeYWyb%2BJ1ulqC9p0SFHVW%2FgOL0c%3DTrvOfpDNEdQ18gFWw2dDnnzb5umsM1h93SmsN2rtBUUv8SXSFQ'

app = Flask(__name__)

CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/search', methods=['GET'])
def search():
    args = request.args
    return perform_search(args["query"])
    # return args
def perform_search(query):
    client = tweepy.Client(bearer_token=bearer_token)
    # query = "ukraine"

    links = {}
    # filter:links -filter:images -filter:videos
    search = "has:links -has:images -has:videos "+query
    print(search)
    tweets = tweepy.Paginator(client.search_recent_tweets, query=query,
                              tweet_fields=['entities'], max_results=100).flatten(limit=500)
    # tweets = client.search_recent_tweets(query=search, tweet_fields=['entities'], max_results=100)

    urls = []
    for tweet in tweets:
    # print(ascii(tweet.text))
        if tweet.entities is not None:
            if 'urls' in tweet.entities:
                # print("--------------------------------")
                # print(tweet.entities['urls'])
                # print("--------------------------------")
                # if 'expanded_url' in tweet.entities['urls']:
                #     print("gfyfyf
                if 'twitter' not in tweet.entities['urls'][0]['expanded_url'] and tweet.entities['urls'][0]['expanded_url'] not in urls:
                    urls.append(tweet.entities['urls'][0]['expanded_url'])
                    links.update({tweet.entities['urls'][0]['expanded_url']:1})
                if tweet.entities['urls'][0]['expanded_url'] in urls:
                    links[tweet.entities['urls'][0]['expanded_url']] += 1
    
    print(urls)
    print("£--------------------------------£")
    print(links)
    return urls
# def perform_webcrawl()

# def _build_cors_preflight_response():
#     response = make_response()
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add('Access-Control-Allow-Headers', "*")
#     response.headers.add('Access-Control-Allow-Methods', "*")
#     return response

# def _corsify_actual_response(response):
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response

if __name__ == '__main__':
   app.run(debug = True)



