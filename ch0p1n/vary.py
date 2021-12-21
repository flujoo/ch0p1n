from ch0p1n.motif import flatten, replace
from itertools import product


# util ---------------------------------------------------------

def expand(scale):
    """
    Expand a scale to the whole range of pitches.

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



# move single pitches ------------------------------------------

def move(pitch, scale, step):
    """
    Move a pitch along a scale by certain number of steps.
    """
    if pitch is None:
        return None

    scale = expand(scale)

    if pitch not in scale:
        if step == 0:
            # rather than trigger an error
            return None
        else:
            # insert `pitch` into `scale`
            scale.append(pitch)
            scale.sort()

    i = scale.index(pitch)

    # move `pitch`
    pitch = scale[i + step]

    return pitch


def span(pitch, scale, steps):
    """
    Move a pitch along a scale within a given range.
    """
    if pitch is None:
        return [None]

    if not steps:
        return []

    if (pitch % 12 not in scale) and (0 in steps):
        steps = [step for step in steps if step != 0]
        span(pitch, scale, steps)

    pitches = [move(pitch, scale, step) for step in steps]

    return pitches



# vary pitch motifs --------------------------------------------

def lead(pitch_motif, harmony, steps=[-1, 0, 1]):
    """
    Repeat a pitch motif in a given harmony,
    according to the common tone rule and nearest chordal tone rule.
    """
    pitches = flatten(pitch_motif)

    # get each pitch's nearest pitches
    nearest_pitches = [
        span(pitch, harmony, steps)
        for pitch in pitches
    ]

    # combine pitches
    pitch_combinations = product(*nearest_pitches)

    # generate motifs
    motifs = [
        # note that `pitch_combination` is tuple
        replace(pitch_motif, list(pitch_combination))
        for pitch_combination in pitch_combinations
    ]

    return motifs


def rescale(pitch_motif, mapping):
    """
    Map the pitches of a pitch motif onto a new scale.

    Parameters
    ----------
    mapping: dict
        A dictionary whose keys and values are pitch classes.
    """
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
        d = to - pitch_class

        if d >= 6:
            to = to - 12
        elif d <= -6:
            to = to + 12

        pitches[i] = to + octave*12

    motif = replace(pitch_motif, pitches)
    return motif
