"""Compute Convex Hull of a series of points.

Algorithm taken from Tomas Bouda
https://medium.com/100-days-of-algorithms/day-28-convex-hull-bc84b678da06

"""
import numpy as np


def split(u, v, points):
    # return points on left side of UV
    return [p for p in points if np.cross(np.subtract(p, u), np.subtract(v, u)) < 0]


def extend(u, v, points):
    if not points:
        return []
    # find furthest point W, and split search to WV, UW
    w = min(points, key=lambda p: np.cross(np.subtract(p, u), np.subtract(v, u)))
    p1, p2 = split(w, v, points), split(u, w, points)
    return extend(w, v, p1) + [w] + extend(u, w, p2)


def convex_hull(points):
    # find two hull points, U, V, and split to left and right search
    u = min(points, key=lambda p: p[0])
    v = max(points, key=lambda p: p[0])
    left, right = split(u, v, points), split(v, u, points)
    
    # find convex hull on each side
    return [v] + extend(u, v, left) + \
           [u] + extend(v, u, right) + [v]