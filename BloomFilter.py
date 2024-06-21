import hashlib
import math
from Bitset import Bitset

class BloomFilter:
    def __init__(self, capacity, error_rate):
        self.capacity = capacity
        self.error_rate = error_rate
        self.size = self._get_size(capacity, error_rate)
        self.num_hashes = self._get_num_hashes(capacity, error_rate)
        self.bitset = Bitset(self.size)

    def _hashes(self, item):
        """Generate multiple hash values for the given item."""
        hash1 = int(hashlib.sha256(item.encode('utf-8')).hexdigest(), 16)
        hash2 = int(hashlib.md5(item.encode('utf-8')).hexdigest(), 16)
        for i in range(self.num_hashes):
            yield (hash1 + i * hash2) % self.size

    def add(self, item):
        for pos in self._hashes(item):
            self.bitset.set(pos)

    def contains(self, item):
        return all(self.bitset.get(pos) for pos in self._hashes(item))

    @staticmethod
    def _get_size(capacity, error_rate):
        m = -(capacity * math.log(error_rate)) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def _get_num_hashes(capacity, error_rate):
        k = (math.log(2) * BloomFilter._get_size(capacity, error_rate)) / capacity
        return int(k)
