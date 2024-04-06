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
from typing import Union, List

def strassen(A: Union[List[List[int]], np.ndarray], B: Union[List[List[int]], np.ndarray]) -> Union[List[List[int]], np.ndarray]:
    """
    Implementation of the Strassen algorithm for matrix multiplication.

    Parameters:
    A (Union[List[List[int]], np.ndarray]): The first matrix.
    B (Union[List[List[int]], np.ndarray]): The second matrix.

    Returns:
    Union[List[List[int]], np.ndarray]: The product of the two matrices.
    """

    # Convert lists to numpy arrays
    if isinstance(A, list):
        A = np.array(A)
    if isinstance(B, list):
        B = np.array(B)

    # Check if the matrices are valid
    if A.shape[1] != B.shape[0]:
        raise ValueError("The number of columns in the first matrix must be equal to the number of rows in the second matrix.")
    if not (np.log2(A.shape[0]).is_integer() and np.log2(A.shape[1]).is_integer() and np.log2(B.shape[0]).is_integer() and np.log2(B.shape[1]).is_integer()):
        raise ValueError("The dimensions of the matrices must be powers of 2.")

    # Base case: if the matrices are 1x1, return their product
    if A.shape[0] == 1 and B.shape[1] == 1:
        return A * B

    # Split the matrices into quadrants
    mid = A.shape[0] // 2
    A11, A12 = A[:mid, :mid], A[:mid, mid:]
    A21, A22 = A[mid:, :mid], A[mid:, mid:]
    B11, B12 = B[:mid, :mid], B[:mid, mid:]
    B21, B22 = B[mid:, :mid], B[mid:, mid:]

    # Compute the 7 products using Strassen's formulas
    M1 = strassen(A11 + A22, B11 + B22)
    M2 = strassen(A21 + A22, B11)
    M3 = strassen(A11, B12 - B22)
    M4 = strassen(A22, B21 - B11)
    M5 = strassen(A11 + A12, B22)
    M6 = strassen(A21 - A11, B11 + B12)
    M7 = strassen(A12 - A22, B21 + B22)

    # Compute the four quadrants of the final product
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    # Combine the four quadrants into a single matrix
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))

    return C
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

