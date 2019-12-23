from sklearn.svm import LinearSVC

from Phase2.tfidf_classifier import TfIdfClassifier
from Phase2.document_io import read_csv_file as read_english
from Phase2.my_tfidf_vectorizer import MyTfIdfVectorizer
from Phase2.preprocessor import Preprocessor

if __name__ == '__main__':
    train_data = read_english('source/phase2_train.csv')
    test_data = read_english('source/phase2_test.csv')

    tfidf_vectorizer = MyTfIdfVectorizer(train_data['text'], Preprocessor())
    c = 1
    svm = TfIdfClassifier(train_data, test_data, tfidf_vectorizer, LinearSVC(C=c))
    svm.fit()
    svm.report()
    print(svm.predict('sport world soccer'))
    print(svm.predict('business business management'))
    print(svm.predict('business business technology management'))
