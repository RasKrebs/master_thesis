
# IMPORTED FROM EVALUATE SCRIPT
from memory_profiler import profile
import os
import psutil

# Get the current process ID
pid = os.getpid()

# Create a psutil Process object for the current process
process = psutil.Process(pid)

# Get the number of logical CPUs in the system
num_cores = psutil.cpu_count(logical=True)

# BELOW IMPORTS ARE FROM THE SOLUTION
        
import numpy as np
from typing import Union

class PrincipalComponentAnalysis:
    @profile
    def __init__(self, n_components: Union[int, None] = None):
        self.n_components = n_components

    @profile
    def fit(self, X: np.ndarray) -> 'PrincipalComponentAnalysis':
        # calculate mean of each feature
        mean = np.mean(X, axis=0)

        # subtract mean from the dataset
        self.X = X - mean

        # compute covariance matrix
        cov_mat = np.cov(self.X, rowvar=False)

        # compute eigen values and eigen vectors
        eig_values, eig_vectors = np.linalg.eigh(cov_mat)

        # sort eigen values in descending order and correspondingly
        # sort the eigen vectors
        idx = np.argsort(eig_values)[::-1]
        self.eigen_values = eig_values[idx]
        self.components = eig_vectors[:,idx]

        return self

    @profile
    def transform(self, X: np.ndarray) -> np.ndarray:
        # if n_components is not specified then use all the components
        n_features = X.shape[1]
        if self.n_components and self.n_components <= n_features:
            n_features = self.n_components

        return np.dot(X, self.components[:, :n_features])

    @profile
    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        # fit to the data and then transform it
        return self.fit(X).transform(X)
