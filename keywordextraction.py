# import nltk
# from nltk.corpus import twitter_samples
# from nltk.probability import FreqDist
# from nltk.tokenize import word_tokenize

# # Load tweets
# tweets = twitter_samples.strings('tweets.20150430-223406.json')

# # Tokenize tweets
# tweet_tokens = [word_tokenize(tweet) for tweet in tweets]

# # Extract keywords using NLTK's built-in stopwords
# stopwords = nltk.corpus.stopwords.words('english')
# keywords = []
# for tweet_tokens in tweet_tokens:
#     keywords.extend([word for word in tweet_tokens if word.lower() not in stopwords])

# # Find the most common keywords
# fdist = FreqDist(keywords)
# top_keywords = fdist.most_common(20)
# print(top_keywords)
