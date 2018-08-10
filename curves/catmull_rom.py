"""Computes cubic Catmull-Rom spline curves.

This module provides functions to compute a cubic Catmull-Rom spline. Catmull-Rom splines are
related to Hermite splines except in this case, the derivative at each point is defined to be the
slope between the two adjacent points.

Given that there is no degree control, the code can be simplified to a series of statements rather
than loops.

"""
import numpy as np


def generate_uniform_knot_vector(num_points):
    """Generates uniform knot vector.

    Knots are used in spacing the Catmull-Rom spline curve. This function generates a uniform knot
    vector so all segments are spaced evenly.

    :param num_points: Number of control points.
    :return: Uniform knot vector.
    """
    return list(range(0, num_points))


def find_knot_index(t_value, knots):
    """Finds knot index for Catmull-Rom Spline pyramid algorithm.

    Catmull-Rom splines offer local control, so they are built using several segments. Each segment
    is built using a different subset of knots and control points. This function provides a guiding
    index for the data that should be used for making each segment.

    :param t_value: Current t-value.
    :param knots: List of spacing values for the curve.
    :return: Index of knot on which to start the Catmull Rom spline pyramid.
    """
    for i in range(0, len(knots) - 3):
        if knots[i] <= t_value < knots[i + 1]:
            return i
    return len(knots) - 3


def catmull_rom(t_value, points, knots=None):
    """Cubic Catmull-Rom spline pyramid algorithm.

    Pyramid algorithm that uses four control points and four knots to interpolate and compute a
    point on the Catmull-Rom spline segment defined by those control points and knots. By combining
    the segments defined by all control points, one can create a curve.

    :param knots: List of spacing values for the curve.
    :param points: List of control points. Each point is also structured as a list: [x, y, ...].
    :param t_value: Current t-value.
    :return: Point on the Catmull-Rom spline curve at t-value.
    """
    points = np.array(points, dtype='float32')
    if not knots:
        knots = generate_uniform_knot_vector(len(points))
    i = find_knot_index(t_value, knots)

    # Layer 1
    alpha = (knots[i] - t_value) / (knots[i] - knots[i - 1])
    p01 = (alpha * points[i - 1]) + ((1.0 - alpha) * points[i])
    alpha = (knots[i + 1] - t_value) / (knots[i + 1] - knots[i])
    p12 = (alpha * points[i]) + ((1.0 - alpha) * points[i + 1])
    alpha = (knots[i + 2] - t_value) / (knots[i + 2] - knots[i + 1])
    p23 = (alpha * points[i + 1]) + ((1.0 - alpha) * points[i + 2])
    # Layer 2
    alpha = (knots[i + 1] - t_value) / (knots[i + 1] - knots[i - 1])
    p012 = (alpha * p01) + ((1.0 - alpha) * p12)
    alpha = (knots[i + 2] - t_value) / (knots[i + 2] - knots[i])
    p123 = (alpha * p12) + ((1.0 - alpha) * p23)
    # Layer 3
    alpha = (knots[i + 1] - t_value) / (knots[i + 1] - knots[i])

    return (alpha * p012) + ((1.0 - alpha) * p123)


def catmull_rom_curve(points, t_values=None, knots=None):
    """Cubic Catmull-Rom spline curve wrapper function.

    Samples the Catmull-Rom spline curve defined by the control points and knots at various
    t-values. Generates uniform knot vector by default.

    :param points: List of control points. Each point is also structured as a list: [x, y, ...].
    :param t_values: Optional. List of parameter values at which to sample the curve.
    :param knots: Optional. List of spacing values for the curve.
    :return: List of points on the Catmull-Rom spline curve at the t-values.
    """
    # Duplicate first and last point to make a full curve touching all points.
    points = np.vstack((points[0], points, points[-1]))
    if not t_values:
        t_values = np.linspace(1, len(points) - 2, 1000 * (len(points) - 2))[:-1]
    if not knots:
        knots = generate_uniform_knot_vector(len(points))
    return [catmull_rom(t, points, knots) for t in t_values]
