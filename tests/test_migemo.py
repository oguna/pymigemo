from unittest import TestCase
import unittest
import migemo


class TestMigemo(TestCase):
    def test_parse_query(self):
        self.assertEqual(['abc'], migemo.Migemo.parse_query('abc'))
        self.assertEqual(['a', 'Bc'], migemo.Migemo.parse_query('aBc'))
        self.assertEqual(['AB', 'c'], migemo.Migemo.parse_query('ABc'))
        self.assertEqual(['kensaku', 'Kensaku'], migemo.Migemo.parse_query('kensakuKensaku'))
        self.assertEqual(['kensaku', 'kensaku'], migemo.Migemo.parse_query('kensaku kensaku'))


if __name__ == '__main__':
    unittest.main()

