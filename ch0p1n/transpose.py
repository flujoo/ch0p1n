from ch0p1n.motif import flatten, replace


def transpose(pitch_motif, scale, step):
    """
    Transpose a pitch motif along a given scale.
    """
    # expand scale
    scale = expand_scale(scale)

    # extract pitches
    pitches = flatten(pitch_motif)

    # move pitches
    pitches = [
        transpose_pitch(pitch, scale, step)
        for pitch in pitches
    ]

    motif = replace(pitch_motif, pitches)
    return motif


def expand_scale(scale):
    """
    Generate a list of pitches based on a given scale.

    Parameters
    ----------
    scale: list
        A list of pitch classes.
    """
    scale.sort()

    pitches = [
        pitch_class + octave*12
        for octave in range(11)
        for pitch_class in scale
    ]

    return pitches


def transpose_pitch(pitch, scale, step):
    """
    Move a pitch along an expanded scale.
    """
    if step == 0 or pitch is None:
        return pitch

    # insert `pitch` into `scale`
    if pitch not in scale:
        scale.append(pitch)
        scale.sort()

    # get the position of `pitch`
    i = scale.index(pitch)

    # move `pitch`
    pitch = scale[i + step]

    return pitch
