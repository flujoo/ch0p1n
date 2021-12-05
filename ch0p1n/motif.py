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
