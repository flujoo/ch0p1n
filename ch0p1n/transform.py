from ch0p1n.motif import flatten, replace


def transform(pitch_motif, mapping):
    """
    Map the pitches of a pitch motif onto a new scale.

    Parameters
    ----------
    mapping: dict
        A dictionary whose keys and values are pitch classes.
    """
    # extract pitches
    pitches = flatten(pitch_motif)

    # map pitches
    for i, pitch in enumerate(pitches):
        if pitch is None:
            continue

        octave = pitch // 12
        pitch_class = pitch % 12

        if pitch_class not in mapping:
            continue

        to = mapping[pitch_class]

        # get the nearest pitch
        # for example, for mapping `{11: 0}` and pitch 59,
        # the resulted pitch should be 60 rather than 48
        if abs(to - pitch_class) >= 6:
            to = 12 - to

        pitches[i] = to + octave*12

    motif = replace(pitch_motif, pitches)
    return motif
