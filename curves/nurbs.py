"""Computes NURBS curves.

NURBS are the weighted variant of B-splines. Given the overlap and flexibility of the B-spline
module, this module simply has to go through each point, multiply all values by the weight, and add
the weight as the last value in the point. The new points can be run through the B-spline pyramid
algorithm to compute the NURBS curve.

If your points already have the weights added to the points, you should ignore this helper module
and use the B-spline curve module.

"""
from curves.bspline import bspline

import numpy as np


def join_points_and_weights(points, weights):
    """Helper function to create modified points for use in computing NURBS curves.

    :param points: Control points that define the shape of the curve.
    :param weights: Weight values that determine the influence of each control point on the curve.
    :return: NURBS control data.
    """
    if not len(points) == len(weights):
        raise Exception('Invalid data provided. Length of points and weights does not match.')
    new_points = np.zeros(len(points), len(points[0]))
    for i in range(0, len(points)):
        point = points[i]
        w = weights[i]
        new_points[i] = list(np.array(point) * w) + [w, ]
    return points


def nurbs(degree, points, weights, t_values=None, knots=None):
    """NURBS curve algorithm.

    Combines points with their respective weights and runs them through the standard B-spline algorithm.
    This function can be used to evaluate the curve at one or many points.

    :param degree: Degree of the NURBS curve. Usually set to 3.
    :param points: List of control points. Each point is also structured as a list: [x, y, ...].
    :param weights: Weights for each control point.
    :param t_values: Optional. List of parameter values at which to sample the curve.
    :param knots: Optional. List of spacing values for the curve.
    :return: List of points on the NURBS curve at the t-values.
    """
    if t_values is None:
        t_values = np.linspace(0, len(points) - degree, len(points) * 1000)[:-1]
    data = join_points_and_weights(points, weights)
    return [bspline(t, degree, data, knots) for t in t_values]
