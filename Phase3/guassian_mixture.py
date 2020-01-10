from sklearn.mixture import GaussianMixture
from Phase3.clustering import Clustering
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from Phase3.document_io import write_csv_file as csv_report


class GuassianMixture:
    def __init__(self, data, vectorizer, n_clusters=3):
        self.method_name = 'GMM'
        self.data = data
        self.n_clusters = n_clusters
        self.clustering = Clustering(data,
                                     vectorizer,
                                     GaussianMixture(n_components=self.n_clusters,
                                                    max_iter=250,
                                                    covariance_type='full'))
        self.clustering.fit()
        self.clustering_centers = self.clustering.model.means_
        self.clustering_labels = self.clustering.predict(data['text'])

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
        dim_reduced_centers = pca.transform(self.clustering_centers)
        plt.scatter(x=dim_reduced_centers[:, 0],
                    y=dim_reduced_centers[:, 1],
                    c='black',
                    s=5,
                    marker='x')
        plt.title(self.method_name + ' - ' + self.clustering.vectorizer.name + ' (K = {})'.format(self.n_clusters))
        plt.show()

    def report(self):
        csv_report('report/' + self.method_name + '_' + self.clustering.vectorizer.name + '.csv',
                   self.data['id'],
                   self.clustering_labels)
