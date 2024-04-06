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



import numpy as np

class StrassenMatrixMultiplier:
    def __init__(self, mat1, mat2):
        # Check if matrices are valid
        if not self.is_valid_matrix(mat1) or not self.is_valid_matrix(mat2):
            raise ValueError("Invalid matrices. Matrices must be 2D arrays with equal dimensions that are powers of 2.")
        
        # Check if matrices can be multiplied
        if len(mat1[0]) != len(mat2):
            raise ValueError("Matrices cannot be multiplied. Number of columns in mat1 must be equal to number of rows in mat2.")
        
        # Initialize matrices
        self.mat1 = mat1
        self.mat2 = mat2
        
    def is_valid_matrix(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        
        if rows != cols:  # Check if matrix is symmetric
            return False
        
        if rows == 1:  # Base case for the recursive algorithm
            return True
        
        if rows & (rows - 1) == 0:  # Check if dimensions are powers of 2
            return True
        else:
            return False
        
    def multiply_matrices(self):
        if len(self.mat1) == 1:  # Base case - use standard matrix multiplication
            return np.dot(self.mat1, self.mat2)
        
        # Split matrices into quadrants
        a11, a12, a21, a22 = self.split_matrix(self.mat1)
        b11, b12, b21, b22 = self.split_matrix(self.mat2)
        
        # Calculate Strassen sub-products
        p1 = StrassenMatrixMultiplier(a11 + a22, b11 + b22).multiply_matrices()
        p2 = StrassenMatrixMultiplier(a21 + a22, b11).multiply_matrices()
        p3 = StrassenMatrixMultiplier(a11, b12 - b22).multiply_matrices()
        p4 = StrassenMatrixMultiplier(a22, b21 - b11).multiply_matrices()
        p5 = StrassenMatrixMultiplier(a11 + a12, b22).multiply_matrices()
        p6 = StrassenMatrixMultiplier(a21 - a11, b11 + b12).multiply_matrices()
        p7 = StrassenMatrixMultiplier(a12 - a22, b21 + b22).multiply_matrices()
        
        # Calculate resulting quadrants
        c11 = p1 + p4 - p5 + p7
        c12 = p3 + p5
        c21 = p2 + p4
        c22 = p1 - p2 + p3 + p6
        
        # Combine resulting quadrants
        result = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))
        
        return result
        
    def split_matrix(self, matrix):
        size = len(matrix)
        mid = size // 2
        upper = matrix[:mid]
        lower = matrix[mid:]
        left = [row[:mid] for row in upper]
        right = [row[mid:] for row in upper]
        
        return left, right, [row[:mid] for row in lower], [row[mid:] for row in lower]
def execute():
    # Set a seed for reproducibility
    np.random.seed(42)
    
    # Define the dimensions for the matrices
    dim = 64 
    
    # Generate random matrices A and B of size dim x dim
    A = np.random.randint(1, 10, size=(dim, dim)) 
    B = np.random.randint(1, 10, size=(dim, dim))
    
    # Perform matrix multiplication using the Strassen algorithm
    C = strassen(A, B)



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
