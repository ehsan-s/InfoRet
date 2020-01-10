from Phase3.document_io import read_csv_file as read_english
from Phase3.tfidf_vectorizer import TfIdfVectorizer
from Phase2.preprocessor import Preprocessor
from Phase3.kmeans import KMEANS
from Phase3.guassian_mixture import GuassianMixture
from Phase3.hierarchical_clustering import HierarchicalClustering
from Phase3.word2vec import Word2Vec


if __name__ == '__main__':
    data = read_english('source/Data.csv')
    vectorizers = [TfIdfVectorizer, Word2Vec]
    clustering_models = [KMEANS, GuassianMixture, HierarchicalClustering]

    for model in clustering_models:
        for vectorizer in vectorizers:
            clustering = model(data, vectorizer(data['text'], Preprocessor()))
            clustering.plot_2D()
            if model == HierarchicalClustering:
                clustering.plot_dendrogram()
            clustering.report()
