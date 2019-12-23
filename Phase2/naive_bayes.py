from scipy.stats import norm


class NaiveBayesClassifier:

    """
        prior_dict: class c -> P(c)
        posterior_dict: (term t, class c) -> P(t|c)
    """
    def __init__(self):
        self.prior_dict = dict()
        self.gaussian_likelihood = dict()
        self.tags = set()

    def fit(self, doc_sparse_matrix, tags):
        self.__fit_gaussian_for_term_tag(doc_sparse_matrix, tags)
        self.__evaluate_prior(tags)

    def predict(self, doc_sparse_matrix):
        doc_size = doc_sparse_matrix.shape[0]
        predicted_tags = []

        for i in range(doc_size):
            predicted_tag = None
            c_map = 0.0
            for (c, prior) in self.prior_dict.items():
                posterior = prior
                col_list = doc_sparse_matrix.getrow(i).nonzero()[1]
                for term_ind in col_list:
                    (mu, std) = self.gaussian_likelihood[term_ind][c]
                    posterior *= norm(mu, std).pdf(doc_sparse_matrix[i, term_ind])
                if posterior > c_map:
                    c_map = posterior
                    predicted_tag = c
            predicted_tags.append(predicted_tag)
        return predicted_tags

    def __fit_gaussian_for_term_tag(self, doc_sparse_matrix, tags):
        features_size = doc_sparse_matrix.shape[1]
        for term_ind in range(features_size):
            term_sparse_matrix = doc_sparse_matrix.getcol(term_ind)
            class_tfidf_dict = self.__get_class_tfidf_dict(term_sparse_matrix, tags)
            class_likelihhood_dict = dict()
            for tag, tfidf_list in class_tfidf_dict.items():
                mu, std = norm.fit(tfidf_list)
                class_likelihhood_dict[tag] = tuple(mu, std)
            self.gaussian_likelihood[term_ind] = class_likelihhood_dict

    def __evaluate_prior(self, tags):
        for c in tags:
            self.prior_dict[c] = tags.count(c) / len(tags)

    """
        :arg term_sparse_matrix
            a column sparse matrix of this term
        :arg tags
            tags associated to the sparse_matrix documents

        :return
        keys of dict are tags
        values of dict are tf-idf list of terms associated to the tag
        { tag_1 : [tf-idf list],
          tag_2 : [tf-idf list],
          ...}  
    """
    def __get_class_tfidf_dict(self, term_sparse_matrix, tags):
        class_tfidf_dict = dict()
        nonzero_row_indices = term_sparse_matrix.nonzero()[0]
        for row_ind in nonzero_row_indices:
            tag = tags[row_ind]
            if tag not in class_tfidf_dict:
                class_tfidf_dict[tag] = list()
            class_tfidf_dict[tag].append(term_sparse_matrix[row_ind, 0])
        return class_tfidf_dict


from Phase2.preprocessor import Preprocessor
from Phase2.tfidf_classifier import TfIdfClassifier
from Phase2.document_io import read_csv_file as read_english
from Phase2.my_tfidf_vectorizer import MyTfIdfVectorizer

if __name__ == '__main__':
    train_data = read_english('source/phase2_train.csv')
    test_data = read_english('source/phase2_test.csv')

    tfidf_vectorizer = MyTfIdfVectorizer(train_data['text'], Preprocessor())
    sparse = tfidf_vectorizer.get_tfidf_vector_of_docs(train_data['text'])
    print('0 data:', sparse.getcol(0).data)
    naive_bayes_classifier = TfIdfClassifier(train_data, test_data, tfidf_vectorizer, NaiveBayesClassifier())
    naive_bayes_classifier.fit()
    # naive_bayes_classifier.report()
    # print(naive_bayes_classifier.predict('sport world soccer'))
    # print(naive_bayes_classifier.predict('business business management'))
    # print(naive_bayes_classifier.predict('business business technology management'))
