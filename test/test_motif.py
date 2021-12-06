import unittest
from ch0p1n.motif import flatten, replace


motif = [[60, 61], [62, [63, 64]]]


class Test_flatten(unittest.TestCase):
    def test(self):
        out = flatten(motif)
        expected = [60, 61, 62, 63, 64]
        self.assertEqual(out, expected)


class Test_replace(unittest.TestCase):
    def test(self):
        out = replace(motif, [6, 6.1, 6.2, 6.3, 6.4])
        expected = [[6, 6.1], [6.2, [6.3, 6.4]]]
        self.assertEqual(out, expected)
