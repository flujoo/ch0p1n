import music21
from typing import List
from ch0p1n.motif import PitchLine, DurationLine



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

            if isinstance(item, int):
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
