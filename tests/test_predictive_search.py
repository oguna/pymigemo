from unittest import TestCase
import unittest
import migemo.romajiconverter


class TestPredictiveSearch(TestCase):
    def test_convert_romaji_to_hiragana(self):
        self.assertEqual('あ', migemo.romajiconverter.convert_romaji_to_hiragana('a'))
        self.assertEqual('z', migemo.romajiconverter.convert_romaji_to_hiragana('z'))
        self.assertEqual('あいうえお', migemo.romajiconverter.convert_romaji_to_hiragana('aiueo'))
        self.assertEqual('ん', migemo.romajiconverter.convert_romaji_to_hiragana('n'))


if __name__ == '__main__':
    unittest.main()

