import mysql.connector
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import numpy as np
import re
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity




def custom_tokenizer(text):
    # Split on whitespace
    tokens = text.split()

    # Split strings with numbers into separate tokens
    pattern = re.compile(r'\d+')
    tokens = [token if pattern.search(token) is None else pattern.sub('', token) for token in tokens]

    return tokens


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ShadowSlash247",
    database="mydatabase"
)

query = "ukraine war"
query_words = query.split()

mycursor = mydb.cursor()
url_ids = []
for word in query_words:
    sql = "SELECT url_ids FROM inverted_index WHERE word = %s"
    val = (word,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result is not None:
        url_ids_str = result[0]
        url_ids = url_ids_str.split(',')
url_ids = list(dict.fromkeys(url_ids))
# print(url_ids)
in_params = ','.join(['%s'] * len(url_ids))
sql = "SELECT url_id,words,date FROM text_words WHERE url_id IN (%s)" % in_params
mycursor.execute(sql, url_ids)
data = mycursor.fetchall()
# print(data)
data_dict = {}
ids = []
for i in data:
    ids.append(i[0])
    # list.append(i[1])
    # dates.append({i[0]: i[2]})
    data_dict[i[0]] = {"words": i[1], "date": i[2]}
# print(list(data_dict)[0])

# terms_list = []
# start_time = time.time()
texts = []
for key, value in data_dict.items():
    doc = json.loads(value['words'])
    # if bool(re.search(r'\d', re.sub(r'\d+', '',' '.join(doc.keys())))) is True:
    #     print(key)
    # text = ' '.join(custom_tokenizer(' '.join(doc.keys())))
    texts.append(' '.join(doc.keys()))
    # terms_list.append(" ".join([term for term in doc.keys() for i in range(doc[term])]))

# print(texts[0])

# texts = custom_tokenizer(texts)
vectorizer = TfidfVectorizer(tokenizer=None)
tfidf = vectorizer.fit_transform(texts)

# perform k-means clustering
k = 5 # set the number of clusters
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(tfidf)

# calculate cosine similarity between each document and the query
query_vector = vectorizer.transform([query])
cosine_similarities = cosine_similarity(tfidf, query_vector).flatten()

# combine cosine similarities and cluster labels into a single score
for i in ids:
    scores = cosine_similarities + clusters
print(scores)

# rank documents by the combined score
# ranked_docs = sorted(list(zip(documents, scores)), key=lambda x: x[1], reverse=True)