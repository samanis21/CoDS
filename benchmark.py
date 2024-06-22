import time
import os
import psutil
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
from BloomFilter import BloomFilter

def memory_usage_psutil():
    """Return the memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 ** 2

def cpu_usage_psutil():
    """Return the CPU usage as a percentage."""
    process = psutil.Process(os.getpid())
    return process.cpu_percent(interval=0.1)

def worker(args, result_queue):
    size, hash_count, num_elements = args
    bloom_filter = BloomFilter(size, hash_count)
    elements = np.arange(num_elements, dtype=int)

    # Benchmark insertion
    start_time = time.time()
    start_mem = memory_usage_psutil()
    start_cpu = cpu_usage_psutil()
    for element in map(str, elements):
        bloom_filter.add(element)
    add_time = time.time() - start_time
    add_mem = memory_usage_psutil() - start_mem
    add_cpu = cpu_usage_psutil() - start_cpu

    # Benchmark search
    start_time = time.time()
    start_mem = memory_usage_psutil()
    start_cpu = cpu_usage_psutil()
    for element in map(str, elements):
        bloom_filter.contains(element)
    check_time = time.time() - start_time
    check_mem = memory_usage_psutil() - start_mem
    check_cpu = cpu_usage_psutil() - start_cpu

    result_queue.put((size, hash_count, add_time, check_time, add_mem, check_mem, add_cpu, check_cpu))

if __name__ == "__main__":
    from BloomFilter import BloomFilter

    # Specify the output directory
    output_dir = '/vsc-hard-mounts/leuven-user/363/vsc36394/V3'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sizes = [1000, 5000, 10000, 50000, 100000]
    hash_counts = [3, 5, 7]
    arguments = [(size, hash_count, size) for size in sizes for hash_count in hash_counts]

    results = []
    for args in arguments:
        result_queue = Queue()
        p = Process(target=worker, args=(args, result_queue))
        p.start()
        results.append(result_queue.get())
        p.join()

    # Plotting the results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Insertion time plot
    ax1.set_title('Bloom Filter Insertion Time')
    ax1.set_xlabel('Size')
    ax1.set_ylabel('Time (seconds)')
    for hash_count in hash_counts:
        insertion_times = [result[2] for result in results if result[1] == hash_count]
        ax1.plot(sizes, insertion_times, label=f"{hash_count} hash functions")
    ax1.legend()

    # Search time plot
    ax2.set_title('Bloom Filter Search Time')
    ax2.set_xlabel('Size')
    ax2.set_ylabel('Time (seconds)')
    for hash_count in hash_counts:
        search_times = [result[3] for result in results if result[1] == hash_count]
        ax2.plot(sizes, search_times, label=f"{hash_count} hash functions")
    ax2.legend()

    # Save the plot and results
    plt.savefig(os.path.join(output_dir, 'benchmark_results.png'))
    with open(os.path.join(output_dir, 'benchmark_results.txt'), 'w') as f:
        for result in results:
            f.write(f"Bloom Filter Size: {result[0]}\n")
            f.write(f"Number of Hash Functions: {result[1]}\n")
            f.write(f"Insertion Time (seconds): {result[2]}\n")
            f.write(f"Search Time (seconds): {result[3]}\n")
            f.write(f"Insertion Memory Usage (MB): {result[4]}\n")
            f.write(f"Search Memory Usage (MB): {result[5]}\n")
            f.write(f"Insertion CPU Usage (%): {result[6]}\n")
            f.write(f"Search CPU Usage (%): {result[7]}\n")
            f.write("\n")

    plt.show()