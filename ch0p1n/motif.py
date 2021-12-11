from copy import deepcopy
from itertools import chain


def flatten(motif):
    """
    Flatten a motif recursively.
    """
    points = []

    for i, line in enumerate(motif):
        for j, cluster in enumerate(line):
            if isinstance(cluster, list):
                points.extend(cluster)
            else:
                points.append(cluster)
    
    return points


def replace(motif, points):
    """
    Replace all the points in a motif.
    """
    motif = deepcopy(motif)
    k = 0

    for i, line in enumerate(motif):
        for j, cluster in enumerate(line):
            if isinstance(cluster, list):
                l = len(cluster)
                motif[i][j] = points[k:k+l]
                k = k + l
            else:
                motif[i][j] = points[k]
                k = k + 1

    return motif


def modify(motif, position, point, on_site=False):
    """
    Change the point at a given position.
    """
    if not on_site:
        motif = deepcopy(motif)

    i, j, *k = position

    if k:
        k = k[0]
        motif[i][j][k] = point
    else:
        motif[i][j] = point

    if not on_site:
        return motif


def access(motif, position):
    """
    Get the point at the given position.
    """
    i, j, *k = position

    if k:
        k = k[0]
        point = motif[i][j][k]
    else:
        point = motif[i][j]
    
    return point


def merge(*motifs):
    """
    Merge some motifs into a single one.
    """
    motif = [
        list(chain(*lines))
        # treat `*motifs` as a matrix and transpose it
        for lines in zip(*motifs)
    ]

    return motif


def multiply(motif, n):
    """
    Replicate a motif some times and merge them.
    """
    motif = [line * n for line in motif]
    return motif
