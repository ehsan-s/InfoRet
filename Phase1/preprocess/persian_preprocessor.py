import re
import unicodedata
import hazm
import inflect
import nltk
from hazm import Stemmer

from Phase1.preprocess import document_io


class PersianPreprocessor:

    def __init__(self):
        self.stemmer = Stemmer()
        self.processed_list = None
        self.high_accur_param = 10000
        self.dictionary = None

    def preprocess(self, persian_list=None):
        """

        :param eng_list: [(title, text)]
        :return:
        """
        normalized_list = []
        if persian_list is None:
            persian_list = self.persian_list
        for news in persian_list:
            ntext = self.normalize_doc(news)
            normalized_list.append(ntext)
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
        return hazm.word_tokenize(doc_str)

    def normalize(self, word):
        word = self.remove_punctuation(word)
        word = self.stem(word)
        return word

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

    def get_high_accurance(self):
        accurance_dict = self.get_accurance_dict()
        accurance_dict = reversed(sorted(accurance_dict.items(), key=lambda x: x[1]))
        result_dict = []
        for (k, v) in accurance_dict:
            if v >= self.high_accur_param:
                result_dict.append((k, v))
        return result_dict

    def remove_high_accured_words(self):
        accurance_dict = self.get_accurance_dict()
        high_accur_words = set()
        for (k, v) in accurance_dict.items():
            if v >= self.high_accur_param:
                high_accur_words.add(k)
        # print(high_accur_words)
        updated_processed_list = []
        for news in self.processed_list:
            updated_news = []
            words = news.split()
            for word in words:
                if word not in high_accur_words:
                    updated_news.append(word)
            updated_processed_list.append(' '.join(updated_news))
        self.processed_list = updated_processed_list
        return self.processed_list


prerprocessor = PersianPreprocessor()
prerprocessor.preprocess()
print(prerprocessor.remove_punctuation(''))
prerprocessor.sort_by_accurance()
# hazm.Normalizer().normalize()
# print(prerprocessor.remove_high_accured_words())
