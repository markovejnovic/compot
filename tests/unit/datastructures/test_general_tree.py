#!/usr/bin/env python

import unittest
from compot.datastructures import GeneralTree

class TestGeneralTreeApply(unittest.TestCase):
    def test_node(self):
        """Tests whether a tree with a single node behaves as expected."""
        actual = GeneralTree(3).apply(lambda i: 3 * i)
        expected = GeneralTree(9)
        self.assertEqual(expected, actual)

    def test_1l(self):
        """Tests whether a tree with one level works"""
        actual = GeneralTree(3, [
            GeneralTree(2),
            GeneralTree(4)
        ]).apply(lambda i: 3 + i)
        expected = GeneralTree(6, [
            GeneralTree(5),
            GeneralTree(7)
        ])
        self.assertEqual(expected, actual)

    def test_2l(self):
        """Tests whether a tree with two levels works."""
        actual = GeneralTree(3, [
            GeneralTree(2),
            GeneralTree(4, [GeneralTree(10)])
        ]).apply(lambda i: 3 + i)
        expected = GeneralTree(6, [
            GeneralTree(5),
            GeneralTree(7, [GeneralTree(13)])
        ])
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
