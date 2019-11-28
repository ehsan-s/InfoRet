import numpy as np
import operator


class Searcher:
    def __init__(self, indexer):
        self.indexer = indexer
        self.K = 10

    def __search(self, doc_ids, v_q):
        """
        computes lnc weight for each document (v_d) and returns the top score docs for the v_q.
        :param doc_ids: list of [(doc_id, tf)] for each term
        :param v_q: normalized query weight vector
        """
        q_num = len(doc_ids)
        scores = {}
        for term in range(q_num):
            for doc in doc_ids[term]:
                doc_id, tf, length = doc[0], doc[1], doc[2]
                if scores.get(doc_id) is None:
                    scores[doc_id] = 0
                scr = 1 + np.log(tf)
                scores[doc_id] += scr * v_q[term]
        for doc_id in scores.keys():
            length = np.linalg.norm(list(self.indexer.doc_dictionary.get(doc_id).values()))
            scores[doc_id] = scores.get(doc_id) / length
        top_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)[0:self.K]

        return list(zip(*top_scores))[0]

    def __calc_query_weight(self, query):
        """
        ltc weight
        :param query: list of terms
        :return: normalized v_q and term_id list
        """
        query_ids = {}
        for term in query:
            tid = self.indexer.term_mapping.get[term]
            if query_ids.get(tid) is None:
                query_ids[tid] = 0
            query_ids[tid] += 1
        v_q = np.zeros(len(query_ids.keys()))
        for i, id in enumerate(query_ids.keys()):
            l = query_ids.get(id)
            N = len(self.indexer.posting)
            df = len(self.indexer.dictionary.get(id))
            t = np.log(N / df)
            v_q[i] = l * t
        norm = np.linalg.norm(v_q)
        if norm != 0:
            v_q /= norm
        return v_q, query_ids.keys()

    def search(self, query):
        """

        :param query: list of terms
        :return:
        """
        v_q, t_ids = self.__calc_query_weight(query)
        doc_ids = []
        for id in t_ids:
            doc_dict = self.indexer.dictionary.get(id)
            doc_id_tf = []
            for doc_id in doc_dict.keys():
                tf = len(doc_dict.get(doc_id))
                doc_id_tf.append((doc_id, tf))
            doc_ids.append(doc_id_tf)
        return self.__search(doc_ids, v_q)
