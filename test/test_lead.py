import unittest
from ch0p1n.lead import get_nearest_pitches, lead


class Test_get_nearest_pitches(unittest.TestCase):
    # C4
    pitch = 60

    # G, B, D
    harmony = [7, 11, 2]

    def test_None(self):
        out = get_nearest_pitches(None, self.harmony)
        expected = [None]
        self.assertEqual(out, expected)

    def test_semitone_0(self):
        out = get_nearest_pitches(self.pitch, self.harmony, [0])
        expected = []
        self.assertEqual(out, expected)

    def test_semitone_1(self):
        out = get_nearest_pitches(self.pitch, self.harmony, range(-1, 2))
        expected = [59]
        self.assertEqual(out, expected)

    def test_semitone_2(self):
        out = get_nearest_pitches(self.pitch, self.harmony, range(-2, 3))
        expected = [59, 62]
        self.assertEqual(out, expected)


class Test_lead(unittest.TestCase):
    def test(self):
        motif = [[None, 60], [[64, 67]]]
        harmony = [7, 11, 2]
        out = lead(motif, harmony)
        expected = [
            [[None, 62], [[62, 67]]],
            [[None, 59], [[62, 67]]]
        ]
        self.assertCountEqual(out, expected)
