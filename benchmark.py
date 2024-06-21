import time
import psutil
import random
import string
import matplotlib.pyplot as plt
import sys
import os

print("PYTHONPATH:", sys.path)
print("Current directory contents:", os.listdir(os.getcwd()))

from BloomFilter import BloomFilter

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def memory_usage_psutil():
    process = psutil.Process()
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem

def cpu_usage_psutil():
    process = psutil.Process()
    return process.cpu_percent(interval=1.0)

def benchmark_bloom_filter(capacity, error_rate, num_elements):
    bf = BloomFilter(capacity, error_rate)

    start_time = time.time()
    start_mem = memory_usage_psutil()
    start_cpu = cpu_usage_psutil()

    for _ in range(num_elements):
        bf.add(random_string())

    add_time = time.time() - start_time
    add_mem = memory_usage_psutil() - start_mem
    add_cpu = cpu_usage_psutil() - start_cpu

    start_time = time.time()
    start_mem = memory_usage_psutil()
    start_cpu = cpu_usage_psutil()

    false_positives = 0
    for _ in range(num_elements):
        if bf.contains(random_string()):
            false_positives += 1

    check_time = time.time() - start_time
    check_mem = memory_usage_psutil() - start_mem
    check_cpu = cpu_usage_psutil() - start_cpu

    actual_bit_usage = sum(bin(x).count('1') for x in bf.bitset.bitset)
    compression_rate = actual_bit_usage / bf.bitset.size

    return {
        "add_time": add_time,
        "check_time": check_time,
        "add_mem": add_mem,
        "check_mem": check_mem,
        "add_cpu": add_cpu,
        "check_cpu": check_cpu,
        "false_positive_rate": false_positives / num_elements,
        "compression_rate": compression_rate,
    }

if __name__ == "__main__":
    capacities = [10**5, 10**6, 10**7]
    error_rate = 0.01
    num_elements = 10**5

    results = []
    for capacity in capacities:
        results.append(benchmark_bloom_filter(capacity, error_rate, num_elements))

    # Plotting results
    plt.figure(figsize=(14, 8))

    add_times = [result['add_time'] for result in results]
    check_times = [result['check_time'] for result in results]
    false_positive_rates = [result['false_positive_rate'] for result in results]
    compression_rates = [result['compression_rate'] for result in results]

    plt.subplot(2, 2, 1)
    plt.plot(capacities, add_times, 'o-', label='Add Time')
    plt.ylabel('Add Time (s)')
    plt.xlabel('Capacity')
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(capacities, check_times, 'o-', label='Check Time')
    plt.ylabel('Check Time (s)')
    plt.xlabel('Capacity')
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(capacities, false_positive_rates, 'o-', label='False Positive Rate')
    plt.ylabel('False Positive Rate')
    plt.xlabel('Capacity')
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.plot(capacities, compression_rates, 'o-', label='Compression Rate')
    plt.ylabel('Compression Rate')
    plt.xlabel('Capacity')
    plt.legend()

    plt.tight_layout()
    plt.show()
