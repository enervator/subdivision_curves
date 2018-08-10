"""Computes B-Spline curves.

This module provides functions to compute a B-Spline curve. Given control points, degree, and a
t-value, the module can generate a point at the specified t-value. As you vary t over the range
of the knots, a curve is formed. By default the knots are automatically generated and are spaced
evenly.

"""
import numpy as np


def generate_uniform_knot_vector(num_points, degree):
    """Generates a uniform knot vector.

    Knots are used to space the B-spline curve over the control points. This function generates
    uniform knots for the control points given the degree. The knots are also replicated at the
    ends so that the curve touches the first and last control point.

    :param num_points: Number of control points.
    :param degree: Degree of the B-spline curve.
    :return: Uniform knot vector.
    """
    count = num_points - degree
    knots = list(range(0, count + 1))
    pad_start = [0 for _ in range(1, degree)]
    pad_end = [count for _ in range(1, degree)]
    return pad_start + knots + pad_end


def find_knot_index(t_value, knots):
    """Finds knot index for B-spline pyramid algorithm.

    B-spline curves provide local control. This is partially explained by the fact that the curve
    is built up using segments. These segments are all built using a subset of the knots and
    control points. This function provides a guiding index for the data that should be used for
    making each segment.

    :param t_value: Current t-value.
    :param knots: List of spacing values for the curve.
    :return: Index of knot on which to start B-spline pyramid.
    """
    for i in range(0, len(knots) - 1):
        if knots[i] <= t_value < knots[i + 1]:
            return i
    return 0


def bspline(t_value, degree, points, knots=None):
    """B-spline pyramid algorithm.

    The pyramid algorithm that is used to compute the point on the curve at parameter t-value.
    Generates a uniform knot vector by default.

    :param t_value: Current t-value.
    :param degree: Degree of the B-spline curve. Usually set to 3.
    :param points: List of control points. Each point is also structured as a list: [x, y, ...].
    :param knots: Optional. List of spacing values for the curve.
    :return: Point on the B-spline curve at t-value.
    """
    if not knots:
        knots = generate_uniform_knot_vector(len(points), degree)
    k = find_knot_index(t_value, knots)
    pts = np.array(points[k-degree+1:k+2], dtype='float32')
    for i in range(0, degree):
        for j in range(0, degree - i):
            k_one = k - degree + 1 + j + i
            k_two = k + 1 + j
            alpha = (t_value - knots[k_one]) / (knots[k_two] - knots[k_one])
            pts[j] = ((1.0 - alpha) * pts[j]) + (alpha * pts[j+1])
    return pts[0]


def bspline_curve(degree, points, t_values=None, knots=None):
    """B-spline curve wrapper function.

    Samples the B-spline curve defined by the control points and knots at various t-values.
    Generates uniform knot vector by default.

    :param degree: Degree of the B-spline curve. Usually set to 3.
    :param points: List of control points. Each point is also structured as a list: [x, y, ...].
    :param t_values: Optional. List of parameter values at which to sample the curve.
    :param knots: Optional. List of spacing values for the curve.
    :return: List of points on the B-spline curve at the t-values.
    """
    if not t_values:
        t_values = np.linspace(0, len(points) - degree, len(points) * 1000)[:-1]
    if not knots:
        knots = generate_uniform_knot_vector(len(points), degree)
    return [bspline(t, degree, points, knots=knots) for t in t_values]
