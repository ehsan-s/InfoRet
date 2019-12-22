from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC


class SVMClassifier:

    """
        train_data: tuple(train_docs, train_tags)
        test_data: tuple(test_docs, test_tags)
    """
    def __init__(self, c, train_data, test_data, tfidf_vectorizer):
        self.tfidf_vectorizer = tfidf_vectorizer

        self.train_docs_sparse_matrix = self.tfidf_vectorizer.get_tfidf_vector_of_docs(train_data[0])
        self.train_tags = train_data[1]
        self.test_docs_sparse_matrix = self.tfidf_vectorizer.get_tfidf_vector_of_docs(test_data[0])
        self.test_tags = test_data[1]
        self.svc = LinearSVC(C=c)
        self.is_learned = False

    def test(self):
        predicted_tags = self.svc.predict(self.test_docs_sparse_matrix)
        print(classification_report(self.test_tags, predicted_tags))

    def classify(self):
        self.svc.fit(self.train_docs_sparse_matrix, self.train_tags)
        self.is_learned = True

    def predict(self, raw_doc):
        if not self.is_learned:
            self.classify()
        doc_sparse_matrix = self.tfidf_vectorizer.get_tfidf_vector(raw_doc)
        return self.svc.predict(doc_sparse_matrix)


from Phase1.preprocess.english_preprocessor import EnglishPreprocessor as EP
from Phase2.document_io import read_csv_file as read_english
from Phase2.my_tfidf_vectorizer import MyTfIdfVectorizer

if __name__ == '__main__':
    train_data = read_english('source/phase2_train.csv')
    test_data = read_english('source/phase2_test.csv')

    tfidf_vectorizer = MyTfIdfVectorizer(train_data[0], EP())
    svm = SVMClassifier(1, train_data, test_data, tfidf_vectorizer)
    svm.classify()
    svm.test()
    print(svm.predict('sport world soccer'))
    print(svm.predict('business business management'))
    print(svm.predict('business business technology management'))
