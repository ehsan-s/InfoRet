from Phase1.preprocess.english_preprocessor import EnglishPreprocessor as EP
from Phase1.preprocess.persian_preprocessor import PersianPreprocessor as PP
from Phase1.indexer import Indexer
from Phase1.preprocess.document_io import read_csv_file_as_list as read_english, \
    read_persian_xml_file_as_list as read_persian
from Phase1.edit_query.edit_query import EditQuery as EQ
from Phase1.search import Searcher

def show_normalized_text(text):
    ep = EP()
    norm_text = ep.preprocess(text)
    return norm_text


def show_repet_words(ep, pp, p_text, e_text):
    ep.preprocess(e_text)
    pp.preprocess(p_text)
    eng_repet_words = ep.sort_by_accurance()
    p_repet_words = pp.sort_by_accurance()
    return eng_repet_words


def make_index():
    ep = EP()
    ep.preprocess(read_english())
    pp = PP()
    pp.preprocess(read_persian())
    eng_docs = ep.processed_list
    pers_docs = pp.processed_list
    indexer = Indexer()
    for doc in eng_docs:
        indexer.add_doc(doc)
    for doc in pers_docs:
        indexer.add_doc(doc)
    return indexer


def show_posting_list(indexer, term):
    eq = EQ(term, indexer)
    term = eq.edit()
    return indexer.get_posting(term)


def show_pos_posting(indexer, term):
    eq = EQ(term, indexer)
    term = eq.edit()
    return indexer.get_pos_posting(term)

def search(indexer, query):
    eq = EQ(query, indexer)
    query = eq.edit()
    searcher = Searcher(indexer)
    searcher.search(query)

if __name__ == '__main__':
    ep = EP()
    pp = PP()
    indexer = None
    english_text = read_english()
    persian_text = read_persian()
    while True:
        print('Enter the section number:')
        section = input()
        print('Enter subsection number:')
        subsection = input()
        if section == '1':
            if subsection == '1':
                print('Enter the text:')
                text = input()
                print(show_normalized_text(text))
            elif subsection == '2':


        elif section == '2':
            pass
        elif section == '3':
            pass
        elif section == '4':
            pass
        elif section == '5':
            pass
        elif section == 'exit':
            break
        else:
            print('wrong input')
    ep.preprocess()
    ep.get_high_accurance(param)
