import mysql.connector
from nltk.corpus import stopwords, wordnet as wn
from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
import re
import json
import multiprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from collections import Counter
import ast

default_stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
default_stopwords = stopwords.words('english')
tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV


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
        # return tokens
        return ' '.join([token for token in tokens])

    def lemmatization(text, lemmatizer=lemmatizer):
        # print(text)
        tokens = tokenize_text(text)
        # for token, tag in pos_tag(tokens):
        #     lemma = lemmatizer.lemmatize(token, tag_map[tag[0]])
        tokens = [lemmatizer.lemmatize(token, tag_map[tag[0]])
                     for token, tag in pos_tag(tokens)]
        # return ' '.join([token for token in tokens])
        return (tokens,' '.join([token for token in tokens]))


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
    text = text.strip(' ')  # strip whitespaces
    text = text.lower()  # lowercase
    text = text.encode('ascii', 'ignore')
    text = text.decode()

    text = remove_special_characters(text)  # remove punctuation and symbols
    text = remove_stopwords(text)  # remove stopwords
    text_tokens,lemmatized_text = lemmatization(text)[0],lemmatization(text)[1]

    return (text_tokens,lemmatized_text)


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
    hashtag_list = []
    texts = []
    # print(len(data))
    for i in data:
        ids.append(i[0])
        cleaned = clean_text(i[1])
        retweets.append(i[3])
        impressions.append(i[4])
        hashtag_list.append(i[5])
        tweets.append(cleaned[0])
        texts.append(cleaned[1])

    docs_list = []

    sentiment_scores = {}
 
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
    cosine_weight = 0.5
    retweet_weight = 0.6
    impression_weight = 0.7

    # calculate scores of each tweet and then remapping them to their tweet id
    scores = [cosine_weight * cosine_similarities[i] + retweet_weight * retweets[i] + impression_weight * impressions[i]
              for i in range(len(tweets))]

    tweet_scores = dict(zip(ids, scores))

    # sort final list of tweets by their score and return the top 10
    ranked_tweet_ids = sorted(tweet_scores, key=tweet_scores.get, reverse=True)
    ranked_tweets = []
    hashtags = get_hashtags(hashtag_list)
    for i in data:
        for j in ranked_tweet_ids:
            if i[0] == j:
                ranked_tweets.append(
                    {"id": i[0], "url": f"https://twitter.com/anyuser/status/{i[0]}", "tweet": i[1], "date": i[2],
                     "retweets": i[3], "impressions": i[4], "sentiment": sentiment_scores.get(i[0])})

    # for i in range(10):
    #     return ranked_tweet_ids[i]
    topics = topic_modelling(tweets)
    return [topics, ranked_tweets[0:10], average_compound_score, hashtags]


def get_hashtags(hashtag_list):
    hashtag_list = [ast.literal_eval(hlist) for hlist in hashtag_list]
    hashtags = [tag for tag_list in hashtag_list if tag_list for tag in tag_list]

    tag_count = Counter(hashtags)
    top_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:5]
    top_5_tags = ['#'+tag[0] for tag in top_tags]
    # print(top_5_tags)
    return top_5_tags


def calculate_tfidf_and_cosine_similarity(docs_list, query):
    # initialize the vectorizer and calculate the tfidf of every document(tweet)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs_list)
    
    # calculate query tfidf
    query_tfidf = vectorizer.transform([query])

    # calculate cosine_similarities for every document(tweet) in relation to the query
    cosine_similarities = cosine_similarity(tfidf_matrix, query_tfidf)
    return cosine_similarities


def sentiment_analysis(doc):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(" ".join(doc))
    return score


def process_chunk(chunk):
    tweet_dictionary = Dictionary(chunk)
    tweet_bow_corpus = [tweet_dictionary.doc2bow(tweet) for tweet in chunk]
    lda_model = LdaModel(corpus=tweet_bow_corpus,
                         id2word=tweet_dictionary,
                         num_topics=5,
                         random_state=42,
                         passes=5,
                         per_word_topics=True)
    topics = {}
    for topic_id in range(5):
        top_words = [word[0] for word in lda_model.show_topic(topic_id, topn=10)]
        for word in top_words:
            if word in topics:
                topics[word] += 1
            else:
                topics[word] = 1
    return topics

def topic_modelling(tweets):
    num_processes = multiprocessing.cpu_count() - 1
    chunk_size = int(len(tweets) / num_processes) + 1
    tweet_chunks = [tweets[i:i + chunk_size] for i in range(0, len(tweets), chunk_size)]
    pool = multiprocessing.Pool(processes=num_processes)
    results = pool.map(process_chunk, tweet_chunks)
    topics = {}
    for result in results:
        for key, value in result.items():
            if key in topics:
                topics[key] += value
            else:
                topics[key] = value
    topics_vals = [{'text': key, 'value': value} for key, value in topics.items()]
    return topics_vals

# print(get_tweets(392919, 'turkey'))
