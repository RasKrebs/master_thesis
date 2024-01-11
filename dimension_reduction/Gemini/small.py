import numpy as np

def pca(data, method='eig'):
    """
    Principal Component Analysis (PCA)

    Parameters:
    data (numpy.ndarray): The data to be analyzed.
    method (str): The method to be used for dimensionality reduction, either 'eig' for eigen decomposition or 'svd' for singular value decomposition.

    Returns:
    numpy.ndarray: The reduced data.
    """

    # Check the input data
    assert isinstance(data, np.ndarray), 'The input data must be a numpy.ndarray.'
    assert data.ndim >= 2, 'The input data must be at least a 2D array.'

    # Center the data
    data_mean = np.mean(data, axis=0)
    centered_data = data - data_mean

    # Calculate the covariance matrix
    covariance_matrix = np.cov(centered_data.T)

    # Perform dimensionality reduction
    if method == 'eig':
        # Calculate the eigenvalues and eigenvectors of the covariance matrix
        eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

        # Sort the eigenvalues and eigenvectors in descending order
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Choose the top k eigenvectors as the principal components
        k = min(data.shape[1], len(eigenvalues))
        principal_components = eigenvectors[:, :k]

    elif method == 'svd':
        # Perform singular value decomposition
        u, s, vh = np.linalg.svd(centered_data)

        # Choose the top k singular values as the principal components
        k = min(data.shape[1], len(s))
        principal_components = vh[:, :k].T

    else:
        raise ValueError('Invalid method: {}'.format(method))

    # Reduce the data to the principal components
    reduced_data = np.dot(centered_data, principal_components.T)

    return reduced_data

if __name__ == '__main__':
    # Generate some sample data
    data = np.random.randn(100, 20)

    # Perform PCA with eigen decomposition
    reduced_data_eig = pca(data, method='eig')

    # Perform PCA with singular value decomposition
    reduced_data_svd = pca(data, method='svd')

    # Print the reduced data
    print(reduced_data_eig.shape)
    print(reduced_data_svd.shape)