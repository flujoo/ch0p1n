from ch0p1n.motif import flatten, replace, modify, access
from ch0p1n.vary import expand, move
from copy import deepcopy


def embellish(pitch_motif, position, reference, scale, step):
    """
    Change the pitch at the given position,
    according to some other pitch in the same pitch motif.
    """
    # get the referenced pitch
    pitch = access(pitch_motif, reference)

    # transpose the referenced pitch
    scale = expand(scale)
    pitch = move(pitch, scale, step)

    # modify the pitch at `position`
    motif = modify(pitch_motif, position, pitch)

    return motif
