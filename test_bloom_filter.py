import pytest
from BloomFilter import BloomFilter


def test_add_and_contains():
    bf = BloomFilter(100, 0.01)
    bf.add("hello")
    assert bf.contains("hello")
    assert not bf.contains("world")

def test_false_positives():
    bf = BloomFilter(1000, 0.01)
    for i in range(500):
        bf.add(f"item{i}")
    false_positives = sum(1 for i in range(500, 1000) if bf.contains(f"item{i}"))
    assert false_positives < 50  # Expecting < 5% false positives

def test_large_data_performance():
    bf = BloomFilter(100000, 0.01)
    for i in range(10000):
        bf.add(f"item{i}")
    for i in range(10000, 20000):
        assert not bf.contains(f"item{i}")

def test_random_strings():
    import random, string
    bf = BloomFilter(1000, 0.01)
    for _ in range(1000):
        bf.add(''.join(random.choices(string.ascii_lowercase, k=10)))
    for _ in range(1000):
        assert not bf.contains(''.join(random.choices(string.ascii_lowercase, k=10)))

def test_varying_sizes():
    sizes = [10, 100, 1000, 10000, 100000]
    for size in sizes:
        bf = BloomFilter(size, 0.01)
        for i in range(size):
            bf.add(f"item{i}")
        for i in range(size):
            assert bf.contains(f"item{i}")
        assert not bf.contains("non_existing_item")
