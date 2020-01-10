from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


class Clustering:
    """
        train_data: tuple(train_docs, train_tags)
        test_data: tuple(test_docs, test_tags)
    """
    def __init__(self, data, vectorizer, model):
        self.vectorizer = vectorizer
        self.vectors = self.vectorizer.get_vectors(data['text'])
        self.model = model
        self.is_clustered = False

    def fit(self):
        self.model.fit(self.vectors)
        self.is_clustered = True

    def predict(self, raw_docs):
        if not self.is_clustered:
            self.fit()
        vectors = self.vectorizer.get_vectors(raw_docs)
        return self.model.predict(vectors)

    def fit_predict(self):
        self.is_clustered = True
        return self.model.fit_predict(self.vectors)
