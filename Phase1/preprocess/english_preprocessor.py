import re
import unicodedata

import nltk
from nltk.stem import PorterStemmer


class EnglishPreprocessor:

    def __init__(self):
        self.stemmer = PorterStemmer()
        self.processed_list = None
        self.high_accur_param = 125
        self.dictionary = None

    def preprocess(self, eng_list):
        """

        :param eng_list: [(title, text)]
        :return:
        """
        normalized_list = []
        for news in eng_list:
            text = self.normalize_doc(news)
            normalized_list.append(text)
        self.processed_list = normalized_list
        self.remove_high_accured_words()
        self.dictionary = self.make_dictionary()
        return normalized_list

    def normalize_doc(self, doc):
        normalized_words = []
        for word in self.get_word_by_word(doc):
            nword = self.normalize(word)
            if nword is not None and nword != '':
                normalized_words.append(nword)
        return ' '.join(normalized_words)

    def get_word_by_word(self, doc_str):
        words = self.tokenize(doc_str)
        for word in words:
            yield word

    def tokenize(self, doc_str):
        return nltk.word_tokenize(doc_str)

    def normalize(self, word):
        word = self.remove_non_ascii(word)
        word = self.lower(word)
        word = self.remove_punctuation(word)
        word = self.stem(word)
        return word

    def remove_non_ascii(self, word):
        return unicodedata.normalize('NFKD', word) \
            .encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def lower(self, word):
        return word.lower()

    def remove_punctuation(self, word):
        return re.sub(r'[^\w\s]', '', word)

    def stem(self, word):
        return self.stemmer.stem(word)

    def make_dictionary(self):
        dictionary = list()
        for news in self.processed_list:
            words = news.split()
            dictionary.extend(words)
        return set(dictionary)

    def get_accurance_dict(self):
        accurance_dict = {}
        for news in self.processed_list:
            words = news.split()
            for word in words:
                accurance_dict[word] = accurance_dict.get(word, 0) + 1
        return accurance_dict

    def sort_by_accurance(self, param=None):
        if param is None:
            param = self.high_accur_param
        accurance_dict = self.get_accurance_dict()
        accurance_dict = reversed(sorted(accurance_dict.items(), key=lambda x: x[1]))
        return list(accurance_dict)[0:param]
        # print(k, " : ", v)

    def remove_high_accured_words(self):
        accurance_dict = self.get_accurance_dict()
        high_accur_words = set()
        for k, v in accurance_dict.items():
            if v >= self.high_accur_param:
                high_accur_words.add(k)
        # print(high_accur_words)
        updated_processed_list = []
        for news in self.processed_list:
            words = news.split()
            for word in words:
                if word not in high_accur_words:
                    updated_processed_list.append(word)
        self.processed_list = ' '.join(updated_processed_list)
        return self.processed_list


prerprocessor = EnglishPreprocessor()
prerprocessor.preprocess()
# prerprocessor.sort_by_accurance()
print(prerprocessor.remove_high_accured_words())
