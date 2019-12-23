import numpy as np
from sklearn.metrics import pairwise_distances
from collections import Counter


class KNN:
    def __init__(self, n_neighbours):
        self.k = n_neighbours
        self.train_X = None
        self.train_y = None
        self.n_features = None

    def fit(self, X, y):
        self.train_X = X
        self.train_y = np.asarray(y)
        self.n_features = X.shape[1]

    def predict(self, X):
        n_samples = X.shape[0]
        # TODO may change dtype
        predictions = np.empty((n_samples, ),
                               dtype=int)
        dist = pairwise_distances(X, self.train_X)
        for i, row in enumerate(dist):
            knn_indices = np.argsort(row)[0:self.k]
            pr_tag = Counter(self.train_y[knn_indices]).most_common(1)[0][0]
            predictions[i] = pr_tag

        return predictions


if __name__ == '__main__':
    from Phase2.tfidf_classifier import TfIdfClassifier
    from Phase2.document_io import read_csv_file as read_english
    from Phase2.my_tfidf_vectorizer import MyTfIdfVectorizer
    from Phase2.preprocessor import Preprocessor
    train_data = read_english('source/phase2_train.csv')
    test_data = read_english('source/phase2_test.csv')

    tfidf_vectorizer = MyTfIdfVectorizer(train_data['text'], Preprocessor())
    knn = TfIdfClassifier(train_data, test_data, tfidf_vectorizer, KNN(5))
    knn.fit()
    knn.report()


