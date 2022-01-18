import music21
from typing import List, Union
from copy import deepcopy
from ch0p1n.motif import Pitch, PitchLine, DurationLine



# notations -> MIDI note numbers -------------------------------

def _to_pitch(notation: str) -> Pitch:

    """
    Convert the given notation to pitch.
    """

    note_names = {
        'C': 0,
        'D': 2,
        'E': 4,
        'F': 5,
        'G': 7,
        'A': 9,
        'B': 11
    }

    accidentals = {
        '': 0,
        '#': 1,
        '##': 2,
        '-': -1,
        '--': -2
    }

    pitch = note_names[notation[0].upper()] + \
        12 * (int(notation[-1]) + 1) + \
        accidentals[notation[1:-1]]

    return pitch


def to_pitch_line(notation_line: list) -> None:

    """
    Convert any notation to pitch in place.
    """

    for i, item in enumerate(notation_line):
        if isinstance(item, str):
            notation_line[i] = _to_pitch(item)
        elif isinstance(item, list):
            for j, notation in enumerate(item):
                if isinstance(notation, str):
                    notation_line[i][j] = _to_pitch(notation)



# MIDI note numbers -> notations -------------------------------

def _get_scale(key: int) -> List[str]:

    """
    Get the pitch classes that make the major scale of the given key.
    """

    note_names = ['F', 'C', 'G', 'D', 'A', 'E', 'B']

    if key >= 0:
        accidentals = ['#']*key + ['']*(7-key)
    else:
        accidentals = ['']*(7+key) + ['-']*(-key)

    pitch_classes = [
        note_name + accidentals[i]
        for i, note_name in enumerate(note_names)
    ]

    return pitch_classes


def _to_notations(pitch: Pitch) -> List[str]:

    """
    Convert the given pitch to equivalent notations.
    """

    notations = []
    pitch_class = pitch % 12
    octave = pitch//12 - 1

    for alter in range(-2, 3):
        pc = pitch_class - alter

        if pc < 0:
            o = octave - 1
        elif pc > 11:
            o = octave + 1
        else:
            o = octave

        try:
            i = [0, 2, 4, 5, 7, 9, 11].index(pc % 12)
        except:
            continue
        
        step = ['C', 'D', 'E', 'F', 'G', 'A', 'B'][i]
        acci = {0: '', 1: '#', 2: '##', -1: '-', -2: '--'}[alter]
        notation = step + acci + str(o)
        notations.append(notation)

    return notations


def _to_notation(
        pitch: Pitch,
        scale: List[str]
    ) -> Union[Pitch, str]:
    
    """
    Convert the given pitch to a notation.
    """

    notations = _to_notations(pitch)

    notations = [
        notation for notation in notations
        if notation[:-1] in scale
    ]

    if notations:
        notation = notations[0]
        return notation
    else:
        return pitch


def _to_notation_lines(
        pitch_lines: List[PitchLine],
        key: int
    ) -> None:

    """
    Convert pitches to notations in the given pitch lines.
    """

    scale = _get_scale(key)

    for i, line in enumerate(pitch_lines):
        for j, item in enumerate(line):
            if isinstance(item, int):
                pitch_lines[i][j] = _to_notation(item, scale)
            elif isinstance(item, list):
                pitch_lines[i][j] = [
                    _to_notation(pitch, scale)
                    for pitch in item
                ]



# show music ---------------------------------------------------

def _to_stream(
        pitch_lines: List[PitchLine],
        duration_lines: List[DurationLine]
    ) -> music21.stream.Stream:
    
    """
    Merge the given pitch and duration lines into
    a music21 Stream object.
    """
    
    stream = music21.stream.Stream()

    for i, line in enumerate(pitch_lines):
        voice = music21.stream.Voice()

        for j, item in enumerate(line):
            duration = duration_lines[i][j]
            duration = abs(duration) # see `elaborate`
            duration = music21.duration.Duration(duration)

            if isinstance(item, (int, str)):
                construct = music21.note.Note
            elif isinstance(item, list):
                construct = music21.chord.Chord
            else:
                construct = music21.note.Rest

            item = construct(item, duration=duration)
            voice.append(item)

        voice.id = str(i+1)
        stream.insert(0, voice)

    return stream


def show(
        pitch_lines: List[PitchLine],
        duration_lines: List[DurationLine],
        group: int = 1,
        key: int = 0,
        meter: str = '4/4',
        clefs: List[str] = ['g', 'f']
    ) -> None:
    
    """
    Show music.

    Parameters
    ----------
    group: int
        The number of voices in the treble staff.

    Examples
    --------
    >>> pitch_lines = [[60, [62, 63]], [None, 40]]
    >>> duration_lines = [[1, 1], [1, 1]]
    >>> show(pitch_lines, duration_lines)
    """

    pitch_lines = deepcopy(pitch_lines)
    _to_notation_lines(pitch_lines, key)
    
    # convert `key` and `meter` to music21 objects
    key = music21.key.KeySignature(key)
    meter = music21.meter.TimeSignature(meter)

    # convert items in `clefs` to music21 objects
    for i, clef in enumerate(clefs):
        if clef == 'g':
            clefs[i] = music21.clef.TrebleClef()
        elif clef == 'f':
            clefs[i] = music21.clef.BassClef()

    clef_1, clef_2 = clefs

    # setup score
    score = music21.stream.Score()
    staff_1 = music21.stream.PartStaff()
    staff_2 = music21.stream.PartStaff()
    layout = music21.layout.StaffGroup([staff_1, staff_2], symbol='brace')
    layout.barTogether = 'Mensurstrich'
    staff_1.append([clef_1, meter])
    staff_2.append([clef_2, meter])
    score.append([layout, staff_1, staff_2])

    # total duration
    duration = sum(duration_lines[0])
    # number of lines
    l = len(pitch_lines)

    # assign lines to staffs
    if group == 0:
        stream_1 = _to_stream([[None]], [[duration]])     
        stream_2 = _to_stream(pitch_lines, duration_lines)
        
    elif group == l:
        stream_1 = _to_stream(pitch_lines, duration_lines)
        stream_2 = _to_stream([[None]], [[duration]])

    else:
        stream_1 = _to_stream(
            pitch_lines[0:group],
            duration_lines[0:group]
        )

        stream_2 = _to_stream(
            pitch_lines[group:],
            duration_lines[group:]
        )

    for voice in stream_1:
        staff_1.insert(0, voice)
    
    for voice in stream_2:
        staff_2.insert(0, voice)

    # add measures
    score[0].makeMeasures(inPlace=True)
    score[1].makeMeasures(inPlace=True)

    # add key signature
    score[0][0].insert(0, key)
    score[1][0].insert(0, key)

    score.show('xml')
