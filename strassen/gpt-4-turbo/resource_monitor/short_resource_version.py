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

def split(matrix):
    """
    Splits a given matrix into quarters.
    """
    row, col = matrix.shape
    row2, col2 = row//2, col//2
    return matrix[:row2, :col2], matrix[:row2, col2:], matrix[row2:, :col2], matrix[row2:, col2:]

def strassen(x, y):
    """
    Computes matrix product by divide and conquer approach, recursively.
    """
    if len(x) == 1:
        return x * y

    # Splitting the matrices into quadrants. This will be done recursively
    # until the base case is reached.
    a, b, c, d = split(x)
    e, f, g, h = split(y)

    # Computing the 7 products, recursively (p1, p2...p7).
    p1 = strassen(a, f - h)
    p2 = strassen(a + b, h)        
    p3 = strassen(c + d, e)        
    p4 = strassen(d, g - e)        
    p5 = strassen(a + d, e + h)        
    p6 = strassen(b - d, g + h)  
    p7 = strassen(a - c, e + f) 

    # Re-combining the 7 products to get the final result.
    upper_left = p5 + p4 - p2 + p6
    upper_right = p1 + p2
    lower_left = p3 + p4
    lower_right = p1 + p5 - p3 - p7

    # Combining the 4 results into a single matrix by stacking horizontally and vertically.
    top = np.hstack((upper_left, upper_right))
    bottom = np.hstack((lower_left, lower_right))
    return np.vstack((top, bottom))

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

