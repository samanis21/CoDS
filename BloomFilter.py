import math
import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(False)

    def add(self, element):
        for i in range(self.hash_count):
            hash_value = mmh3.hash(element, i) % self.size
            self.bit_array[hash_value] = True

    def contains(self, element):
        for i in range(self.hash_count):
            hash_value = mmh3.hash(element, i) % self.size
            if not self.bit_array[hash_value]:
                return False
        return True