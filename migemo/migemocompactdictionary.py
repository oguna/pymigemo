import array
import struct
from os import path
from typing import List
import sys

from . import bitvector
from . import loudstrie


class MigemoCompactDictionary:
    def __init__(self, file):
        self.key_trie = MigemoCompactDictionary.read_louds_trie(file, True)
        self.value_trie = MigemoCompactDictionary.read_louds_trie(file, False)
        self.mapping_bit_vector = MigemoCompactDictionary.read_bit_vector(file)
        size = struct.unpack('>i', file.read(4))[0]
        self.mapping = array.array('L')
        self.mapping.fromfile(file, size)
        if sys.byteorder == 'little':
            self.mapping.byteswap()

    @staticmethod
    def read_bit_vector(bf) -> bitvector.BitVector:
        size = struct.unpack('>I', bf.read(4))[0]
        word_size = (size + 63) // 64
        words = array.array('Q')
        words.fromfile(bf, word_size)
        if sys.byteorder == 'little':
            words.byteswap()
        return bitvector.BitVector(words, size)

    @staticmethod
    def read_louds_trie(bf, compact_hiragana: bool) -> loudstrie.LOUDSTrie:
        size = struct.unpack('>i', bf.read(4))[0]
        if compact_hiragana:
            chars = array.array('H')
            for i in range(size):
                chars.append(MigemoCompactDictionary.decode_compact_hiragana(bf.read(1)[0]))
        else:
            chars = array.array('H')
            chars.fromfile(bf, size)
            if sys.byteorder == 'little':
                chars.byteswap()
        bit_vector = MigemoCompactDictionary.read_bit_vector(bf)
        return loudstrie.LOUDSTrie(bit_vector, chars)

    @staticmethod
    def decode_compact_hiragana(c: int) -> int:
        if 0x20 <= c <= 0x7e:
            return c
        elif 0xa1 <= c <= 0xf6:
            return c + 0x3040 - 0xa0
        raise Exception()

    def predictive_search(self, key: str) -> List[str]:
        key_index = self.key_trie.get(key)
        if key_index != -1:
            result = []
            for i in self.key_trie.visit_depth_first(key_index):
                start = self.mapping_bit_vector.select(i, False)
                end = self.mapping_bit_vector.next_clear_bit(start)
                size = end - start - 1
                offset = self.mapping_bit_vector.rank(start, False)
                for j in range(size):
                    result.append(self.value_trie.get_key(self.mapping[start - offset + j]))
            return result
        else:
            return []


if __name__ == '__main__':
    with open(path.dirname(path.abspath(__file__)) + '/migemo-compact-dict', mode='rb') as file:
        dictionary = MigemoCompactDictionary(file)
    line = input('yomi>')
    while line:
        print(dictionary.predictive_search(line))
        line = input('yomi>')
