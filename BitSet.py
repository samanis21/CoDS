class BitSet:
    def __init__(self, size):
        self.size = size
        self.bitset = bytearray((size + 7) // 8)

    def add(self, index):
        byte_index = index // 8
        bit_index = index % 8
        self.bitset[byte_index] |= 1 << bit_index

    def contains(self, index):
        byte_index = index // 8
        bit_index = index % 8
        return (self.bitset[byte_index] & (1 << bit_index)) != 0
