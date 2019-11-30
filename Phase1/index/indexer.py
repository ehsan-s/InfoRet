import os, pickle
import ast
from Phase1.index.gamma_code import GammaCodeCompressor as GC, GammaCodeDecompressor as GD
from Phase1.index.variable_byte import VariableByteCompressor as VC, VariableByteDecompressor as VD


class Indexer:
    def __init__(self, index_file='index.pkl', doc_directory='docs/'):
        # list of doc_ids
        self.posting = []
        # {term: t_id}
        self.term_mapping = {}
        # {t_id: term}
        self.inv_term_mapping = {}
        # positional indexing {t_id: {doc_id: [pos]}}
        self.dictionary = {}
        # {doc_id: {t_id: tf}}
        self.doc_dictionary = {}
        # bi_gram indexing {bi: {t_id}}
        self.bigram = {}

        self.max_doc_id = -1
        self.max_term_id = -1

        self.doc_directory = doc_directory
        self.index_file = index_file

    def add_doc(self, doc):
        self.max_doc_id += 1
        doc_id = self.max_doc_id

        self.__save_doc(doc, doc_id)
        self.posting.append(doc_id)

        self.__indexer_add(doc_id)

    def del_doc(self, doc_id):
        self.__indexer_remove(doc_id)

        os.remove(self.doc_directory + str(doc_id) + '.txt')
        self.posting.remove(doc_id)

    def save_index(self):
        pickle.dump(self, open(self.index_file, 'wb'), pickle.HIGHEST_PROTOCOL)

    def save_dictionary(self, method="normal", file_name=None):
        """

        :param method: can be "normal", "gamma" or "var"
        :return:
        """
        if file_name is None:
            file_name = method + "_dict.txt"
        if method == "normal":
            with open(file_name, 'w') as file:
                file.write(str(self.dictionary))
                file.close()
        elif method == 'gamma':
            GC.compress_to_file(self.dictionary, file_name)
        elif method == 'var':
            VC.compress_to_file(self.dictionary, file_name)

    def load_dictionary(self, method="normal", file_name=None):
        """

        :param method: can be "normal", "gamma" or "var"
        :return:
        """
        if file_name is None:
            file_name = method + "_dict.txt"
        if method == "normal":
            with open(file_name, 'r') as file:
                self.dictionary = ast.literal_eval(file.readline())
                file.close()
        elif method == 'gamma':
            self.dictionary = GD.decompress_from_file(file_name)
        elif method == 'var':
            self.dictionary = VD.decompress_from_file(file_name)

    @staticmethod
    def load(index_file='index.pkl'):
        return pickle.load(open(index_file, 'rb'))

    def get_posting(self, term):
        t_id = self.term_mapping.get(term)
        return list(self.dictionary.get(t_id).keys())

    def get_pos_posting(self, term):
        t_id = self.term_mapping.get(term)
        return self.dictionary.get(t_id)

    def get_bigram_posting(self, bi):
        t_id_set = self.bigram.get(bi)
        terms = []
        if t_id_set is not None:
            for t_id in t_id_set:
                term = self.inv_term_mapping.get(t_id)
                if term is not None:
                    terms.append(term)
        return terms

    def __indexer_add(self, doc_id):
        """
        index doc_id and adds to the dictionary
        :return:
        """
        self.doc_dictionary[doc_id] = {}
        with open(self.doc_directory + str(doc_id) + '.txt', 'r') as file:
            line = file.readline()
            pos = []
            while not line == '':
                terms = line.rstrip('\n').split()
                for local_pos, term in enumerate(terms):
                    t_id = self.term_mapping.get(term)
                    if t_id is None:
                        self.max_term_id += 1
                        t_id = self.max_term_id
                        self.term_mapping[term] = t_id
                        self.inv_term_mapping[t_id] = term
                        # update bigram_index
                        self.__bigram_indexer_add(t_id)
                    docs = self.dictionary.get(t_id)
                    if self.doc_dictionary.get(doc_id).get(t_id) is None:
                        self.doc_dictionary.get(doc_id)[t_id] = 0
                    self.doc_dictionary.get(doc_id)[t_id] += 1
                    if docs is None:
                        self.dictionary[t_id] = {}
                        docs = self.dictionary.get(t_id)

                    poses = docs.get(doc_id)
                    if poses is None:
                        docs[doc_id] = []
                        poses = docs.get(doc_id)
                    term_pos = len(pos) + local_pos
                    poses.append(term_pos)

                pos.extend(terms)
                line = file.readline()

    def __indexer_remove(self, doc_id):
        """
        removes doc_id from the dictionary and updates the index
        :param doc_id:
        :return:
        """
        self.doc_dictionary.pop(doc_id, None)
        for t_id in self.dictionary:
            self.dictionary.get(t_id).pop(doc_id, None)
            if self.dictionary.get(t_id) == {}:
                # delete term
                self.__bigram_indexer_remove(t_id)
                term = self.inv_term_mapping.pop(t_id, None)
                self.term_mapping.pop(term, None)

    def __bigram_indexer_add(self, t_id):
        term = self.inv_term_mapping.get(t_id)
        for i in range(len(term)):
            bi = term[i:(i + 2)]
            if len(bi) == 1:
                bi = bi + "$"
            t_id_set = self.bigram.get(bi)
            if t_id_set is None:
                self.bigram[bi] = set()
                t_id_set = self.bigram.get(bi)
            t_id_set.add(t_id)

    def __bigram_indexer_remove(self, t_id):
        term = self.inv_term_mapping.get(t_id)
        for i in range(len(term) - 1):
            bi = term[i:(i + 2)]
            if len(bi) == 1:
                bi = bi + "$"
            t_id_set = self.bigram.get(bi)
            if t_id in t_id_set:
                t_id_set.remove(t_id)

    def __save_doc(self, doc, doc_id):
        with open(self.doc_directory + str(doc_id) + '.txt', 'w') as file:
            file.write(doc)
            file.close()
