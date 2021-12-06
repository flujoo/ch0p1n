from copy import deepcopy
from ch0p1n.motif import modify, flatten


def is_complete(pitch_motif, harmony, exclude=[]):
    """
    Check if a pitch motif fully reifies a given harmony.
    """
    # not include the pitches at positions `exclude`
    if exclude:
        pitch_motif = deepcopy(pitch_motif)

        for position in exclude:
            modify(pitch_motif, position, None)

    # extract pitches
    pitches = flatten(pitch_motif)
    
    # remove `None`
    pitches = [pitch for pitch in pitches if pitch is not None]

    # get pitch classes
    pitch_classes = [pitch % 12 for pitch in pitches]

    # check completeness
    completeness = set(pitch_classes) >= set(harmony)

    return completeness
