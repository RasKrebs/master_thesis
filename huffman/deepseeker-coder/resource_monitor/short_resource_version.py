import psutil
import os
import threading
import multiprocessing

# Define a global variable to store the maximum resources usage
max_resources_usage = {"cpu": 0, "memory": 0}


import requests

book_url = "https://www.gutenberg.org/cache/epub/1513/pg1513-images.html"
response = requests.get(book_url)
text = response.text


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



import heapq
import os
from collections import defaultdict

def calculate_frequency(message):
    frequency = defaultdict(int)
    for symbol in message:
        frequency[symbol] += 1
    return frequency

def build_huffman_tree(frequency):
    heap = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def huffman_encoding(message):
    frequency = calculate_frequency(message)
    huffman_tree = build_huffman_tree(frequency)
    huffman_codes = {symbol: code for symbol, code in huffman_tree}
    encoded_message = ''.join(huffman_codes[symbol] for symbol in message)
    return encoded_message, huffman_codes

def huffman_decoding(encoded_message, huffman_codes):
    reverse_huffman_codes = {v: k for k, v in huffman_codes.items()}
    decoded_message = ''
    while encoded_message:
        for code in reverse_huffman_codes:
            if encoded_message.startswith(code):
                decoded_message += reverse_huffman_codes[code]
                encoded_message = encoded_message[len(code):]
    return decoded_message

def execute(text):
    if not isinstance(text, str):
        raise ValueError("Input data must be a string.")  # Ensure the input is a string
    
    root = huffman_encoding(text)  # Generate the Huffman tree from the input text
    return root



if __name__ == "__main__":
    # Start the resource monitoring in a separate thread
    global monitoring
    monitoring = True
    monitor_thread = threading.Thread(target=resource_monitor)
    monitor_thread.start()

    # Execute the Huffman coding process
    huffman_codes = execute(text)


    # Stop the monitoring
    monitoring = False
    monitor_thread.join()

    print(max_resources_usage['cpu']), print(max_resources_usage['memory'] / (1024**2))

