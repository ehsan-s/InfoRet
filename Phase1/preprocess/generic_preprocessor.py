import re
from abc import abstractmethod


class GenericPreprocessor:

    def __init__(self):
        self.processed_list = None
        self.high_accur_param = None
        self.must_be_words = None

    def preprocess(self, text_list):
        """

        :param text_list: ['text']
        :return:
        """
        self.processed_list = []
        for news in text_list:
            self.processed_list.append(self.normalize(news))

        self.remove_high_accured_words()

        normalized_list = []
        for news in self.processed_list:
            text = self.stem_doc(news)
            normalized_list.append(text)
        self.processed_list = normalized_list
        return normalized_list

    def stem_doc(self, doc):
        normalized_words = []
        for word in self.get_word_by_word(doc):
            nword = self.stem(word)
            if nword is not None and nword != '':
                normalized_words.append(nword)
        return ' '.join(normalized_words)

    def get_word_by_word(self, doc_str):
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

    def remove_punctuation(self, word):
        return re.sub(r'[^\w\s]', '', word)

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
        cnt = 0
        for (k, v) in accurance_dict:
            cnt += 1
            if cnt < 100:
                print(k + " " + str(v))
            if v >= self.high_accur_param:
                result_dict.append((k, v))
        return result_dict

    def remove_high_accured_words(self):
        accurance_dict = self.get_accurance_dict()
        high_accur_words = set()
        # self.get_high_accurance()
        for (k, v) in accurance_dict.items():
            if v >= self.high_accur_param:
                high_accur_words.add(k)
        for must_be in self.must_be_words:
            high_accur_words.discard(must_be)
        print('stop words are: ' + str(high_accur_words))
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

