from copy import deepcopy


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


def modify(motif, position, point):
    """
    Change the point at a given position on-site.
    """
    i, j, *k = position

    if k:
        k = k[0]
        motif[i][j][k] = point
    else:
        motif[i][j] = point
