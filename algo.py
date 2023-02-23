# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import PorterStemmer
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np

# nltk.download("stopwords")
# nltk.download("punkt")

def rank_documents(query, documents, num_results=5):
    # Tokenize and stem the query and documents
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    query = [stemmer.stem(w) for w in word_tokenize(query) if w not in stop_words]
    query = " ".join(query)
    documents = [
        " ".join([stemmer.stem(w) for w in word_tokenize(doc) if w not in stop_words])
        for doc in documents
    ]
    # Compute TF-IDF scores
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([query] + documents)
    query_tfidf = tfidf_matrix[0]
    document_tfidfs = tfidf_matrix[1:]
    # Compute cosine similarities
    cosine_similarities = np.dot(document_tfidfs, query_tfidf.T).flatten()
    # Rank documents by cosine similarity
    ranked_indices = np.argsort(-cosine_similarities)
    # Return top N results
    return [documents[i] for i in ranked_indices[:num_results]]
