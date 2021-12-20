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
        steps = [step if step != 0 for step in steps]
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
