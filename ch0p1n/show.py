import music21


def show(pitch_motif, duration_motif, partition=1, key=0,
         meter='4/4', clefs=['g', 'f']):
    """
    Show motif.

    Parameters
    ----------
    partition: int
        The number of voices in the treble staff.

    Examples
    --------
    >>> pitch_motif = [[60, [62, 63]], [None, 40]]
    >>> duration_motif = [[1, 1], [1, 1]]
    >>> show(pitch_motif, duration_motif)
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
    duration = sum(duration_motif[0])
    # number of lines
    l = len(pitch_motif)

    # assign lines to staffs
    if partition == 0:
        stream_1 = to_stream([[None]], [[duration]])     
        stream_2 = to_stream(pitch_motif, duration_motif)
        
    elif partition == l:
        stream_1 = to_stream(pitch_motif, duration_motif)
        stream_2 = to_stream([[None]], [[duration]])

    else:
        stream_1 = to_stream(
            pitch_motif[0:partition],
            duration_motif[0:partition]
        )

        stream_2 = to_stream(
            pitch_motif[partition:],
            duration_motif[partition:]
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


def to_stream(pitch_motif, duration_motif):
    """
    Merge a pitch motif and its duration motif into
    a music21 Stream object.
    """
    stream = music21.stream.Stream()

    for i, line in enumerate(pitch_motif):
        voice = music21.stream.Voice()

        for j, cluster in enumerate(line):
            duration = duration_motif[i][j]
            duration = music21.duration.Duration(duration)

            if isinstance(cluster, int):
                construct = music21.note.Note
            elif isinstance(cluster, list):
                construct = music21.chord.Chord
            else:
                construct = music21.note.Rest

            cluster = construct(cluster, duration=duration)
            voice.append(cluster)

        voice.id = str(i+1)
        stream.insert(0, voice)

    return stream
