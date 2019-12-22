import re
import unicodedata
import hazm
import inflect
import nltk
from hazm import Stemmer
from Phase1.preprocess.generic_preprocessor import GenericPreprocessor


class PersianPreprocessor(GenericPreprocessor):

    def __init__(self):
        self.stemmer = Stemmer()
        self.high_accur_param = 8040
        self.must_be_words = []

    def tokenize(self, doc_str):
        return hazm.word_tokenize(doc_str)

    def normalize(self, text):
        text = self.remove_punctuation(text)
        text = re.sub(' +', ' ', text.strip())
        return text

    def stem(self, word):
        word = self.stemmer.stem(word)
        word = re.sub(' +', ' ', word.strip())
        return word

# prerprocessor = PersianPreprocessor()
# print(prerprocessor.remove_punctuation(''))
# hazm.Normalizer().stem()
# print(prerprocessor.remove_stopwords())
