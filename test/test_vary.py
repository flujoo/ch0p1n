import unittest
from ch0p1n.vary import rescale


class TestRescale(unittest.TestCase):
    def test(self):
        motif = [[60], [[59, 61], None]]
        mapping = {0: 11, 11: 0, 1: 10}
        out = rescale(motif, mapping)
        expected = [[59], [[60, 58], None]]
        self.assertEqual(out, expected)
