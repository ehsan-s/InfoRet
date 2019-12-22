from Phase1.preprocess.english_preprocessor import EnglishPreprocessor
from nltk.corpus import stopwords


class Preprocessor(EnglishPreprocessor):

    def set_stopwords(self):
        self.stop_words = stopwords.words('english')
