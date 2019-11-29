import re
import unicodedata

import nltk
from nltk.stem import PorterStemmer

from Phase1.preprocess import document_io


class EnglishPreprocessor:

    def __init__(self):
        self.eng_list = document_io.read_csv_file_as_list()
        self.stemmer = PorterStemmer()
        self.processed_list = None
        self.high_accur_param = 125
        self.dictionary = None

    def preprocess(self):
        normalized_list = []
        for news in self.eng_list:
            ntitle = self.normalize_doc(news[0])
            ntext = self.normalize_doc(news[1])

            normalized_list.append([ntitle, ntext])
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
        return normalized_words

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
        return unicodedata.normalize('NFKD', word)\
            .encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def lower(self, word):
        return word.lower()

    def remove_punctuation(self, word):
        return re.sub(r'[^\w\s]', '', word)

    def stem(self, word):
        return self.stemmer.stem(word)

    def make_dictionary(self):
        dictionary = set()
        for news in self.processed_list:
            for new in news:
                for word in new:
                    dictionary.add(word)
        return dictionary

    def get_accurance_dict(self):
        accurance_dict = {}
        for news in self.processed_list:
            for new in news:
                for word in new:
                    accurance_dict[word] = accurance_dict.get(word, 0) + 1
        return accurance_dict

    def sort_by_accurance(self):
        accurance_dict = self.get_accurance_dict()
        accurance_dict = reversed(sorted(accurance_dict.items(), key=lambda x: x[1]))
        for (k,v) in accurance_dict:
            print(k, " : ", v)

    def remove_high_accured_words(self):
        accurance_dict = self.get_accurance_dict()
        high_accur_words = []
        for k,v in accurance_dict.items():
            if v >= self.high_accur_param:
                high_accur_words.append(k)
        #print(high_accur_words)
        updated_processed_list = []
        for news in self.processed_list:
            tuple = []
            for new in news:
                tuple.append(list(filter(lambda a: a not in high_accur_words, new)))
            updated_processed_list.append(tuple)
        self.processed_list = updated_processed_list
        return self.processed_list


prerprocessor = EnglishPreprocessor()
prerprocessor.preprocess()
# prerprocessor.sort_by_accurance()
print(prerprocessor.remove_high_accured_words())