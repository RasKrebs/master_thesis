RasKrebs: Create a python class called PrincipalComponentAnalysis that implements the Principal Component Analysis algorithm from scratch. It should have three methods, fit, transform and fit_transform. Two arguments should be able to be passed, first is n_components which specifies the number of components to use. If n_components is not specified it should default to all. Second is decomposition_method, which should be either 'eigen' or 'svd'. If not specified it should default to 'eigen'.

Make sure to add documentation to the class and methods in the form of docstrings and comments. Also make sure to add type hints to the methods.

GitHub Copilot: Here is a Python class that implements the Principal Component Analysis algorithm from scratch:

```python
import numpy as np
from typing import Optional, Union

class PrincipalComponentAnalysis:
    """
    Principal Component Analysis (PCA) class.

    Parameters
    ----------
    n_components : int, optional
        Number of components to use. If not specified, all components are used.
    decomposition_method : str, optional
        Method to use for decomposition. Either 'eigen' or 'svd'. If not specified, 'eigen' is used.
    """

    def __init__(self, n_components: Optional[int] = None, decomposition_method: Optional[str] = 'eigen'):
        self.n_components = n_components
        self.decomposition_method = decomposition_method
        self.components = None
        self.mean = None

    def fit(self, X: np.ndarray) -> None:
        """
        Fit the model with X.

        Parameters
        ----------
        X : numpy array of shape (n_samples, n_features)
            Training data.
        """
        # Calculate the mean
        self.mean = np.mean(X, axis=0)
        X = X - self.mean

        # Calculate the covariance matrix
        cov = np.cov(X.T)

        # Eigen decomposition
        if self.decomposition_method == 'eigen':
            eigenvalues, eigenvectors = np.linalg.eig(cov)
            # Sort eigenvectors
            eigenvectors = eigenvectors.T
            idxs = np.argsort(eigenvalues)[::-1]
            eigenvalues = eigenvalues[idxs]
            eigenvectors = eigenvectors[idxs]
        # Singular Value Decomposition
        elif self.decomposition_method == 'svd':
            eigenvectors, s, v = np.linalg.svd(X.T)
            eigenvalues = s**2 / (X.shape[0] - 1)

        # Store first n eigenvectors
        self.components = eigenvectors[0:self.n_components]

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Apply the dimensionality reduction on X.

        Parameters
        ----------
        X : numpy array of shape (n_samples, n_features)
            Input data.

        Returns
        -------
        X_new : numpy array of shape (n_samples, n_components)
            Transformed values.
        """
        X = X - self.mean
        return np.dot(X, self.components.T)

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """
        Fit the model with X and apply the dimensionality reduction on X.

        Parameters
        ----------
        X : numpy array of shape (n_samples, n_features)
            Training data.

        Returns
        -------
        X_new : numpy array of shape (n_samples, n_components)
            Transformed values.
        """
        self.fit(X)
        return self.transform(X)
```

This class has three methods: `fit`, `transform`, and `fit_transform`. The `fit` method calculates the mean and covariance of the data, and then performs either eigen decomposition or singular value decomposition based on the `decomposition_method` parameter. The `transform` method applies the dimensionality reduction on the data. The `fit_transform` method combines these two steps.