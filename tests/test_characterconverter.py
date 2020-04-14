import unittest
from migemo.characterconverter import *


class TestCharacterConverter(unittest.TestCase):
    def test_character_converter(self):
        self.assertEqual('アイウエオ', han2zen('ｱｲｳｴｵ'))
        self.assertEqual('ｱｲｳｴｵ', zen2han('アイウエオ'))
        self.assertEqual('アイウエオ', hira2kata('あいうえお'))


if __name__ == '__main__':
    unittest.main()
