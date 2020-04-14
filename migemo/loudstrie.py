import array
from typing import Generator, Optional

import bisect
from . import bitvector


class LOUDSTrie:
    def __init__(self, bit_vector: bitvector.BitVector, edges: array.array):
        if edges.typecode != 'H':
            raise Exception
        self.bit_vector = bit_vector
        self.edges = edges

    def get_key(self, index: int) -> Optional[str]:
        if index <= 0 or len(self.edges) <= index:
            return None
        sb = []
        while index > 1:
            sb.append(chr(self.edges[index]))
            index = self.parent(index)
        if not sb:
            return ''
        else:
            sb.reverse()
            return ''.join(sb)

    def get(self, key: str) -> int:
        index = 1
        for i in range(len(key)):
            c = key[i]
            index = self.traverse(index, c)
            if index == -1:
                break
        if index >= 0:
            return index
        else:
            return -1

    def parent(self, x: int) -> int:
        return self.bit_vector.rank(self.bit_vector.select(x, True), False)

    def first_child(self, x: int) -> int:
        y = self.bit_vector.select(x, False) + 1
        if self.bit_vector.get(y):
            return self.bit_vector.rank(y, True) + 1
        return -1

    def traverse(self, index: int, c: chr) -> int:
        child = self.first_child(index)
        if child == -1:
            return -1
        start = self.bit_vector.select(child, True)
        end = self.bit_vector.next_clear_bit(start)
        size = end - start - 1
        result = bisect.bisect_left(self.edges, ord(c), child, child + size)
        if self.edges[result] == ord(c):
            return result
        else:
            return -1

    def visit_depth_first(self, index: int) -> Generator[int, None, None]:
        yield index
        child = self.first_child(index)
        if child == -1:
            return
        child_pos = self.bit_vector.select(child, True)
        while self.bit_vector.get(child_pos):
            yield from self.visit_depth_first(child)
            child = child + 1
            child_pos = child_pos + 1
