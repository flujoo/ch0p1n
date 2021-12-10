import unittest
from ch0p1n.transpose import transpose, localize


class Test_transpose(unittest.TestCase):
    # C#4, D4, D#4
    motif = [[61, [62, 63], None]]

    def test_step_0(self):
        out = transpose(self.motif, [0, 4], 0)
        expected = self.motif
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


class Test_localize(unittest.TestCase):
    def test(self):
        motif = [[60, [64, 67], None]]
        scale = [0, 2, 4, 5, 7, 9, 11]
        localize(motif, (0, 1, 0), (0, 0), scale, 1)
        expected = [[60, [62, 67], None]]
        self.assertEqual(motif, expected)
