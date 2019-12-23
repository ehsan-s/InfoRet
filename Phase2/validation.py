from Phase2.tfidf_classifier import TfIdfClassifier
from Phase2.document_io import read_csv_file as read_english
from Phase2.my_tfidf_vectorizer import MyTfIdfVectorizer
from Phase2.preprocessor import Preprocessor
from Phase2.knn import KNN
from sklearn.svm import LinearSVC
import numpy as np


def validation(model, parameters_list, validation_ratio=.1):
    """

    :param model: can be "svm" or "knn"
    :param parameters_list: list of parameters
    :param validation_ratio: ratio of data for validation
    :return:
    """
    train_data = read_english('source/phase2_train.csv')
    tfidf_vectorizer = MyTfIdfVectorizer(train_data['text'], Preprocessor())
    n_samples = len(train_data['text'])
    validation_samples = np.random.choice(n_samples, int(validation_ratio * n_samples), replace=False)
    mask = np.ones(n_samples, dtype=bool)
    mask[validation_samples] = False
    new_train = {}
    validation = {}
    new_train['text'] = list(np.array(train_data['text'])[mask])
    new_train['tag'] = list(np.array(train_data['tag'])[mask])
    validation['text'] = list(np.array(train_data['text'])[validation_samples])
    validation['tag'] = list(np.array(train_data['tag'])[validation_samples])
    classifier = TfIdfClassifier(new_train, validation, tfidf_vectorizer)
    for parameter in parameters_list:
        if model == "svm":
            new_model = LinearSVC(C=parameter)
        elif model == 'knn':
            new_model = KNN(n_neighbours=parameter)

        classifier.model = new_model
        classifier.fit()
        print("parameter: {}".format(parameter))
        classifier.report()


if __name__ == '__main__':
    # SVM
    print("SVM")
    validation("svm", parameters_list=[.5, 1, 1.5, 2])
    print("######################################")
    print("KNN")
    validation("knn", parameters_list=[1, 5, 9])
