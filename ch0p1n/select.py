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
            modify(pitch_motif, position, None, True)

    # extract pitches
    pitches = flatten(pitch_motif)

    # get pitch classes
    pitch_classes = [pitch % 12 for pitch in pitches if pitch]

    # check completeness
    completeness = set(pitch_classes) >= set(harmony)

    return completeness



# contour ------------------------------------------------------

def get_contour(pitches):
    """
    Get the contour of a list of pitches,
    which includes no `None`.
    """
    contour = []

    for i, pitch in enumerate(pitches[:-1]):
        d = pitches[i+1] - pitch

        if d > 0:
            contour.append(1)
        elif d < 0:
            contour.append(-1)
        else:
            contour.append(0)

    return contour


def get_ordinals(pitches):
    """
    Get the ordinals of a list of pitches,
    which includes no `None`.
    """
    ordinals = [
        sorted(set(pitches)).index(pitch)
        for pitch in pitches
    ]
    
    return ordinals


def is_isomorphic(pitch_motif, proto, method="contour", which=0):
    """
    Check if a pitch motif has the same contour as the prototype.
    """
    # get the contour from a pitch motif
    def get(motif):
        # get the targeted line
        line = motif[which]

        # remove `None`
        line = [pitch for pitch in line if pitch]

        # compare chords' highest pitches
        line = [
            max(pitch) if isinstance(pitch, list) else pitch
            for pitch in line
        ]

        # get contour
        if method == "contour":
            contour = get_contour(line)
        elif method == "ordinals":
            contour = get_ordinals(line)

        return contour

    # compare contours
    isomorphism = get(pitch_motif) == get(proto)

    return isomorphism
