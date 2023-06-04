import tweepy
import mysql.connector
import json
import time

api_key = "placeholder"
api_secret = "placeholder"
access_token = "placeholder"
access_secret = "placeholder"
bearer_token = 'placeholder'

mydb = mysql.connector.connect(
    host="placeholder",
    user="placeholder",
    password="placeholder",
    database="placeholder"
)



mycursor = mydb.cursor()

def check_if_in_db(tweet_id):
    mycursor = mydb.cursor()
    val = ([tweet_id])
    sql = "SELECT * FROM tweets WHERE tweet_id = %s"
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    mycursor.close()

    if len(data) == 0:
        return True
    else:
        return False


def update_url(url, title, description):
    mycursor = mydb.cursor()
    val = ([url])
    sql = "SELECT EXISTS(SELECT * from urls WHERE url=%s)"
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    mycursor.close()
    print(data[0][0])
    if data[0][0] == 0:
        mycursor = mydb.cursor()
        sql = "INSERT INTO urls (url, title, description) VALUES (%s, %s, %s)"
        val = ([url,title, description])
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        mycursor = mydb.cursor()
        sql = "UPDATE urls SET frequency = frequency+1 WHERE url=(%s)"
        val = ([url])
        mycursor.execute(sql, val)
        mydb.commit()

query = "ukraine"
search = "has:links -has:images -has:videos -has:media -is:retweet lang:en " + query

client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_secret,
                       access_token=access_token, access_token_secret=access_secret, wait_on_rate_limit=True)

tweets = tweepy.Paginator(client.search_recent_tweets, query=search,
                          tweet_fields=['entities', 'created_at', 'public_metrics'], expansions='author_id',
                          max_results=100).flatten(limit=500000)
try:
    for tweet in tweets:
        if tweet.entities is not None and check_if_in_db(tweet.id):
            if 'urls' in tweet.entities and 'twitter' not in tweet.entities['urls'][0]['expanded_url']:
                hashtags = []
                if 'hashtags' in tweet.entities:
                    for i in range(len(tweet.entities['hashtags'])):
                        hashtags.append(tweet.entities['hashtags'][i]['tag'])
                url = tweet.entities['urls'][0]['expanded_url']
                created_at = tweet.created_at
                content = tweet.text
                if 'title' not in tweet.entities['urls'][0]:
                    title = "N/A"
                else:
                    title = tweet.entities['urls'][0]['title']
                if 'description' not in tweet.entities['urls'][0]:
                    description = "N/A"
                else:
                    description = tweet.entities['urls'][0]['description']

                retweets = tweet.public_metrics['retweet_count']
                impressions = tweet.public_metrics['impression_count']
                tweet_id = tweet.id
                user_id = tweet.author_id
                mycursor = mydb.cursor()
                sql = "INSERT INTO tweets (url,created_at,tweet,query,retweets,impressions, tweet_id,user_id, hashtags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = ([url,created_at,content,query,retweets,impressions,tweet_id, user_id, json.dumps(hashtags)])
                mycursor.execute(sql, val)
                mydb.commit()
                update_url(url, title, description)
except tweepy.TweepyException:
    time.sleep(120)
