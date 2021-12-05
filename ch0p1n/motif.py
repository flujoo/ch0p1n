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
    Replace all the points in a motif on-site.
    """
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
