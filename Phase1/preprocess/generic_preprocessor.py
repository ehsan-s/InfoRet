import re
from abc import abstractmethod


class GenericPreprocessor:

    def __init__(self):
        self.processed_list = None
        self.high_accur_param = None
        self.must_be_words = None
        self.stop_words = None
        self.high_accured_words = None

    def preprocess(self, text_list, is_query=False):
        """

        :param text_list: ['text']
        :return:
        """
        self.processed_list = []
        for news in text_list:
            self.processed_list.append(self.normalize(news))

        if not is_query:
            self.set_stopwords()
        self.remove_stopwords()

        normalized_list = []
        for news in self.processed_list:
            text = self.__stem_doc(news)
            normalized_list.append(text)
        self.processed_list = normalized_list
        return normalized_list

    def __stem_doc(self, doc):
        normalized_words = []
        for word in self.__get_word_by_word(doc):
            nword = self.stem(word)
            if nword is not None and nword != '':
                normalized_words.append(nword)
        return ' '.join(normalized_words)

    def __get_word_by_word(self, doc_str):
        words = self.tokenize(doc_str)
        for word in words:
            yield word

    @abstractmethod
    def tokenize(self, doc_str):
        pass

    @abstractmethod
    def normalize(self, text):
        pass

    @abstractmethod
    def stem(self, word):
        pass

    def set_stopwords(self):
        self.high_accured_words = self.__find_high_accured_words()
        self.stop_words = set()
        for (k, v) in self.high_accured_words:
            if k not in self.must_be_words:
                self.stop_words.add(k)

    def remove_punctuation(self, word):
        return re.sub(r'[^\w\s]', '', word)

    def __get_accurance_dict(self):
        accurance_dict = {}
        for news in self.processed_list:
            words = news.split()
            for word in words:
                accurance_dict[word] = accurance_dict.get(word, 0) + 1
        return accurance_dict

    def __find_high_accured_words(self):
        accurance_dict = self.__get_accurance_dict()
        accurance_dict = reversed(sorted(accurance_dict.items(), key=lambda x: x[1]))
        total_accurance = 0
        for (k, v) in accurance_dict:
            total_accurance += v
        # print(total_accurance)
        accurance_dict = self.__get_accurance_dict()
        accurance_dict = reversed(sorted(accurance_dict.items(), key=lambda x: x[1]))
        high_accured_words = []
        cnt = 0
        for (k, v) in accurance_dict:
            cnt += 1
            if cnt < 100:
                pass
                # print(k + " " + str(v) + " " + str(v/total_accurance))
            if v >= self.high_accur_param:
                high_accured_words.append((k, v))
        return high_accured_words

    def get_high_accured_words(self):
        return self.high_accured_words

    def remove_stopwords(self):
        # print('stop words are: ' + str(self.high_accured_words))
        updated_processed_list = []
        for news in self.processed_list:
            updated_news = []
            words = news.split()
            for word in words:
                if word not in self.stop_words:
                    updated_news.append(word)
            updated_processed_list.append(' '.join(updated_news))
        self.processed_list = updated_processed_list
        return self.processed_list
