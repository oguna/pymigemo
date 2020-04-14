from unittest import TestCase
from migemo.regexgenerator import RegexGenerator
from migemo.regexoperator import *
import unittest


class TestRegexGenerator(TestCase):
    def test_0(self):
        rg = RegexGenerator(RegexOperators.DEFAULT.value)
        rg.add('a')
        rg.add('b')
        rg.add('c')
        self.assertEqual('[cba]', rg.generate())

    def test_1(self):
        rg = RegexGenerator(RegexOperators.DEFAULT.value)
        self.assertEqual('', rg.generate())

    def test_2(self):
        rg = RegexGenerator(RegexOperators.DEFAULT.value)
        rg.add('ab')
        rg.add('ac')
        rg.add('z')
        self.assertEqual('(z|a[cb])', rg.generate())


if __name__ == '__main__':
    unittest.main()
