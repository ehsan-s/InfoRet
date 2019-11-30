from Phase1.preprocess.persian_preprocessor import PersianPreprocessor as PP
from Phase1.preprocess.english_preprocessor import EnglishPreprocessor as EP
from Phase1.indexer import Indexer
from Phase1.preprocess.document_io import read_csv_file_as_list as read_english, \
    read_persian_xml_file_as_list as read_persian
from Phase1.edit_query.edit_query import EditQuery as EQ
from Phase1.search import Searcher

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
                is_eng = EQ.is_english(txt)
                if is_eng:
                    norm_text = EP().preprocess([txt])
                else:
                    norm_text = PP().preprocess([txt])
                print(norm_text)
            elif subsection == '2':
                print('English Repetitive Words:')
                print(ep_all.get_high_accurance())
                print('Persian Repetitive Words:')
                print(pp_all.get_high_accurance())

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
                ed_term = EQ(term, indexer).edit()
                print(indexer.get_posting(ed_term))
            elif subsection == '3':
                print('Enter the term:')
                term = input()
                ed_term = EQ(term, indexer).edit()
                print(indexer.get_pos_posting(ed_term))

        elif section == '3':
            # TODO compressing
            pass
        elif section == '4':
            if subsection == '1':
                print('Enter the query:')
                query = input()
                print(EQ(query, indexer).edit())
        elif section == '5':
            if subsection == '1':
                print('Enter the query:')
                query = input()
                ed_query = EQ(query, indexer).edit()
                Searcher(indexer).search(ed_query)
            elif subsection == '2':
                print('Enter the query:')
                query = input()
                print('Enter the window size')
                size = int(input())
                ed_query = EQ(query, indexer).edit()
                Searcher(indexer).search_prox(ed_query, size)
        elif section == 'exit':
            break
        else:
            print('wrong input')
