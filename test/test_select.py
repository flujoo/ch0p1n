import unittest
from ch0p1n.select import is_complete


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
