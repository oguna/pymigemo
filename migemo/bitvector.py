import array


class BitVector:
    def __init__(self, words: array.array, size: int):
        self.words = words
        self.sizeInBits = size
        self.lb = array.array('L')
        self.lb.extend(range((self.sizeInBits + 511) // 512))
        self.sb = array.array('H')
        self.sb.extend(range(len(self.lb) * 8))
        s = 0
        s_in_lb = 0
        for i in range(len(self.sb)):
            bit_count = 0
            if i < len(self.words):
                bit_count = BitVector.bit_count(self.words[i])
            self.sb[i] = s_in_lb
            s_in_lb = s_in_lb + bit_count
            if i & 7 == 7:
                self.lb[i >> 3] = s
                s = s + s_in_lb
                s_in_lb = 0

    def rank(self, pos: int, b: bool) -> int:
        if pos < 0 | self.sizeInBits <= pos:
            raise Exception()
        count: int = self.sb[pos // 64] + self.lb[pos // 512]
        word: int = self.words[pos // 64]
        count = count + self.bit_count(word & ((1 << (pos & 63)) - 1))
        if b:
            return count
        else:
            return pos - count

    @staticmethod
    def bit_count(i: int) -> int:
        i = i - ((i >> 1) & 0x5555555555555555)
        i = (i & 0x3333333333333333) + ((i >> 2) & 0x3333333333333333)
        i = (i + (i >> 4)) & 0x0f0f0f0f0f0f0f0f
        i = i + (i >> 8)
        i = i + (i >> 16)
        i = i + (i >> 32)
        return i & 0x7f

    def size(self) -> int:
        return self.sizeInBits

    def get(self, pos: int) -> bool:
        if pos < 0 or self.sizeInBits <= pos:
            raise IndexError()
        return ((self.words[pos >> 6] >> (pos & 63)) & 1) == 1

    def select(self, count: int, b: bool) -> int:
        lb_index = self.lower_bound_binary_search_lb(count, b) - 1
        count_in_lb = count - (self.lb[lb_index] if b else 512 * lb_index - self.lb[lb_index])
        sb_index = self.lower_bound_binary_search_sb(count_in_lb, lb_index * 8, lb_index * 8 + 8, b) - 1
        count_in_sb = count_in_lb - (self.sb[sb_index] if b else 64 * (sb_index % 8) - self.sb[sb_index])
        word = self.words[sb_index]
        for i in range(64):
            if ((word >> i) & 1) == (1 if b else 0):
                count_in_sb = count_in_sb - 1
            if count_in_sb == 0:
                return sb_index * 64 + i
        raise Exception

    def lower_bound_binary_search_lb(self, key: int, b: bool) -> int:
        high = len(self.lb)
        low = -1
        while high - low > 1:
            mid = (high + low) // 2
            if (self.lb[mid] if b else 512 * mid - self.lb[mid]) < key:
                low = mid
            else:
                high = mid
        return high

    def lower_bound_binary_search_sb(self, key: int, start: int, end: int, b: bool) -> int:
        high = end
        low = start - 1
        while high - low > 1:
            mid = (high + low) // 2
            if (self.sb[mid] if b else 64 * (mid % 8) - self.sb[mid]) < key:
                low = mid
            else:
                high = mid
        return high

    def next_clear_bit(self, index: int) -> int:
        if self.sizeInBits <= index:
            return self.sizeInBits
        index = index + 1
        while self.get(index):
            index = index + 1
            if self.sizeInBits == index:
                return self.sizeInBits
        return index
        """
        MASK = 0xffffffffffffffff
        u = index >> 6
        if u >= len(self.words):
            return index
        word = ~self.words[u] & (MASK << (index & 63))
        while True:
            if word != 0:
                return u * 64 + BitVector.number_of_tailing_zeros(word)
            u = u + 1
            if u == len(self.words):
                return 64 * len(self.words)
            word = ~self.words[u]
        """

    @staticmethod
    def number_of_tailing_zeros(i: int) -> int:
        if i == 0:
            return 64
        """
        n = 63
        y = i & 0xFFFFFFFF
        if y != 0:
            n = n - 32
            x = y
        else:
            x = (i >> 32) & 0xFFFFFFFF
        y = x << 16
        if y != 0:
            n = n - 16
            x = y
        y = x << 8
        if y != 0:
            n = n - 8
            x = y
        y = x << 4
        if y != 0:
            n = n - 4
            x = y
        y = x << 2
        if y != 0:
            n = n - 2
            x = y
        return n - ((x << 1) >> 31)
        """
        pos = 0
        while i & 1 == 0:
            pos = pos + 1
            i = i >> 1
        return pos
