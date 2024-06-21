class Bitset:
    def __init__(self, size):
        self.size = size
        self.bitset = [0] * size

    def set(self, pos):
        self.bitset[pos] = 1

    def get(self, pos):
        return self.bitset[pos]
