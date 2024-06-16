from BitSet import BitSet
import mmh3

class BloomFilter:
    def __init__(self, capacity, error_rate=0.01):
        self.size = self._optimal_size(capacity, error_rate)
        self.hash_count = self._optimal_hash_count(capacity, error_rate)
        self.bitset = BitSet(self.size)

    def add(self, item):
        item = str(item)
        for i in range(self.hash_count):
            combined_hash = mmh3.hash(item, i) % self.size
            self.bitset.add(combined_hash)

    def contains(self, item):
        item = str(item)
        for i in range(self.hash_count):
            combined_hash = mmh3.hash(item, i) % self.size
            if not self.bitset.contains(combined_hash):
                return False
        return True

    @staticmethod
    def _optimal_size(capacity, error_rate):
        from math import ceil, log
        return ceil(-(capacity * log(error_rate)) / (log(2) ** 2))

    @staticmethod
    def _optimal_hash_count(capacity, error_rate):
        from math import log
        return round((BloomFilter._optimal_size(capacity, error_rate) / capacity) * log(2))
