import unittest

from migemo.bitvector import BitVector


class TestBitVector(unittest.TestCase):
    def test_bit_count(self):
        self.assertEqual(BitVector.bit_count(1), 1)
        self.assertEqual(BitVector.bit_count(3), 2)
        self.assertEqual(BitVector.bit_count(0xfffffffffffffffff), 64)

    def test_number_of_tailing_zeros(self):
        self.assertEqual(BitVector.number_of_tailing_zeros(0), 64)
        self.assertEqual(BitVector.number_of_tailing_zeros(1), 0)
        self.assertEqual(BitVector.number_of_tailing_zeros(2), 1)
        self.assertEqual(BitVector.number_of_tailing_zeros(4), 2)
        self.assertEqual(BitVector.number_of_tailing_zeros(0x8000000000000000), 63)


if __name__ == '__main__':
    unittest.main()
