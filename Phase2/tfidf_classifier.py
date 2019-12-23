from sklearn.metrics import classification_report


class TfIdfClassifier:
    """
        train_data: tuple(train_docs, train_tags)
        test_data: tuple(test_docs, test_tags)
    """
    def __init__(self, train_data, test_data, tfidf_vectorizer, model):
        self.tfidf_vectorizer = tfidf_vectorizer

        self.train_docs_sparse_matrix = self.tfidf_vectorizer.get_tfidf_vector_of_docs(train_data['text'])
        self.train_tags = train_data['tag']
        self.test_docs_sparse_matrix = self.tfidf_vectorizer.get_tfidf_vector_of_docs(test_data['text'])
        self.test_tags = test_data['tag']
        self.model = model
        self.is_learned = False

    def fit(self):
        self.model.fit(self.train_docs_sparse_matrix, self.train_tags)
        self.is_learned = True

    def predict(self, raw_doc):
        if not self.is_learned:
            self.fit()
        doc_sparse_matrix = self.tfidf_vectorizer.get_tfidf_vector(raw_doc)
        return self.model.predict(doc_sparse_matrix)

    def predict_docs(self, raw_docs):
        if not self.is_learned:
            self.fit()
        docs_sparse_matrix = self.tfidf_vectorizer.get_tfidf_vector_of_docs(raw_docs)
        return self.model.predict(docs_sparse_matrix)


    """
        raw_data: tuple(taw_docs, tags)
        if raw_data is None get report of test_data
    """
    def report(self, raw_test_data=None):
        if raw_test_data:
            sparse_matrix = self.tfidf_vectorizer.get_tfidf_vector_of_docs(raw_test_data['text'])
            tags = raw_test_data['tag']
        else:
            sparse_matrix = self.test_docs_sparse_matrix
            tags = self.test_tags
        predicted_tags = self.model.predict(sparse_matrix)
        print(classification_report(tags, predicted_tags))

