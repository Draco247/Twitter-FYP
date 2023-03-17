import mysql.connector
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string
# import nltk
from nltk.stem import PorterStemmer
import re
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import numpy as np
# import gensim
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel

default_stemmer = PorterStemmer()
default_stopwords = stopwords.words('english')


# function to clean text of tweets for analysis
def clean_text(text):
    def remove_link(text):
        if "http" in text:
            text = re.sub(r'http\S+', '', text).strip()
        return text

    def tokenize_text(text):
        return [w for s in sent_tokenize(text) for w in word_tokenize(s)]

    def remove_special_characters(text,
                                  characters=string.punctuation.replace('!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n', ' ')):
        tokens = tokenize_text(text)
        pattern = re.compile('[{}]'.format(re.escape(characters)))
        return ' '.join(filter(None, [pattern.sub('', t) for t in tokens]))

    def stem_text(text, stemmer=default_stemmer):
        tokens = tokenize_text(text)
        return ' '.join([stemmer.stem(t) for t in tokens])

    def remove_stopwords(text, stop_words=default_stopwords):
        tokens = [w for w in tokenize_text(text) if w not in stop_words]
        return tokens

    def convert(text):
        dict = {}
        for i in text.split():
            # print(f"i is hello: {i}")
            if i in dict:
                dict.update({i: dict[i] + 1})
            else:
                dict[i] = 1
        json_object = json.dumps(dict, indent=4)
        return json_object

    text = remove_link(text)
    # print(text)
    # print("------------------")
    text = text.strip(' ')  # strip whitespaces
    text = text.lower()  # lowercase
    text = text.encode('ascii', 'ignore')
    text = text.decode()

    # text = stem_text(text) # stemming
    text = remove_special_characters(text)  # remove punctuation and symbols
    text = remove_stopwords(text)  # remove stopwords
    # print(f"text is here {text}")
    # text_dict = convert(text)
    # text.strip(' ') # strip whitespaces again?

    return text


def get_tweets(url_id, query):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ShadowSlash247",
        database="mydatabase"
    )
    curr = conn.cursor()

    # get all tweets that use the specified url
    sql = "SELECT tweet_id, tweet, created_at, retweets, impressions, hashtags FROM tweettest4 WHERE url_id = (%s)"
    curr.execute(sql, (url_id,))
    data = curr.fetchall()
    # print(ascii(data))
    tweets = []
    ids = []
    retweets = []
    impressions = []
    # print(len(data))
    for i in data:
        ids.append(i[0])
        cleaned = clean_text(i[1])
        retweets.append(i[3])
        impressions.append(i[4])
        tweets.append(cleaned)
    # print(tweets)
    # print(len(tweets))

    docs_list = []
    
    sentiment_scores = {}
    # print(ascii(tweets))
    # print("-apple-")
    count = 0
    for doc in tweets:
        score = sentiment_analysis(doc)
        sentiment_scores[ids[count]] = score
        docs_list.append(" ".join(doc))
        count += 1
    # print(sentiment_scores)
    compound_sum = 0
    for i in sentiment_scores.values():
        compound_sum += i['compound']

    average_compound_score = compound_sum / len(sentiment_scores)

    cosine_similarities = calculate_tfidf_and_cosine_similarity(docs_list, query)

    # setting weights for each variable used in ranking the tweets
    cosine_weight = 0.7
    retweet_weight = 0.3
    impression_weight = 0.2

    # calculate scores of each tweet and then remapping them to their tweet id
    scores = [cosine_weight * cosine_similarities[i] + retweet_weight * retweets[i] + impression_weight * impressions[i]
              for i in range(len(tweets))]
    # print(scores)
    tweet_scores = dict(zip(ids, scores))
    # for tweet_id, score in tweet_scores.items():
    #     print(tweet_id, score)

    # sort final list of tweets by their score and return the top 10
    ranked_tweet_ids = sorted(tweet_scores, key=tweet_scores.get, reverse=True)
    ranked_tweets = []
    for i in data:
        for j in ranked_tweet_ids:
            if i[0] == j:
                ranked_tweets.append(
                    {"id": i[0], "url": f"https://twitter.com/anyuser/status/{i[0]}", "tweet": i[1], "date": i[2],
                     "retweets": i[3], "impressions": i[4], "sentiment":sentiment_scores.get(i[0])})

    # for i in range(10):
    #     return ranked_tweet_ids[i]
    topics = topic_modelling(tweets)
    return [topics,ranked_tweets[0:10],average_compound_score]

def calculate_tfidf_and_cosine_similarity(docs_list, query):
    # initialize the vectorizer and calculate the tfidf of every document(tweet)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs_list)
    # print(tfidf_matrix)
    # query = 'This is the second document.'
    # calculate query tfidf
    query_tfidf = vectorizer.transform([query])
    # print(query_tfidf)
    # calculate cosine_similarities for every document(tweet) in relation to the query
    cosine_similarities = cosine_similarity(tfidf_matrix, query_tfidf)
    return cosine_similarities

def sentiment_analysis(doc):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(" ".join(doc))
    return score
    # sentiment_scores.append({ids[count]: score})
    # count = 0
    # for doc in tweets:
    #     score = analyzer.polarity_scores(" ".join(doc))
    #     sentiment_scores.append({ids[count]: score})
    #     docs_list.append(" ".join(doc))
    #     count += 1


def topic_modelling(tweets):
    tweet_dictionary = Dictionary(tweets)
    print(tweet_dictionary)
    tweet_bow_corpus = [tweet_dictionary.doc2bow(tweet) for tweet in pd.Series(tweets)]
    lda_model = LdaModel(corpus=tweet_bow_corpus,
                         id2word=tweet_dictionary,
                         num_topics=5,
                         random_state=42,
                         passes=10,
                         per_word_topics=True)
    # Print the top 10 words for each of the 5 topics
    topics = {}
    for topic_id in range(5):
        for word in lda_model.show_topic(topic_id, topn=10):
            # print(word)
            if word[0] in topics:
                topics[word[0]] = topics.get(word[0])+1
            else:
                topics[word[0]] = 1
        # topics[topic_id] = " ".join(word[0] for word in lda_model.show_topic(topic_id, topn=10))
        # return (f'Topic {topic_id}: {" ".join(word[0] for word in lda_model.show_topic(topic_id, topn=10))}')
    # print(topics)
    topics_vals = [{'text': key, 'value': value} for key, value in topics.items()]
    return topics_vals


# print(get_tweets(392919, 'turkey'))
