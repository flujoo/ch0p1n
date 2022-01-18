import unittest
from ch0p1n.utils import to_pitch_line, _get_scale


class TestToPitchLine(unittest.TestCase):
    def test(self):
        notation_line = [60, 'B-5', None, [61, 'c##2']]
        to_pitch_line(notation_line)
        expected = [60, 82, None, [61, 38]]
        self.assertEqual(notation_line, expected)


class Test_get_scale(unittest.TestCase):
    def test(self):
        out = _get_scale(7)
        expected = ['F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#']
        self.assertEqual(out, expected)
