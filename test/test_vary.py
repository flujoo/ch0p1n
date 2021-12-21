import unittest
from ch0p1n.vary import rescale, transpose


class TestRescale(unittest.TestCase):
    def test(self):
        motif = [[60], [[59, 61], None]]
        mapping = {0: 11, 11: 0, 1: 10}
        out = rescale(motif, mapping)
        expected = [[59], [[60, 58], None]]
        self.assertEqual(out, expected)


class TestTranspose(unittest.TestCase):
    # C#4, D4, D#4
    motif = [[61, [62, 63], None]]

    def test_0_step(self):
        out = transpose(self.motif, [0, 4], 0)
        expected = [[None, [None, None], None]]
        self.assertEqual(out, expected)

    def test_chromatic(self):
        out = transpose(self.motif, list(range(12)), -1)
        expected = [[60, [61, 62], None]]
        self.assertEqual(out, expected)

    def test_c_major(self):
        scale = [0, 2, 4, 5, 7, 9, 11]
        out = transpose(self.motif, scale, 1)
        expected = [[62, [64, 64], None]]
        self.assertEqual(out, expected)
