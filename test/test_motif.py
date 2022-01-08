import unittest
from ch0p1n.motif import (
    _reify,
    _move,
    _move2,
    _extract,
    _replace,
    rescale,
    transpose,
    _access,
    is_complete,
    is_similar,
    divide,
    elaborate,
    to_pitch_line
)


class Test_move(unittest.TestCase):
    pitch = 60
    scale = _reify([11])

    def test_none(self):
        out = _move(None, self.scale, 1)
        self.assertIsNone(out)

    def test_step_0(self):
        out = _move(self.pitch, self.scale, 0)
        self.assertIsNone(out)

    def test_step_minus_1(self):
        out = _move(self.pitch, self.scale, -1)
        expected = 59
        self.assertEqual(out, expected)

    def test_step_1(self):
        out = _move(self.pitch, self.scale, 1)
        expected = 71
        self.assertEqual(out, expected)


class Test_move2(unittest.TestCase):
    def test(self):
        out = _move2(60, _reify([11]), [-1, 0, 1])
        expected = [59, 71]
        self.assertEqual(out, expected)


class Test_extract(unittest.TestCase):
    def test(self):
        motif = [62, [63, 64], None]
        out = _extract(motif)
        expected = [62, 63, 64, None]
        self.assertEqual(out, expected)


class Test_replace(unittest.TestCase):
    def test(self):
        motif = [62, [63, 64], None]
        pitches = [6.2, 6.3, 6.4, 6.5]
        out = _replace(motif, pitches)
        expected = [6.2, [6.3, 6.4], 6.5]
        self.assertEqual(out, expected)


class TestRescale(unittest.TestCase):
    def test(self):
        motif = [60, [59, 61], None]
        mapping = {0: 11, 11: 0, 1: 10}
        out = rescale(motif, mapping)
        expected = [59, [60, 58], None]
        self.assertEqual(out, expected)


class TestTranspose(unittest.TestCase):
    # C#4, D4, D#4
    motif = [61, [62, 63], None]

    def test_0_step(self):
        out = transpose(self.motif, [0, 4], 0)
        expected = [None, [None, None], None]
        self.assertEqual(out, expected)

    def test_chromatic(self):
        out = transpose(self.motif, list(range(12)), -1)
        expected = [60, [61, 62], None]
        self.assertEqual(out, expected)

    def test_c_major(self):
        scale = [0, 2, 4, 5, 7, 9, 11]
        out = transpose(self.motif, scale, 1)
        expected = [62, [64, 64], None]
        self.assertEqual(out, expected)


class Test_access(unittest.TestCase):
    position = (0, 1)
    pitch_line = [[60, 61], None]
    duration_line = [1, 2]

    def test_pitch_line(self):
        out = _access(self.pitch_line, self.position)
        expected = 61
        self.assertEqual(out, expected)

    def test_pitch_line_list(self):
        out = _access(self.pitch_line, 0)
        expected = [60, 61]
        self.assertEqual(out, expected)

    def test_duration_line(self):
        out = _access(self.duration_line, self.position)
        expected = 1
        self.assertEqual(out, expected)


class TestIsComplete(unittest.TestCase):
    # C4, None, D4, E4, G4
    motif = [60, None, 62, [64, 67]]

    # C, E, G
    harmony = [0, 4, 7]

    def test(self):
        out = is_complete(self.motif, self.harmony)
        self.assertTrue(out)

    def test_exclude(self):
        out = is_complete(self.motif, self.harmony, [(3, 0)])
        self.assertFalse(out)


class TestIsSimilar(unittest.TestCase):
    motif = [60, 50, [70, 40]]
    proto = [60, 50, [40, 60]]

    def test_directions(self):
        out = is_similar(self.motif, self.proto)
        self.assertTrue(out)

    def test_ordinals(self):
        out = is_similar(self.motif, self.proto, method="ordinal")
        self.assertFalse(out)


class TestDivide(unittest.TestCase):
    def test(self):
        pitch_motif = [60, [61, 62], None]
        duration_motif = [1, 2, 3]
        out = divide(pitch_motif, duration_motif, 1, 4)
        expected = (
            [60, [61, 62], [61, 62], [61, 62], [61, 62], None],
            [1, 0.5, 0.5, 0.5, 0.5, 3]
        )
        self.assertEqual(out, expected)


class TestElaborate(unittest.TestCase):
    # Beethoven Sonata No.1
    pitch_motif = [80, 77, None]
    duration_motif = [2, 1, 1]
    scale = [5, 7, 8, 10, 0, 1, 4]
    steps = [-1, -1, -1]

    def test_right(self):
        out = elaborate(self.pitch_motif, self.duration_motif, 0,
            self.scale, self.steps, 'right', 1/4)
        expected = (
            [80, 79, 77, 76, 77, None],
            [1.5, 1/6, 1/6, 1/6, 1, 1]
        )
        self.assertEqual(out, expected)

    def test_right_absolute(self):
        out = elaborate(self.pitch_motif, self.duration_motif, 0,
            self.scale, self.steps, 'right', 1/4, False)
        expected = (
            [80, 79, 79, 79, 77, None],
            [1.5, 1/6, 1/6, 1/6, 1, 1]
        )
        self.assertEqual(out, expected)

    def test_right_chord(self):
        pitch_motif = [[80, 84], 77, None]
        out = elaborate(pitch_motif, self.duration_motif, 0,
            self.scale, self.steps, 'right', 1/4)
        expected = (
            [[80, 84], [79, 82], [77, 80], [76, 79], 77, None],
            [1.5, 1/6, 1/6, 1/6, 1, 1]
        )
        self.assertEqual(out, expected)

    def test_left(self):
        out = elaborate(self.pitch_motif, self.duration_motif, 0,
            self.scale, self.steps, 'left')
        expected = (
            [76, 77, 79, 80, 77, None],
            [0.5, 0.5, 0.5, 0.5, 1, 1]
        )
        self.assertEqual(out, expected)


class TestToPitchLine(unittest.TestCase):
    def test(self):
        notation_line = [60, 'B-5', None, [61, 'c##2']]
        to_pitch_line(notation_line)
        expected = [60, 82, None, [61, 38]]
        self.assertEqual(notation_line, expected)
