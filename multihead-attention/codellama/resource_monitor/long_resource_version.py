import psutil
import os
import threading
import multiprocessing

# Define a global variable to store the maximum resources usage
max_resources_usage = {"cpu": 0, "memory": 0}


import numpy as np
import random

np.random.seed(42)
seq_length = 100 
batch_size = 32
emb_size = 512
num_heads = 8 


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



import math
from typing import Optional, Tuple

class MultiHeadAttention:
    def __init__(self, emb_size: int, num_heads: int):
        """Initialize the multi-head attention layer with the given parameters."""
        assert emb_size % num_heads == 0, "Embedding size should be divisible by number of heads"
        self.emb_size = emb_size
        self.num_heads = num_heads

        # Initialize query, key, value, and output projection weights
        self.wq = [[random() for _ in range(emb_size)] for _ in range(emb_size)]
        self.wk = [[random() for _ in range(emb_size)] for _ in range(emb_size)]
        self.wv = [[random() for _ in range(emb_size)] for _ in range(emb_size)]
        self.wo = [[random() for _ in range(emb_size)] for _ in range(emb_size)]

    def scaled_dot_product_attention(self, query: list, key: list, value: list) -> Tuple[list, list]:
        """Calculate the attention weights and apply them to the value tensor."""
        depth = len(query[0])  # Get the depth of a single head (d_k)
        dots = [sum(q * k for q, k in zip(qs, ks)) for qs, ks in zip(query, key)]  # Calculate dot products between query and key matrices
        scaled_dots = [dot / math.sqrt(depth) for dot in dots]  # Scale the dot products by sqrt(d_k)

        # Apply softmax to ensure that attention weights sum up to 1 (for stability)
        unnormalized_alphas = [math.exp(dot) for dot in scaled_dots]
        normalization_factor = sum(unnormalized_alphas)
        alphas = [alpha / normalization_factor for alpha in unnormalized_alphas]  # Normalize the attention weights

        # Apply attention weights to value tensor and return the result (attention output)
        attn_output = []
        for row, alpha in zip(value, alphas):
            attn_output.append([alpha * v for v in row])
        return attn_output, alphas

    def split_heads(self, x: list) -> list:
        """Split the input tensor into multiple heads."""
        head_size = len(x[0]) // self.num_heads  # Calculate the size of a single head (d_v)

        # Split the input matrix into multiple sub-matrices, each representing a single head
        x_split = []
        for start in range(self.num_heads):
            head = [x[i][start * head_size:(start + 1) * head_size] for i in range(len(x))]
            x_split.append(head)

        return x_split

    def merge_heads(self, x: list) -> list:
        """Merge the input tensor from multiple heads into a single matrix."""
        head_size = len(x[0][0])  # Get the size of a single head (d_v)

        # Merge the sub-matrices representing individual heads into a single matrix
        x_merged = []
        for start in range(len(x)):
            row = [x[i][start] for i in range(self.num_heads)]
            merged_row = []
            for i in range(head_size):
                merged_row += [col[i] for col in row]
            x_merged.append(merged_row)

        return x_merged

    def forward(self, query: list, key: Optional[list] = None, value: Optional[list] = None):
        """Forward pass of the multi-head attention layer."""
        if key is None:  # If key is not provided, use query as key
            key = query
        if value is None:  # If value is not provided, use query as value
            value = query

        # Apply projection weights to input tensors (query, key, and value)
        q = [[sum(a * b for a, b in zip(row, w)) for w in self.wq] for row in query]
        k = [[sum(a * b for a, b in zip(row, w)) for w in self.wk] for row in key]
        v = [[sum(a * b for a, b in zip(row, w)) for w in self.wv] for row in value]

        # Split input tensors into multiple heads
        q_split = self.split_heads(q)
        k_split = self.split_heads(k)
        v_split = self.split_heads(v)

        attn_outputs, alphas = [], []  # Initialize empty lists for attention outputs and weights
        for i in range(self.num_heads):
            qs, ks, vs = q_split[i], k_split[i], v_split[i]  # Process each head individually

            attn_output, alpha = self.scaled_dot_product_attention(qs, ks, vs)
            attn_outputs.append(attn_output)
            alphas.append(alpha)

        attn_output = self.merge_heads(attn_outputs)  # Merge attention outputs from multiple heads into a single matrix
        output = [[sum(a * b for a, b in zip(row, w)) for w in self.wo] for row in attn_output]

        return output, alphas  # Return the result and attention weights (alphas)
def execute(batch_size, emb_size, num_heads, seq_length):
    """
    Executes the MultiHeadAttention model with generated input data.
    
    Args:
        batch_size (int): The number of samples in the batch.
        emb_size (int): The size of each input embedding vector.
        num_heads (int): The number of attention heads.
    
    Returns:
        ndarray: The output from the MultiHeadAttention model.
    """
    # Load the data
    data = np.random.rand(batch_size, seq_length, emb_size)
    
    # Initialize the MultiHeadAttention model
    model = MultiHeadAttention(emb_size=emb_size, num_heads=num_heads)
    
    # Perform the forward pass and return the output
    output = model.forward(data)
    return output



if __name__ == "__main__":
    # Start the resource monitoring in a separate thread
    global monitoring
    monitoring = True
    monitor_thread = threading.Thread(target=resource_monitor)
    monitor_thread.start()

    # Execute the Huffman coding process

    # Using the execute function
    output = execute(batch_size, emb_size, num_heads, seq_length)


    # Stop the monitoring
    monitoring = False
    monitor_thread.join()

    print(max_resources_usage['cpu']), print(max_resources_usage['memory'] / (1024**2))

