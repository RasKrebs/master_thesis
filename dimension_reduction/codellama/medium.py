class PrincipalComponentAnalysis:
    """
    A class for implementing Principal Component Analysis (PCA) from scratch.

    Attributes:
        n_components (int): The number of components to use in the PCA decomposition. If not specified, it will default to all components.
        decomposition_method (str): The method to use for decomposing the data into principal components. Either 'eigen' or 'svd'. If not specified, it will
default to 'eigen'.

    Methods:
        fit(X) -> None: Fits the PCA model on the input data X.
        transform(X) -> np.ndarray: Transforms the input data X into a lower-dimensional space using the fitted PCA model.
        fit_transform(X) -> np.ndarray: Fits the PCA model on the input data X and then transforms the data into a lower-dimensional space.
    """

    def __init__(self, n_components=None, decomposition_method='eigen'):
        self.n_components = n_components
        self.decomposition_method = decomposition_method

    def fit(self, X):
        # Compute the covariance matrix of the input data
        cov = np.cov(X, rowvar=False)

        # Compute the eigenvectors and eigenvalues of the covariance matrix
        eigvals, eigvecs = np.linalg.eigh(cov)

        # Sort the eigenvalues in descending order
        sorted_eigvals = np.sort(eigvals)[::-1]

        # Select the top n eigenvectors corresponding to the largest eigenvalues
        self.components_ = eigvecs[:self.n_components]

        # Compute the principal components by projecting the data onto the selected eigenvectors
        self.principal_components_ = np.dot(X, self.components_)

    def transform(self, X):
        return np.dot(X, self.components_)

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)