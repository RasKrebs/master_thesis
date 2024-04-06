import psutil
import os
import threading
import multiprocessing

# Define a global variable to store the maximum resources usage
max_resources_usage = {"cpu": 0, "memory": 0}


import numpy as np
np.random.seed(42)


# Implement the resource monitor
def resource_monitor():
    """
    Monitors the CPU and memory usage of the current process, updating global max usage.
    """
    global max_resources_usage
    process = psutil.Process(os.getpid())
    
    while monitoring:
        cpu_usage = process.cpu_percent(interval=1) / multiprocessing.cpu_count()
        memory_usage = process.memory_info().rss
        max_resources_usage['cpu'] = max(max_resources_usage['cpu'], cpu_usage)
        max_resources_usage['memory'] = max(max_resources_usage['memory'], memory_usage)



from typing import Union
import numpy as np
import pandas as pd


class PrincipalComponentAnalysis:
    """Principal Component Analysis (PCA) implementation.
    Can perform both singular value decomposition and eigenvalue decomposition.
    """
    def __init__(self, n_components:int = 0, decomposition:str = 'eigen') -> None:
        """
            Initializes the Principal Component Analysis model.

            Parameters:
                n_components (int): The number of components to keep.
                    Default is all.

            Methods:
                fit(X): Applies PCA to the input data.

                transform(X, n_components): Transforms the input data to
                    the specified number of components using the fitted PCA model.

                fit_transform(X): Applied pca to input, transforms to
                    specified number of components and returns the reduced data.

            Attributes:
                n_components (int): The number of components to keep.
                components (None): Placeholder for the components.
                mean (None): Placeholder for the sample mean.
                decomposition (str): The type of decomposition to use. Either 'eigen'
                    or 'svd'.
        """
        self.n_components = n_components
        self.components = None
        self.mean = None
        self.eigenvalues = None
        self.components = None
        self.explained_variance_ratio = None
        self.cumulative_explained_variance = None

        # Assert decomposition is valid
        if decomposition not in ['eigen', 'svd']:
            raise ValueError("Decomposition must be either 'eigen' or 'svd'")

        self.decomposition = decomposition

    def fit(self, data: Union[pd.DataFrame, np.ndarray, list]) -> None:
        """
        Applies PCA to the input data.

        Parameters:
            data (pandas.DataFrame, numpy.ndarray, list): The input data to fit
                the model on.
        """
        # Handling different input types
        if isinstance(data, pd.DataFrame):
            data = data.values
        elif isinstance(data, list):
            data = np.array(data)
        elif isinstance(data, np.ndarray):
            pass
        else:
            raise TypeError("`data` must be a pandas dataframe, numpy array or list")

        # Mean centering
        self.mean = np.mean(data, axis=0)
        data_centered = data - self.mean

        # Standard decomposition
        if self.decomposition == 'eigen':
            # Compute Sample Covariance Matrix
            cov = 1/(len(data)-1) * (data_centered).T @ (data_centered)

            #  Calculate eigenvalues and eigenvectors
            eigenvalues, eigenvectors = np.linalg.eig(cov)
            eigenvectors = eigenvectors.T # Transpose eigenvectors

        else:
            # Compute SVD
            _, singular_values, unit_arr = np.linalg.svd(data_centered, full_matrices=False)

            # Store results - Using same variable names for simpler code
            eigenvectors, eigenvalues = unit_arr.T, singular_values**2

        # Sorting in descending order
        eigenvalues_sorted_index = sorted(range(len(eigenvalues)), key=lambda k: eigenvalues[k],
                                          reverse=True)
        self.eigenvalues = eigenvalues[eigenvalues_sorted_index]
        self.components = eigenvectors[eigenvalues_sorted_index]

        # Compute explained variance and cumulative explained variance ratio
        self.explained_variance_ratio = (self.eigenvalues / np.sum(self.eigenvalues)) * 100
        self.cumulative_explained_variance = np.cumsum(self.explained_variance_ratio)

        # Keep only n_components (if specified)Selecting components
        if self.n_components != 0:
            self.components = self.components[0:self.n_components]

    def transform(self, data: Union[pd.DataFrame, np.ndarray, list], n_components: int = 0
                  ) -> np.ndarray:
        """
        Transforms the input data to the specified number of components using the fitted PCA model.

        Parameters:
            data (Union[pd.DataFrame, np.ndarray, list]): The input data to be transformed.

        Returns:
            np.ndarray: The transformed data.
        """
        # Raise error if fit has not been called
        if self.mean is None or self.components is None:
            raise ValueError("Please fit the model first")

        # Transforms to specified number of components, if not specified, use all
        if n_components != 0:
            self.components = self.components[0:n_components]

        return (data - self.mean) @ self.components.T

    def fit_transform(self, data: Union[pd.DataFrame, np.ndarray, list], n_components: int = 0
                      ) -> np.ndarray:
        """
        Applied pca to input, transforms to specified number of components and returns
            the reduced data.

        Parameters:
            data (Union[pd.DataFrame, np.ndarray, list]): The input data to fit the model
                on and transform.
            n_components (int): The number of components to keep. Default is all.

        Returns:
            np.ndarray: The transformed data.

        """
        # Apply PCA and transform data
        self.n_components = n_components
        self.fit(data)
        return self.transform(data)
def execute():
    # Set the random seed for reproducibility
    np.random.seed(42)
    
    # Generate random data: 100 samples with 5 features
    X = np.random.rand(100, 5)
    
    # Initialize PCA with 2 components
    pca = PrincipalComponentAnalysis(n_components=2)
        
    # Fit PCA on the generated data
    pca.fit(X)
    
    # Transform the data using the fitted PCA
    X_pca = pca.transform(X)
    
# Execute the function to see the results



if __name__ == "__main__":
    # Start the resource monitoring in a separate thread
    global monitoring
    monitoring = True
    monitor_thread = threading.Thread(target=resource_monitor)
    monitor_thread.start()

    # Execute the Huffman coding process

    # Using the execute function
    output = execute()


    # Stop the monitoring
    monitoring = False
    monitor_thread.join()

    print(max_resources_usage['cpu']), print(max_resources_usage['memory'] / (1024**2))

