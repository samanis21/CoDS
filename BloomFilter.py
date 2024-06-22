import hashlib
from Bitset import Bitset

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bitset = Bitset(size)

    def _hashes(self, item):
        hash_values = []
        for i in range(self.hash_count):
            hash_value = int(hashlib.md5((str(i) + item).encode()).hexdigest(), 16) % self.size
            hash_values.append(hash_value)
        return hash_values

    def add(self, item):
        for hash_value in self._hashes(item):
            self.bitset.set(hash_value)

    def contains(self, item):
        for hash_value in self._hashes(item):
            if not self.bitset.get(hash_value):
                return False
        return True

    def __str__(self):
        return str(self.bitset)