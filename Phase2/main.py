from Phase1.preprocess.english_preprocessor import EnglishPreprocessor as EP
from Phase2.document_io import read_csv_file
from Phase2.svm import SVMClassifier
from Phase2.my_tfidf_vectorizer import MyTfIdfVectorizer

# dirname = os.path.dirname(__file__)
# print(os.path.join(dirname, 'source/phase2_test.csv'))

if __name__ == '__main__':
    train_data = read_csv_file('source/phase2_train.csv')
    EP().preprocess(train_data[0])
    # test_data = read_english('source/phase2_test.csv')
    #
    # tfidf_vectorizer = MyTfIdfVectorizer(train_data[0], EP())
    # svm = SVMClassifier(1, train_data, test_data, tfidf_vectorizer)
    # svm.fit()
    # svm.test()
