# Bloom Filter Implementation

## Description

This project implements a Bloom Filter in Python using the `bitarray` library and the MurmurHash3 (`mmh3`) hashing algorithm. A Bloom Filter is a probabilistic data structure that allows for efficient set membership checks with a configurable false positive rate.

## Project Files

### BloomFilter.py
This file contains the main implementation of the Bloom Filter using the `bitarray` library and MurmurHash3 hashing functions.

### BitSet.py
This file contains a simple `Bitset` class to handle bit array operations. It includes methods to set, get, and clear bits in the array.

### benchmark.py
This script benchmarks the performance of the Bloom Filter implementation by measuring time, memory, and CPU usage for insertion and search operations. It also generates performance plots.

### test_bloom_filter.py
This file contains test cases using the `pytest` framework to verify the correctness of the Bloom Filter implementation, including tests for false positives and performance with large datasets.

### jobscript_unix
This is a job script for running the benchmark on HPC infrastructure. It specifies job requirements and environment setup, and runs the benchmark script.

## Usage

### BloomFilter.py
To use the Bloom Filter, import the `BloomFilter` class and create an instance with the desired size and number of hash functions:

##python
from BloomFilter import BloomFilter

# Create a Bloom filter with size 1000 and 3 hash functions
bf = BloomFilter(size=1000, hash_count=3)

# Add an element
bf.add("hello")

# Check if an element is in the Bloom filter
print(bf.contains("hello"))  # Output: True
print(bf.contains("world"))  # Output: False


### benchmark.py
The `benchmark.py` script can be run to benchmark the Bloom Filter implementation. It will output performance metrics and generate plots.

##sh
python benchmark.py


### test_bloom_filter.py
To run the test cases, use the following command:

##sh
pytest test_bloom_filter.py


### jobscript_unix
To submit the job script to an HPC cluster, use the `sbatch` command:

##sh
sbatch jobscript_unix


## Benchmarking

The `benchmark.py` script benchmarks the Bloom Filter by measuring the time, memory, and CPU usage for insertion and search operations with different sizes and numbers of hash functions. The results are saved in `benchmark_results.txt` and plotted in `benchmark_results.png`.

## Performance Metrics

### Time Complexity
- Insertion and Lookup: O(k), where k is the number of hash functions.

### Space Complexity
- Bit Array: O(m), where m is the size of the bit array.

## Future Work

- Extended performance tests on different datasets.
- Integration with Jupyter notebooks for demonstration purposes.

