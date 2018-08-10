"""Computes Lagrange interpolation curve.

This module provides functions to compute Lagrange interpolation. Lagrange interpolation is one of
the most basic forms. It basically finds a polynomial to fit the data. As such, it also suffers
from the same drawbacks. This form of curve generation has high oscillation and no local control.

"""
import numpy as np


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


def lagrange(data, t_value, nodes=None):
    """Lagrange interpolation pyramid algorithm.

    The Lagrange interpolation pyramid algorithm. Computes a single point at the t-value on the
    curve defined by the control points.

    A custom node vector can be specified using the nodes argument. If this value is not passed in,
    a uniform node vector will be generated automatically.

    :param data: Control points.
    :param t_value: Current t-value.
    :param nodes: Optional. Custom spacing values for the curve.
    :return: Point on the Lagrange interpolation curve at t-value.
    """
    if not data or len(data) < 2:
        return None
    data = np.array(data, dtype='float32')
    if not nodes:
        nodes = generate_uniform_node_vector(data)
    if len(nodes) != len(data):
        raise Exception('The number of nodes does not match the number of control points!')
    for i in range(len(data) - 1, 0, -1):
        for j in range(0, i):
            one = j
            two = j + (len(data) - i)
            w_1 = (nodes[two] - t_value) / (nodes[two] - nodes[one])
            w_2 = (t_value - nodes[one]) / (nodes[two] - nodes[one])
            data[j] = w_1 * data[j] + w_2 * data[j + 1]
    return data[0]


def lagrange_curve(data, t_values=None, nodes=None):
    """Lagrange interpolation curve wrapper function.

    Samples the Lagrange interpolation curve at various t-values.

    :param data: Control points.
    :param t_values: Optional. List of parameter values at which to sample the curve.
    :param nodes: Optional. Custom spacing values for the curve.
    :return: List of points on the Lagrange interpolation curve at the t-values.
    """
    if not nodes:
        nodes = generate_uniform_node_vector(data)
    if not t_values:
        t_values = np.linspace(0, len(data) - 1, 1000*len(data))
    return [lagrange(data, t, nodes) for t in t_values]
