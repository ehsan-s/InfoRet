from Phase1.preprocess.english_preprocessor import EnglishPreprocessor as EP


def show_normalized_text(text):
    ep = EP()
    norm_text = ep.preprocess(text)


def show_repet_words(param=None):
    ep = EP()
    ep.preprocess()
    ep.sort_by_accurance(param)
