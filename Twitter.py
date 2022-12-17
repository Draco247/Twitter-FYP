import requests
import tweepy
from flask import Flask,request

# all the api keys
api_key = "H2stUS5brlYYEoznyxOPTNctW"
api_secret = "2eMQ4ZTV6ThlcRYPVW8cNHh5mGOhi26JcXcxLtOihYALaWSXTm"
access_token = "1504482408392904709-N5ILpyFmffn0IEZLqpTaEnMg8pSp6R"
access_secret = "VYKgAoBPh7bIkvNuMFRI0ixiG97egPe3v7ZyKwXNQgBpG"
bearer_token='AAAAAAAAAAAAAAAAAAAAANUmhAEAAAAAUeYWyb%2BJ1ulqC9p0SFHVW%2FgOL0c%3DTrvOfpDNEdQ18gFWw2dDnnzb5umsM1h93SmsN2rtBUUv8SXSFQ'

app = Flask(__name__)

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
    query = "ukraine"

    search = "has:links -has:media "+query

    tweets = client.search_recent_tweets(query=query, tweet_fields=['entities'], max_results=10)

    urls = []
    for tweet in tweets.data:
    # print(ascii(tweet.text))
        if len(tweet.entities) is not None:
            if 'urls' in tweet.entities:
                # print("--------------------------------")
                # print(tweet.entities['urls'])
                urls.append(tweet.entities['urls'])
    return urls

if __name__ == '__main__':
   app.run(debug = True)



