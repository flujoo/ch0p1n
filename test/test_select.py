import unittest
from ch0p1n.select import is_complete, is_isomorphic


class Test_is_complete(unittest.TestCase):
    # C4, None, D4, E4, G4
    motif = [[60, None, 62], [64, 67]]

    # C, E, G
    harmony = [0, 4, 7]

    def test(self):
        out = is_complete(self.motif, self.harmony)
        self.assertTrue(out)

    def test_exclude(self):
        out = is_complete(self.motif, self.harmony, [(1, 0)])
        self.assertFalse(out)


class Test_is_isomorphic(unittest.TestCase):
    motif = [[60, 50, [70, 40]]]
    proto = [[60, 50, [40, 60]]]

    def test_contour(self):
        out = is_isomorphic(self.motif, self.proto)
        self.assertTrue(out)

    def test_ordinals(self):
        out = is_isomorphic(self.motif, self.proto, method="ordinals")
        self.assertFalse(out)
