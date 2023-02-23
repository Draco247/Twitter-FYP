import tweepy
# from tweepy import Client, Paginator, RateLimitError
import mysql.connector
import json
import time


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

query = "Brexit"
search = "has:links -has:images -has:videos -has:media -is:retweet lang:en "+query


client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)


def check_if_in_db(tweet_id):
    mycursor = mydb.cursor()
    val = ([tweet_id])
    sql = "SELECT * FROM tweets WHERE tweet_id = %s"
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

# Name and path of the file where you want the Tweets written to
tweets = tweepy.Paginator(client.search_recent_tweets, query=search,tweet_fields=['entities','created_at','public_metrics'], max_results=100).flatten(limit=500000)
try:
    for tweet in tweets:
        if tweet.entities is not None and check_if_in_db(tweet.id):
            if 'urls' in tweet.entities and 'twitter' not in tweet.entities['urls'][0]['expanded_url']:
                hashtags = []
                # print(ascii(tweet.entities))
                # print("******************************")
                if 'hashtags' in tweet.entities:
                    for i in range (len(tweet.entities['hashtags'])):
                         hashtags.append(tweet.entities['hashtags'][i]['tag'])
                # print(hashtags)
                url = tweet.entities['urls'][0]['expanded_url']
                created_at = tweet.created_at
                content = tweet.text
                # print(tweet.public_metrics)
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
                print(tweet_id)
                mycursor = mydb.cursor()
                sql = "INSERT INTO tweets (url,title,description,created_at,tweet,query,retweets,impressions, tweet_id, hashtags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = ([url,title,description,created_at,content,query,retweets,impressions,tweet_id, json.dumps(hashtags)])
                mycursor.execute(sql, val)
                mydb.commit()
except tweepy.TweepyException:
    time.sleep(120)

# client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

# auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
# api = tweepy.API(auth)
# query = "Brexit"
# search_terms = [query +"has:links -has:images -has:videos -has:media -is:retweet lang:en "]

# # # Bot searches for tweets containing certain keywords
# class MyStream(tweepy.StreamingClient):

#     # This function gets called when the stream is working
#     def on_connect(self):

#         print("Connected")


#     # This function gets called when a tweet passes the stream
#     def on_tweet(self, tweet):

#         if tweet.entities is not None and check_if_in_db(tweet.id):
#             if 'urls' in tweet.entities and 'twitter' not in tweet.entities['urls'][0]['expanded_url']:
#                 hashtags = []
#                 # print(ascii(tweet.entities))
#                 # print("******************************")
#                 if 'hashtags' in tweet.entities:
#                     for i in range (len(tweet.entities['hashtags'])):
#                             hashtags.append(tweet.entities['hashtags'][i]['tag'])
#                 # print(hashtags)
#                 url = tweet.entities['urls'][0]['expanded_url']
#                 created_at = tweet.created_at
#                 content = tweet.text
#                 # print(tweet.public_metrics)
#                 if 'title' not in tweet.entities['urls'][0]:
#                     title = "N/A"
#                 else:
#                     title = tweet.entities['urls'][0]['title']
#                 if 'description' not in tweet.entities['urls'][0]:
#                     description = "N/A"
#                 else:
#                     description = tweet.entities['urls'][0]['description']

#                 retweets = tweet.public_metrics['retweet_count']
#                 impressions = tweet.public_metrics['impression_count']
#                 tweet_id = tweet.id
#                 print(tweet_id)
#                 mycursor = mydb.cursor()
#                 sql = "INSERT INTO tweets (url,title,description,created_at,tweet,query,retweets,impressions, tweet_id, hashtags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#                 val = ([url,title,description,created_at,content,query,retweets,impressions,tweet_id, json.dumps(hashtags)])
#                 mycursor.execute(sql, val)
#                 mydb.commit()
#         # except tweepy.TweepyException:
#         #     time.sleep(120)
        

# # Creating Stream object
# stream = MyStream(bearer_token=bearer_token)

# # Adding terms to search rules
# # It's important to know that these rules don't get deleted when you stop the
# # program, so you'd need to use stream.get_rules() and stream.delete_rules()
# # to change them, or you can use the optional parameter to stream.add_rules()
# # called dry_run (set it to True, and the rules will get deleted after the bot
# # stopped running).
# for term in search_terms:
#     stream.add_rules(tweepy.StreamRule(term),dry_run=True)

# # Starting stream
# stream.filter(tweet_fields=['created_at','entities','public_metrics'])

# try: 
#     for tweet in tweets:
#         if tweet.entities is not None and 'mentions' in tweet.entities:
#             if 'urls' in tweet.entities and 'twitter' not in tweet.entities['urls'][0]['expanded_url']:
#                 # print(ascii(tweet.entities))
#                 # print("******************************")
#                 if 'hashtags' in tweet.entities:
#                     print(tweet.entities)
#                 url = tweet.entities['urls'][0]['expanded_url']
#                 created_at = tweet.created_at
#                 content = tweet.text
#                 # print(tweet.public_metrics)
#                 if 'title' not in tweet.entities['urls'][0]:
#                     title = "N/A"
#                 else:
#                     title = tweet.entities['urls'][0]['title']
#                 if 'description' not in tweet.entities['urls'][0]:
#                     description = "N/A"
#                 else:
#                     description = tweet.entities['urls'][0]['description']

#                 retweets = tweet.public_metrics['retweet_count']
#                 impressions = tweet.public_metrics['impression_count']
#                 tweet_id = tweet.id
#                 print(tweet_id)
#                 mycursor = mydb.cursor()
#                 sql = "INSERT INTO tweets (url,title,description,created_at,tweet,query,retweets,impressions, tweet_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#                 val = ([url,title,description,created_at,content,query,retweets,impressions,tweet_id])
#                 mycursor.execute(sql, val)
#                 mydb.commit()
# except tweepy.RateLimitError as exc:
#     print('Rate limit!')

# with open(file_name, 'a+') as filehandle:
#     for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
#                                   tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(
#             limit=1000):
#         filehandle.write('%s\n' % tweet.id)

# auth = tweepy.OAuth1UserHandler(
#   api_key, 
#   api_secret, 
#   access_token, 
#   access_secret
# )

# api = tweepy.API(auth)


# extracted_tweets = []

# for status in tweepy.Cursor(api.search_tweets, 
#                             "Ukraine", 
#                             lang="en",
#                             count=100).items(250):
#     extracted_tweets.append(ascii(status))
# print(extracted_tweets)
# client = tweepy.Client(bearer_token=bearer_token)

# search = "has:links -has:images -has:videos  "+query
# print(search)
# tweets = tweepy.Paginator(client.search_recent_tweets, query=query,tweet_fields=['entities','created_at'],expansions=['entities.mentions.username','author_id'] ,user_fields=['username'], max_results=100).flatten(limit=200)

# count = 0
# for tweet in tweets:
    
#     if tweet.entities is not None and 'mentions' in tweet.entities:
#         if 'urls' in tweet.entities:
#             # print(tweet.entities)
            
#             print(check_if_in_db(tweet.entities['urls'][0]['expanded_url'],tweet.created_at,tweet.entities['mentions'][0]['username']))
#             if 'twitter' not in tweet.entities['urls'][0]['expanded_url'] and check_if_in_db(tweet.entities['urls'][0]['expanded_url'],tweet.created_at,tweet.entities['mentions'][0]['username']) == False:
#                 # clean_text(ascii(tweet.text))
#                 print("clear")
#                 # urls.append(tweet.entities['mentions'][0]['username'])
#                 # urls.append(tweet.entities['urls'][0]['expanded_url'])
#                 to_db(tweet.entities['urls'][0]['expanded_url'],tweet.created_at,ascii(tweet.text),query,tweet.entities['mentions'][0]['username'])
#             # if 'twitter' not in tweet.entities['urls'][0]['expanded_url'] and check_if_in_db(tweet.entities['urls'][0]['expanded_url'],tweet.created_at) == True:
#             #     # freq_update(tweet.entities['urls'][0]['expanded_url'])
#             #     print("not clear")
#             # if 'twitter' not in tweet.entities['urls'][0]['expanded_url'] and tweet.entities['urls'][0]['expanded_url'] not in urls:
#             #     # urls.append(tweet.entities['urls'][0]['expanded_url'])
#             #     # links.update({"url":tweet.entities['urls'][0]['expanded_url'], "frequency":1})
#             #     urls.append({"entry":{"url":tweet.entities['urls'][0]['expanded_url'], "frequency":1}})
#             #     count+=1
#                 # urls.append({"entry"+str(count):{"url":tweet.entities['urls'][0]['expanded_url'], "frequency":1}})

#                 # clean_text(ascii(tweet.text)
#                 # to_db(tweet.entities['urls'][0]['expanded_url'],tweet.created_at,ascii(tweet.text),query)
#             # if tweet.entities['urls'][0]['expanded_url'] in urls:
#                 # links[tweet.entities['urls'][0]['expanded_url']] += 1
#                 # freq_update(tweet.entities['urls'][0]['expanded_url'])

# # print(urls)
# # print("£------------------------------£")
# # print(links

# return urls

