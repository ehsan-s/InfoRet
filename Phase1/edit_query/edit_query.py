import nltk

def get_edit_distance(word1, word2):
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

print(get_edit_distance("oslow", "snow"))
print(nltk.edit_distance("oslow", "snow"))

def create_bigram(word):
    s = word + "$"
    bigram = [s[i-1] + s[i] for i in range(len(s))]
    print(bigram)
    return bigram

def jaccard_index(word1, word2):
    bigram1_set = set(create_bigram(word1))
    bigram2_set = set(create_bigram(word2))
    intersect = bigram1_set.intersection(bigram2_set)
    union = bigram1_set.union(bigram2_set)
    jaccard_index = len(intersect)/len(union)
    print(jaccard_index)
    return jaccard_index

print(jaccard_index("carlo", "carol"))
# print(nltk.jaccard_distance("carlo", "carlo"))