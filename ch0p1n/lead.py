from ch0p1n.motif import flatten, replace
from itertools import product


def lead(pitch_motif, harmony, semitone=2):
    """
    Adapt a pitch motif to a given harmony,
    according to voice-leading rules,
    especially the common tone rule and nearest chordal tone rule.
    """
    # extract all pitches from `pitch_motif`
    pitches = flatten(pitch_motif)

    # get each pitch's nearest pitches
    nearest_pitches = [
        get_nearest_pitches(pitch, harmony, semitone)
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


def get_nearest_pitches(pitch, harmony, semitone=2):
    """
    Get a pitch's nearest pitches in a given harmony.
    """
    if pitch is None:
        return [None]

    # all pitches in the range
    pitches = range(pitch - semitone, pitch + semitone + 1)
    
    # keep only those which fit the harmony
    pitches = [pitch for pitch in pitches if pitch % 12 in harmony]

    return pitches
