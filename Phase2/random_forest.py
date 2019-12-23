from sklearn.ensemble import RandomForestClassifier

from Phase2.tfidf_classifier import TfIdfClassifier
from Phase2.document_io import read_csv_file as read_english
from Phase2.my_tfidf_vectorizer import MyTfIdfVectorizer
from Phase2.preprocessor import Preprocessor

if __name__ == '__main__':
    train_data = read_english('source/phase2_train.csv')
    test_data = read_english('source/phase2_test.csv')

    tfidf_vectorizer = MyTfIdfVectorizer(train_data['text'], Preprocessor())
    rfc = TfIdfClassifier(train_data, test_data, tfidf_vectorizer, RandomForestClassifier())
    rfc.fit()
    rfc.report()
    rfc.report(train_data)
    # print(rfc.predict('sport world soccer'))
    # print(rfc.predict('business business management'))
    # print(rfc.predict('business business technology management'))
