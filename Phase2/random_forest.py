from sklearn.ensemble import RandomForestClassifier as RFClassifier
from sklearn.metrics import classification_report


class RandomForestClassifier:
    """
        train_data: tuple(train_docs, train_tags)
        test_data: tuple(test_docs, test_tags)
    """
    def __init__(self, train_data, test_data, tfidf_vectorizer):
        self.tfidf_vectorizer = tfidf_vectorizer

        self.train_docs_sparse_matrix = self.tfidf_vectorizer.get_tfidf_vector_of_docs(train_data[0])
        self.train_tags = train_data[1]
        self.test_docs_sparse_matrix = self.tfidf_vectorizer.get_tfidf_vector_of_docs(test_data[0])
        self.test_tags = test_data[1]
        self.model = RFClassifier()
        self.is_learned = False

    def test(self):
        predicted_tags = self.model.predict(self.test_docs_sparse_matrix)
        print(classification_report(self.test_tags, predicted_tags))

    def classify(self):
        self.model.fit(self.train_docs_sparse_matrix, self.train_tags)
        self.is_learned = True

    def predict(self, raw_doc):
        if not self.is_learned:
            self.classify()
        doc_sparse_matrix = self.tfidf_vectorizer.get_tfidf_vector(raw_doc)
        return self.model.predict(doc_sparse_matrix)


from Phase2.preprocessor import Preprocessor
from Phase2.document_io import read_csv_file as read_english
from Phase2.my_tfidf_vectorizer import MyTfIdfVectorizer

if __name__ == '__main__':
    train_data = read_english('source/phase2_train.csv')
    test_data = read_english('source/phase2_test.csv')

    tfidf_vectorizer = MyTfIdfVectorizer(train_data[0], Preprocessor())
    rfc = RandomForestClassifier(train_data, test_data, tfidf_vectorizer)
    rfc.classify()
    rfc.test()
    print(rfc.predict('sport world soccer'))
    print(rfc.predict('business business management'))
    print(rfc.predict('business business technology management'))
