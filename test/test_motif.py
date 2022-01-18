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
    elaborate,
    divide,
    fragment
)


class Test_move(unittest.TestCase):
    pitch = 60
    scale = _reify([11])

    def test_none(self):
        out = _move(None, self.scale, 1)
        self.assertIsNone(out)

    def test_step_none(self):
        out = _move(self.pitch, self.scale, None)
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


class TestElaborate(unittest.TestCase):
    # Beethoven Sonata No.1
    pitch_motif = [80, 77, None]
    duration_motif = [2, 1, 1]
    scale = [5, 7, 8, 10, 0, 1, 4]
    steps = [-1, -1, -1]

    def test_right(self):
        out = elaborate(self.pitch_motif, self.duration_motif, 0,
            self.steps, self.scale, 'right', 1/4)
        expected = (
            [80, 79, 77, 76, 77, None],
            [1.5, 1/6, 1/6, 1/6, 1, 1]
        )
        self.assertEqual(out, expected)

    def test_right_absolute(self):
        out = elaborate(self.pitch_motif, self.duration_motif, 0,
            self.steps, self.scale, 'right', 1/4, False)
        expected = (
            [80, 79, 79, 79, 77, None],
            [1.5, 1/6, 1/6, 1/6, 1, 1]
        )
        self.assertEqual(out, expected)

    def test_right_chord(self):
        pitch_motif = [[80, 84], 77, None]
        out = elaborate(pitch_motif, self.duration_motif, 0,
            self.steps, self.scale, 'right', 1/4)
        expected = (
            [[80, 84], [79, 82], [77, 80], [76, 79], 77, None],
            [1.5, 1/6, 1/6, 1/6, 1, 1]
        )
        self.assertEqual(out, expected)

    def test_left(self):
        out = elaborate(self.pitch_motif, self.duration_motif, 0,
            self.steps, self.scale, 'left')
        expected = (
            [76, 77, 79, 80, 77, None],
            [0.5, 0.5, 0.5, 0.5, 1, 1]
        )
        self.assertEqual(out, expected)

    def test_previous(self):
        out = elaborate(self.pitch_motif, self.duration_motif, 1,
            self.steps, self.scale, 'previous')
        expected = (
            [80, 72, 73, 76, 77, None],
            [0.5, 0.5, 0.5, 0.5, 1, 1]
        )
        self.assertEqual(out, expected)

    def test_previous_0(self):
        out = elaborate(self.pitch_motif, self.duration_motif, 0,
            self.steps, self.scale, 'previous', duration = 4)
        expected = (
            [76, 77, 79, 80, 77, None],
            [-1, -1, -1, 2, 1, 1]
        )
        self.assertEqual(out, expected)

    def test_next(self):
        out = elaborate(self.pitch_motif, self.duration_motif, 0,
            self.steps, self.scale, 'next', 1/2)
        expected = (
            [80, 79, 77, 76, 77, None],
            [2, 1/6, 1/6, 1/6, 1/2, 1]
        )
        self.assertEqual(out, expected)

    def test_next_last(self):
        pitch_motif = [80, 77, 80]
        out = elaborate(pitch_motif, self.duration_motif, 2,
            self.steps, self.scale, 'next', duration = 4)
        expected = (
            [80, 77, 80, 79, 77, 76],
            [2, 1, 1, -1, -1, -1]
        )
        self.assertEqual(out, expected)

    def test_none_0(self):
        pitch_motif = [[80, 81], 77, None]
        out = elaborate(pitch_motif, self.duration_motif, 0,
            [0, None], self.scale, 'right')
        expected = (
            [[80, 81], [80, 81], None, 77, None],
            [2/3, 2/3, 2/3, 1, 1]
        )
        self.assertEqual(out, expected)


class TestDivide(unittest.TestCase):
    pitch_motif = [60, 61, 62]
    duration_motif = [2, 2, 2]

    def test(self):
        out = divide(self.pitch_motif, self.duration_motif, 3)
        expected = [
            ([60], [2]),
            ([61], [2]),
            ([62], [2])
        ]
        self.assertEqual(out, expected)

    def test_slur(self):
        out = divide(self.pitch_motif, self.duration_motif, 2)
        expected = [
            ([60, 61], [2, 1]),
            ([61, 62], [1, 2])
        ]
        self.assertEqual(out, expected)


class TestFragment(unittest.TestCase):
    def test(self):
        pitch_motif = [60, 61, 62, 63]
        duration_motif = [1, 2, 1/2, 1/2]
        out = fragment(pitch_motif, duration_motif, 0, 1, 1/2)
        expected = ([60, 61], [1, 1])
        self.assertEqual(out, expected)
