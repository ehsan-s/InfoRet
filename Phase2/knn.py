import numpy as np
class KNN:
    def __init__(self, n_neighbours):
        self.k = n_neighbours
        self.train_X = None
        self.train_y = None

    def fit(self, X, y):
        self.train_X = X
        self.train_y = y
