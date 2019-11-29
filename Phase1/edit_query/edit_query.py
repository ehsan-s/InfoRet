
class EditQuery:

    def __init__(self, token_list, indexer):
        self.query_token_list = token_list
        self.indexer = indexer

    def edit(self):
        edited_token_list = []
        for query_token in self.query_token_list:
            token_bigram = self.create_bigram(query_token)
            dictionary_candidate_words = set()
            for bi in token_bigram:
                dictionary_candidate_words.union(set(self.indexer.get_bigram_posting(bi)))
            jaccard_dict = {}
            for dict_term in dictionary_candidate_words:
                jaccard_dict[dict_term] = self.jaccard_index(query_token, dict_term)
            sorted_jaccard_dict = reversed(sorted(jaccard_dict.items(), key=lambda x: x[1]))
            counter = 0
            min_edit_dist = 1000
            min_dist_word = ''
            for (jaccard_term, jaccard_dist) in sorted_jaccard_dict:
                counter += 1
                if counter > 10:
                    break
                cur_edit_dist = self.get_edit_distance(jaccard_term, query_token)
                if cur_edit_dist < min_edit_dist:
                    min_edit_dist = cur_edit_dist
                    min_dist_word = jaccard_term

            edited_token_list.append(min_dist_word)
        return edited_token_list

    def get_edit_distance(self, word1, word2):
        edit_distance = [[0 for i in range(len(word2) + 1)] for j in range(len(word1) + 1)]
        for i in range(len(word1) + 1):
            edit_distance[i][0] = i
        for i in range(len(word2) + 1):
            edit_distance[0][i] = i
        for i in range(1, len(word1) + 1):
            for j in range(1, len(word2) + 1):
                edit_distance[i][j] = min(edit_distance[i][j-1] + 1,
                                          edit_distance[i-1][j] + 1,
                                          edit_distance[i-1][j-1] + (word1[i-1] != word2[j-1]))
        # for i in range(len(word1) + 1):
        #     print(edit_distance[i])
        # print(edit_distance[len(word1)][len(word2)])
        return edit_distance[len(word1)][len(word2)]

    def create_bigram(self, word):
        s = word + "$"
        bigram = [s[i-1] + s[i] for i in range(len(s))]
        return bigram

    def jaccard_index(self, word1, word2):
        bigram1_set = set(self.create_bigram(word1))
        bigram2_set = set(self.create_bigram(word2))
        intersect = bigram1_set.intersection(bigram2_set)
        union = bigram1_set.union(bigram2_set)
        jaccard_index = len(intersect)/len(union)
        return jaccard_index


# print(get_edit_distance("oslow", "snow"))
# print(nltk.edit_distance("oslow", "snow"))
#
# print(jaccard_index("carlo", "carol"))
# print(nltk.jaccard_distance("carlo", "carlo"))