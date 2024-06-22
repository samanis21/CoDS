import time
import psutil
import matplotlib.pyplot as plt
from BloomFilter import BloomFilter
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import os

output_dir = '/vsc-hard-mounts/leuven-user/363/vsc36394/V2'
def random_string(length=10):
    import string
    import random
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def memory_usage_psutil():
    process = psutil.Process()
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem

def cpu_usage_psutil():
    process = psutil.Process()
    return process.cpu_percent(interval=1.0)

def benchmark_bloom_filter(size, hash_count, num_elements):
    bloom_filter = BloomFilter(size, hash_count)
    elements = [f"element_{i}" for i in range(num_elements)]

    # Benchmark insertion
    start_time = time.time()
    start_mem = memory_usage_psutil()
    start_cpu = cpu_usage_psutil()
    for element in elements:
        bloom_filter.add(element)
    add_time = time.time() - start_time
    add_mem = memory_usage_psutil() - start_mem
    add_cpu = cpu_usage_psutil() - start_cpu

    # Benchmark search
    start_time = time.time()
    start_mem = memory_usage_psutil()
    start_cpu = cpu_usage_psutil()
    for element in elements:
        bloom_filter.contains(element)
    check_time = time.time() - start_time
    check_mem = memory_usage_psutil() - start_mem
    check_cpu = cpu_usage_psutil() - start_cpu

    return add_time, check_time, add_mem, check_mem, add_cpu, check_cpu

def plot_benchmark(results, filename):
    sizes, insertion_times, search_times, _, _, _, _ = zip(*results)
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, insertion_times, label='Insertion Time')
    plt.plot(sizes, search_times, label='Search Time')
    plt.xlabel('Number of Elements')
    plt.ylabel('Time (seconds)')
    plt.title('Bloom Filter Benchmark')
    plt.legend()
    try:
        output_file = os.path.join(output_dir, filename)
        plt.savefig(output_file, dpi=300)
        print(f"Benchmark plot saved to: {filename}")
    except Exception as e:
        print(f"Error saving benchmark plot: {e}")
   
    

if __name__ == "__main__":
    sizes = [1000, 5000, 10000, 50000, 100000]
    hash_count = 5
    results = []

    for size in sizes:
        add_time, check_time, add_mem, check_mem, add_cpu, check_cpu = benchmark_bloom_filter(size, hash_count, size)
        results.append((size, add_time, check_time, add_mem, check_mem, add_cpu, check_cpu))

    plot_benchmark(results, 'benchmark.png')
    output_file = os.path.join(output_dir, 'benchmark_results.txt')
    with open(output_file, 'w') as f:
        for size, add_time, check_time, add_mem, check_mem, add_cpu, check_cpu in results:
            f.write(f"Size: {size}, Insertion Time: {add_time}, Search Time: {check_time}, Insertion Memory: {add_mem}, Search Memory: {check_mem}, Insertion CPU: {add_cpu}, Search CPU: {check_cpu}\n")