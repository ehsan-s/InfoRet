import re
import unicodedata
from Phase1.preprocess.generic_preprocessor import GenericPreprocessor
import nltk
from nltk.stem import PorterStemmer


class EnglishPreprocessor(GenericPreprocessor):

    def __init__(self):
        self.stemmer = PorterStemmer()
        self.high_accur_param = 110
        self.must_be_words = ['reuters']

    def tokenize(self, doc_str):
        return nltk.word_tokenize(doc_str)

    def normalize(self, text):
        text = self.remove_non_ascii(text)
        text = self.remove_punctuation(text)
        text = self.lower(text)
        text = re.sub(' +', ' ', text.strip())
        return text

    def stem(self, word):
        word = self.stemmer.stem(word)
        word = re.sub(' +', ' ', word.strip())
        return word

    @staticmethod
    def remove_non_ascii(word):
        return unicodedata.normalize('NFKD', word) \
            .encode('ascii', 'ignore').decode('utf-8', 'ignore')

    @staticmethod
    def lower(word):
        return word.lower()


# prerprocessor = EnglishPreprocessor()
# print(not prerprocessor.stem('بیسیسمنت ؟! .  %$!#^&*() @ یبکتمنسی   '))
