class Bitset:
    def __init__(self, size):
        self.size = size
        self.bitset = [0] * size

    def set(self, pos):
        if pos < 0 or pos >= self.size:
            raise IndexError("Bitset index out of range")
        self.bitset[pos] = 1

    def get(self, pos):
        if pos < 0 or pos >= self.size:
            raise IndexError("Bitset index out of range")
        return self.bitset[pos]

    def clear(self, pos):
        if pos < 0 or pos >= self.size:
            raise IndexError("Bitset index out of range")
        self.bitset[pos] = 0

    def __str__(self):
        return ''.join(map(str, self.bitset))