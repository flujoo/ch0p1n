import unittest
from ch0p1n.elaborate import embellish


class TestEmbellish(unittest.TestCase):
    def test(self):
        motif = [[60, [64, 67], None]]
        scale = [0, 2, 4, 5, 7, 9, 11]
        out = embellish(motif, (0, 1, 0), (0, 0), scale, 1)
        expected = [[60, [62, 67], None]]
        self.assertEqual(out, expected)
