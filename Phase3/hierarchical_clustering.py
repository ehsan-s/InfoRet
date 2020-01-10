from sklearn.cluster import AgglomerativeClustering
from Phase3.clustering import Clustering
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, ward
from Phase3.document_io import write_csv_file as csv_report


class HierarchicalClustering:
    def __init__(self, data, vectorizer, n_clusters=3):
        self.method_name = 'Hierarchical'
        self.data = data
        self.n_clusters = n_clusters
        cluster_model = AgglomerativeClustering(n_clusters=self.n_clusters, linkage='ward')
        self.clustering = Clustering(data, vectorizer, cluster_model)
        self.clustering_labels = self.clustering.fit_predict()

    def plot_2D(self):
        pca = PCA(n_components=2)
        dim_reduced_data = pca.fit_transform(self.clustering.vectors)
        colors = ['red', 'green', 'blue', 'olive', 'gray', 'pink']
        cluster_colors = [colors[cluster_num] for cluster_num in self.clustering_labels]

        plt.scatter(x=dim_reduced_data[:, 0],
                    y=dim_reduced_data[:, 1],
                    c=cluster_colors,
                    s=5,
                    marker='o')
        plt.title(self.method_name + ' - ' + self.clustering.vectorizer.name + ' (K = {})'.format(self.n_clusters))
        plt.show()

    def plot_dendrogram(self):
        linkage_matrix = ward(self.clustering.vectors)
        dendrogram(linkage_matrix, truncate_mode='level', p=3)
        plt.title('Dendrogram: ' + self.method_name + ' - ' + self.clustering.vectorizer.name +
                  ' (K = {})'.format(self.n_clusters))
        plt.show()

    def report(self):
        csv_report('report/' + self.method_name + '_' + self.clustering.vectorizer.name + '.csv',
                   self.data['id'],
                   self.clustering_labels)
