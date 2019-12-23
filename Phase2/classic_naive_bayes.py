import operator
from sklearn.metrics import classification_report


class ClassicNaiveBayesClassifier:

    """
        prior_dict: class c -> P(c)
        posterior_dict: (term t, class c) -> P(t|c)
    """
    def __init__(self, raw_train_docs, train_tags, preprocessor):
        self.prior_dict = dict()
        self.posterior_dict = dict()
        self.vocabulary = set()
        self.tags = set()
        self.preprocessor = preprocessor
        self.train_docs = self.preprocessor.preprocess(raw_train_docs)
        self.train_tags = train_tags
    """
        :arg train_docs: [
        train_class_num_dict: class c -> number of training documents associated to c
        train_doc_num: number of training documents
    """
    def __preprocess_training_set(self, train_docs, train_tags):
        self.t_ct = dict()
        self.t_c = dict()
        self.tag_num_dict = dict()
        self.tags = set(train_tags)
        self.train_num = len(train_docs)
        for i in range(self.train_num):
            doc_tokens = train_docs[i].split(' ')
            self.vocabulary.update(doc_tokens)
            for token in doc_tokens:
                if token not in self.t_ct:
                    self.t_ct[token] = dict()
                    for c in self.tags:
                        self.t_ct[token][c] = 0
                self.t_ct[token][train_tags[i]] = self.t_ct[token][train_tags[i]] + 1
            self.t_c[train_tags[i]] = self.t_c.get(train_tags[i], 0) + len(doc_tokens)
            self.tag_num_dict[train_tags[i]] = self.tag_num_dict.get(train_tags[i], 0) + 1

    def fit(self):
        self.__preprocess_training_set(self.train_docs, self.train_tags)
        for c in self.tags:
            self.prior_dict[c] = self.tag_num_dict[c] / self.train_num
        for term in self.vocabulary:
            for c in self.tags:
                self.posterior_dict[(term, c)] = (self.t_ct[term][c] + 1)/(self.t_c[c] + len(self.vocabulary))

    def predict(self, doc):
        doc = self.preprocessor.preprocess([doc])
        doc_tokens = doc[0].split(' ')
        bayes = dict()
        for c in self.tags:
            bayes[c] = self.prior_dict[c]
            for token in doc_tokens:
                bayes[c] *= self.posterior_dict.get((token, c), 1)
        return max(bayes.items(), key=operator.itemgetter(1))[0]

    def report(self, test_data):
        docs = self.preprocessor.preprocess(test_data['text'])
        predicted_tags = list()
        for doc in docs:
            predicted_tags.append(self.predict(doc))
        print(classification_report(test_data['tag'], predicted_tags))

from Phase2.preprocessor import Preprocessor
from Phase2.document_io import read_csv_file as read_english

if __name__ == '__main__':
    train_data = read_english('source/phase2_train.csv')
    test_data = read_english('source/phase2_test.csv')

    naive_bayes_classifier = ClassicNaiveBayesClassifier(train_data['text'], train_data['tag'], Preprocessor())
    naive_bayes_classifier.fit()
    naive_bayes_classifier.report(train_data)
    # print(naive_bayes_classifier.predict('sport world soccer'))
    # print(naive_bayes_classifier.predict('business business management'))
    # print(naive_bayes_classifier.predict('business business technology management'))
