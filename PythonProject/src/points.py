from random import random

def generate_points(n : int):
    """
    Generate n random points.
    """
    ret = []
    for _ in range(n):
        ret.append((random(), random()))
    return ret
