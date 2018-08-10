"""Computes Hermite interpolation curve.

Hermite interpolation expands upon other interpolation curves by adding the ability to describe
varying levels of derivatives at the control points. This provides greater control over the shape
of the curve.

Hermite interpolation can also easily be made into a spline system because continuity at the
control points is guaranteed by the number of derivatives provided for the point. For greater
continuity, you can provide more derivatives.

"""
import numpy as np
from math import factorial, pow


def taylor(data, u_j, t_value, t_j):
    """Algorithm for evaluating Taylor series at a parameter value.

    Computes the Taylor series given a point and the derivatives at that point. The resulting
    function is evaluated at a given parameter value, t-value.

    :param data: Information related to the point. Structured such that the first value is the
        point, the second value is the first derivative, and so on.
    :param u_j: Number of data values.
    :param t_value: Parameter value at which to evaluate the Taylor series.
    :param t_j: Base parameter value that describes the point.
    :return: Point on the curve defined by the Taylor series for a given control point.
    """
    if u_j < 1:
        raise Exception('u_j < 1 error')
    if u_j == 1:
        return data[0]
    interp = pow(t_value - t_j, u_j - 1) / factorial(u_j - 1)
    return taylor(data, u_j - 1, t_value, t_j) + (interp * data[u_j - 1])


def compute_start_sequence(data):
    """Computes starting sequence for Hermite interpolation pyramid algorithm.

    Since there can be more than one piece of data for each control point, the pyramid algorithm
    is structured recursively. This function generates a sequence that helps keep track of the
    operations along the diagonals of the pyramid during the algorithm.

    :param data: Control data.
    :return: Sequence describing the structure of the control data.
    """
    sequence = []
    for i in range(0, len(data)):
        subseq = [i for _ in range(0, len(data[i]))]
        sequence.extend(subseq)
    return sequence


def generate_uniform_node_vector(data):
    """Generates uniform node vector.

    Node values can be used to control the spacing of the curve over the parameter range. For
    example, if the nodes were 0,2,3, the curve between P0 and P1 would have a larger range than
    the curve between P1 and P2. This alters the shape of the overall curve.

    This function generates a uniform node vector so all control points are spaced evenly.

    :param data: Control points.
    :return: Uniform node vector.
    """
    return list(range(0, len(data)))


# Computes a parametric function for the general hermite Interpolation at a given t value.
def hermite_internal(t_value, data, seq):
    """Hermite interpolation pyramid algorithm.

    Recursive variant of the Hermite interpolation pyramid algorithm. Computes a point on the
    interpolation curve defined by the control data at the t-value.

    :param t_value: Current t-value.
    :param data: Control data.
    :param seq: Sequence of control data.
    :return: Point on the Hermite interpolation curve at t-value.
    """
    if len(seq) < 1:
        return None
    if len(seq) == 1:
        return data[seq[0]][0]
    if seq[0] == seq[-1]:
        return taylor(data[seq[0]], len(seq), t_value, seq[0])
    w1 = (seq[-1] - t_value) / (seq[-1] - seq[0])
    w2 = (t_value - seq[0]) / (seq[-1] - seq[0])
    return (w1 * hermite_internal(t_value, data, seq[:-1])) + \
           (w2 * hermite_internal(t_value, data, seq[1:]))


def hermite(t_value, data):
    """Hermite interpolation point wrapper function.

    Wrapper function that removes the need for a start sequence, which is an implementation detail.

    :param data: Control data.
    :param t_value: Current t-value.
    :return: Point on the Hermite interpolation curve at t-value.
    """
    data = np.array(data, dtype='float32')
    start = compute_start_sequence(data)
    return hermite_internal(t_value, data, start)


def hermite_curve(data, t_values=None):
    """Hermite interpolation curve wrapper function.

    Samples the Hermite interpolation curve defined by the data at various t-values. By default, it
    will generate values over the entire curve.

    :param data: Control data.
    :param t_values: Optional. List of parameter values at which to sample the curve.
    :return: List of points on the Hermite interpolation curve at the t-values.
    """
    data = np.array(data, dtype='float32')
    if not t_values:
        t_values = np.linspace(0, len(data) - 1, 1000 * len(data))
    start = compute_start_sequence(data)
    return [hermite_internal(t, data, start) for t in t_values]


def hermite_spline(data, t_value):
    """Hermite spline point wrapper function.

    Uses pairs of points to create Hermite splines using the pyramid algorithm. Also removes the
    need for a start sequence since it is an implementation detail.

    :param data: Control data.
    :param t_value: Current t-value.
    :return: Point on the Hermite spline curve at t-value.
    """
    k = int(t_value)
    subdata = np.array(data[k:k+2], dtype='float32')
    start = compute_start_sequence(subdata)
    return hermite_internal(t_value - k, subdata, start)


def hermite_spline_curve(data, t_values=None):
    """Hermite spline curve wrapper function.

    Samples the Hermite spline curve at various t-values.

    :param data: Control data.
    :param t_values: Optional. List of parameter values at which to sample the curve.
    :return: List of points on the Hermite spline curve at the t-values.
    """
    if not t_values:
        t_values = np.linspace(0, len(data) - 1, 1000 * len(data))
    return [hermite_spline(data, t) for t in t_values]
