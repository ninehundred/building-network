import math

def get_segment_len(p1x, p1y, p2x, p2y):
    """return segment length from a series of points"""
    return math.sqrt(((p1x-p2x)**2)+((p1y-p2y)**2))
