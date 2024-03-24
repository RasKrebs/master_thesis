import numpy as np
from typing import Optional, Union

class PrincipalComponentAnalysis:
    """
    Principal Component Analysis (PCA) class.
    """

    def __init__(self, n_components: Optional[int] = None, decomposition_method: str = 'eigen'):
        """
        Initialize the PCA class.

        Parameters:
        n_components (int): Number of components to keep. If not specified, all components are kept.
        decomposition_method (str): The method to use for decomposition. Either 'eigen' or 'svd'. Defaults to 'eigen'.
        """
        self.n_components = n_components
        self.decomposition_method = decomposition_method
        self.components = None
        self.explained_variance_ = None
        self.explained_variance_ratio_ = None
        self.cumulative_explained_variance_ratio_ = None

    def fit(self, X: Union[np.ndarray, list]):
        """
        Fit the model with X.

        Parameters:
        X (numpy.ndarray or list): Training data.
        """
        X = np.asarray(X)
        X = X - np.mean(X, axis=0)
        if self.decomposition_method == 'eigen':
            covariance_matrix = np.cov(X.T)
            eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
            idx = eigenvalues.argsort()[::-1]
            self.components = eigenvectors[:, idx]
            self.explained_variance_ = eigenvalues[idx]
        elif self.decomposition_method == 'svd':
            _, s, Vt = np.linalg.svd(X, full_matrices=False)
            self.components = Vt.T
            self.explained_variance_ = s**2 / (X.shape[0] - 1)
        self.explained_variance_ratio_ = self.explained_variance_ / self.explained_variance_.sum()
        self.cumulative_explained_variance_ratio_ = np.cumsum(self.explained_variance_ratio_)
        if self.n_components is not None:
            self.components = self.components[:, :self.n_components]
            self.explained_variance_ = self.explained_variance_[:self.n_components]
            self.explained_variance_ratio_ = self.explained_variance_ratio_[:self.n_components]
            self.cumulative_explained_variance_ratio_ = self.cumulative_explained_variance_ratio_[:self.n_components]

    def transform(self, X: Union[np.ndarray, list], n_components: Optional[int] = None):
        """
        Apply dimensionality reduction to X.

        Parameters:
        X (numpy.ndarray or list): The input data.
        n_components (int): Number of components to keep. If not specified, all components are kept.

        Returns:
        X_new (numpy.ndarray): The input data transformed to the PCA space.
        """
        X = np.asarray(X)
        X = X - np.mean(X, axis=0)
        X_new = np.dot(X, self.components[:, :n_components])
        return X_new

    def fit_transform(self, X: Union[np.ndarray, list], n_components: Optional[int] = None):
        """
        Fit the model with X and apply the dimensionality reduction on X.

        Parameters:
        X (numpy.ndarray or list): The input data.
        n_components (int): Number of components to keep. If not specified, all components are kept.

        Returns:
        X_new (numpy.ndarray): The input data transformed to the PCA space.
        """
        self.fit(X)
        return self.transform(X, n_components)