from Phase1.preprocess.persian_preprocessor import PersianPreprocessor as PP
from Phase1.preprocess.english_preprocessor import EnglishPreprocessor as EP
from Phase1.index.indexer import Indexer
from Phase1.preprocess.document_io import read_csv_file_as_list as read_english, \
    read_persian_xml_file_as_list as read_persian
from Phase1.edit_query.edit_query import EditQuery as EQ
from Phase1.search import Searcher

import os

if __name__ == '__main__':
    ep_all = EP()
    pp_all = PP()
    eng_docs = ep_all.preprocess(read_english())
    per_docs = pp_all.preprocess(read_persian())
    indexer = Indexer()
    while True:
        print('Enter the section number:')
        section = input()
        print('Enter subsection number:')
        subsection = input()
        if section == '1':
            if subsection == '1':
                print('Enter the text:')
                txt = input()
                is_eng = EQ.is_english(query=txt)
                if is_eng:
                    norm_text = EP().preprocess([txt])
                else:
                    norm_text = PP().preprocess([txt])
                print(norm_text)
            elif subsection == '2':
                print('English Repetitive Words:')
                print(ep_all.get_high_accured_words())
                print('Persian Repetitive Words:')
                print(pp_all.get_high_accured_words())

        elif section == '2':
            if subsection == '1':
                for doc in eng_docs:
                    indexer.add_doc(doc)
                for doc in per_docs:
                    indexer.add_doc(doc)
                print('Indexing is done')
            elif subsection == '2':
                print('Enter the term:')
                term = input()
                ed_term = EQ(term, indexer, ep_all, pp_all).edit()
                print(indexer.get_posting(ed_term))
            elif subsection == '3':
                print('Enter the term:')
                term = input()
                ed_term = EQ(term, indexer, ep_all, pp_all).edit()
                print(indexer.get_pos_posting(ed_term))

        elif section == '3':
            indexer.save_dictionary(file_name='normal_dict.txt')
            print("normal dict size: " + str(os.path.getsize('normal_dict.txt')))
            if subsection == '1':
                indexer.save_dictionary(method='var', file_name='var_dict.txt')
                print("‫‪variable‬‬ ‫‪byte‬‬ dict size: " + str(os.path.getsize('var_dict.txt')))
                indexer.load_dictionary(method='var', file_name='var_dict.txt')
                print('Indexer saved and loaded')
            elif subsection == '2':
                indexer.save_dictionary(method='gamma', file_name='gamma_dict.txt')
                print("gamma code‬‬ dict size: " + str(os.path.getsize('gamma_dict.txt')))
                indexer.load_dictionary(method='gamma', file_name='gamma_dict.txt')
                print('Indexer saved and loaded')
        elif section == '4':
            if subsection == '1':
                print('Enter the query:')
                query = input()
                print(EQ(query, indexer, ep_all, pp_all).edit())
        elif section == '5':
            if subsection == '1':
                print('Enter the query:')
                query = input()
                ed_query = EQ(query, indexer, ep_all, pp_all).edit()
                print(Searcher(indexer).search(ed_query))
            elif subsection == '2':
                print('Enter the query:')
                query = input()
                print('Enter the window size')
                size = int(input())
                ed_query = EQ(query, indexer, ep_all, pp_all).edit()
                print(Searcher(indexer).search_prox(ed_query, size))
        elif section == 'exit':
            break
        else:
            print('wrong input')

# if __name__ == '__main__':
#     ep = EP()
#     docs = ep.preprocess(read_english())
#     indexer = Indexer()
#     for doc in docs:
#         indexer.add_doc(doc)
#     print(EQ('Europe us is here man!', indexer).edit())
