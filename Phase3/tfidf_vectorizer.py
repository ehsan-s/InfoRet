from Phase2.my_tfidf_vectorizer import MyTfIdfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


class TfIdfVectorizer(MyTfIdfVectorizer):
    def __init__(self, raw_docs, preprocessor):
        self.name = 'tfidf'
        self.preprocessor = preprocessor
        # train_docs = preprocessor.preprocess(raw_docs)
        self.vectorizer = TfidfVectorizer(max_df=0.85, max_features=1000)
        self.vectorizer.fit(raw_docs)

    def get_vectors(self, raw_docs):
        # docs = self.preprocessor.preprocess(raw_docs)
        return self.vectorizer.transform(raw_docs).toarray()
