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


client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_secret, access_token=access_token, access_token_secret=access_secret, wait_on_rate_limit=True)

mycursor = mydb.cursor()
# with open('mydata.json') as f:
#     user_mapping = json.load(f)
# user_mapping = {k: v for d in user_mapping for k, v in d.items()}

# # print(user_mapping)
# # print(data)
# sql = "SELECT tweettest4.url_id, COUNT(*) as frequency FROM tweettest4 WHERE url_id IS NOT NULL GROUP BY tweettest4.url_id"
# mycursor.execute(sql)
# data2 = mycursor.fetchall()
# # print(ascii(data2))
# url_frequency_by_user = {}

# for row in data2:
#     url_id = row[0]
#     frequency = 0
#     # get the tweet_ids for the current URL
#     tweet_ids = []
#     mycursor.execute('SELECT tweet_id FROM tweettest4 WHERE url_id = %s', (url_id,))
#     for tweet in mycursor:
#         tweet_ids.append(tweet[0])
#     # iterate over the tweet_ids and add the frequency to the appropriate user
#     checked_users = []
#     for tweet_id in tweet_ids:
#         user_id = user_mapping.get(str(tweet_id), None) # get the user_id for the current tweet_id
#         if user_id:
#             if user_id not in checked_users:
#                 frequency += 1
#                 checked_users.append(user_id)
#             # if url_id == 394107:
#             #     print(user_id)
#             # increment the frequency for the current URL and user
#             # url_frequency_by_user.setdefault(user_id, {}).setdefault(url_id, 0)
#             # url_frequency_by_user[user_id][url_id] += frequency
#     # if url_id == 394107:
#     #     print(f"{url_id} used {frequency} times")
#     url_frequency_by_user[url_id] = frequency
# # print(url_frequency_by_user)
# # max_value = max(url_frequency_by_user.values())

# for id,freq in url_frequency_by_user.items():
#    #  print(f"{id} used {freq} times")
#    sql = "UPDATE urltest SET frequency = %s WHERE url_id = %s"
#    val = (freq, id)
#    mycursor.execute(sql, val)
# mydb.commit()

# print(max_value)

# close database connection
# conn.close()

# print the results
# for user_id, url_frequencies in url_frequency_by_user.items():
#     print(f'User {user_id} used the following URLs with their respective frequencies:')
#     for url_id, frequency in url_frequencies.items():
#         print(f'    URL {url_id}: {frequency} times')
# new_dict = {k: v for d in data for k, v in d.items()}

# # print(new_dict)
# # Create a set to hold unique values
# unique_values = set()

# # Iterate over the values in the dictionary and add unique values to the set
# for value in new_dict.values():
#     unique_values.add(value)

# # Convert the set to a list
# unique_values_list = list(unique_values)
# count = {}

# for i in data2:
    
# print(len(unique_values_list))
# tweet_ids = []
# user_ids = []    
# for dictionary in data:
#     tweet_ids.extend(dictionary.keys())
#     user_ids.extend(dictionary.values())

# print(len(user_ids))
# values = list(set(user_ids))
# print(len(values))

# sql = "SELECT tweet_id FROM tweettest4"
# mycursor.execute(sql)
# data = mycursor.fetchall()
# tweet_ids = [i[0] for i in data]
# print(tweet_ids)

# user_ids = []
# for i in range(0, len(tweet_ids), 100):
#    group = tweet_ids[i:i+100]
#    count = 0
# #    print(len(group))
#    print(f"group {i} to {i+100}")
#    tweets = client.get_tweets(group,expansions='author_id')
#    print(ascii(tweets))
#    for tweet in tweets.data:
#     # print(f"group {tweet.id}")
#     # print(f"author {tweet.author_id}")
#     user_ids.append({tweet.id:tweet.author_id})
#     #   print(count)
#     #   if tweet.author_id != None:
#     #     print(f"group {group[count]}")
#     #     print(f"author {tweet.author_id}")
#     #     user_ids.append(tweet.author_id)
#     count += 1
      
#    print("--------------------")
# #    print(len(group))
# #    print(len(user_ids))
# # print(user_ids)
# with open("mydata.json", "w") as final:
#    json.dump(user_ids, final,indent =2)
# tweets = client.get_tweets(tweet_ids[0:101],expansions='author_id')
# print(ascii(tweets))
# for tweet in tweets:
#     print(ascii(tweet))

# for response in tweepy.Paginator(client.get_tweets, tweet_ids,
#                                     max_results=1000, limit=5):
#     print(response.meta)
    
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

def url_id(url):
    mycursor = mydb.cursor()
    val = ([url])
    sql = "SELECT EXISTS(SELECT * from urltest WHERE url=%s)"
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    mycursor.close()
    if data == 0:
        mycursor = mydb.cursor()
        sql = "INSERT INTO urltest (url) VALUES (%s)"
        val = ([url])
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        sql = "UPDATE "

    return data

tweets = tweepy.Paginator(client.search_recent_tweets, query=search,tweet_fields=['entities','created_at','public_metrics'], expansions='author_id', max_results=100).flatten(limit=500000)
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
                user_id = tweet.author_id
                print(tweet.author_id)
                url_id(url)
                # mycursor = mydb.cursor()
                # sql = "INSERT INTO tweets (url,created_at,tweet,query,retweets,impressions, tweet_id,user_id, hashtags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                # val = ([url,created_at,content,query,retweets,impressions,tweet_id, user_id, json.dumps(hashtags)])
                # # sql = "INSERT INTO tweets (url,title,description,created_at,tweet,query,retweets,impressions, tweet_id, hashtags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                # # val = ([url,title,description,created_at,content,query,retweets,impressions,tweet_id, json.dumps(hashtags)])
                # mycursor.execute(sql, val)
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

