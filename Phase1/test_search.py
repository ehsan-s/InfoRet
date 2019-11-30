from Phase1.search import Searcher
from Phase1.index.indexer import Indexer


if __name__ == '__main__':
    doc1 = "i was a kid in an infinite yard\n i was a kid without a heart"
    doc2 = "my infinite heart rate destroyed us"
    doc3 = "playing with my kid helped me not to be a destroyed lost"
    indexer = Indexer()
    indexer.add_doc(doc1)
    indexer.add_doc(doc2)
    indexer.add_doc(doc3)
    # doc4 = 'my i i i heart rate increased as a kid\n playing in the yard helped me to get rid'
    # indexer.del_doc(doc_id=2)
    # indexer.add_doc(doc4)
    # print(indexer.get_posting('heart'))
    # print(indexer.get_pos_posting('kid'))
    # print(indexer.get_bigram_posting('d$'))
    # print(indexer.get_bigram_posting('it'))
    # indexer.save_index()
    # new_indexer = Indexer.load()
    # searcher = Searcher(indexer)
    # print(searcher.search(['infinite', 'kid']))
    # print(searcher.search_prox(['i', 'heart'], 7))
    print(indexer.dictionary)
    indexer.save_dictionary()
    indexer.save_dictionary(method='gamma')
    indexer.save_dictionary(method='var')
    indexer.load_dictionary()
    print(indexer.dictionary)
    indexer.load_dictionary(method='gamma')
    print(indexer.dictionary)
    indexer.load_dictionary(method='var')
    print(indexer.dictionary)
