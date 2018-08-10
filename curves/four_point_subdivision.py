"""Computes Four Point Subdivision curve.

Four point subdivision is named as such because it uses a moving window of four control points. It
weights those control points in a certain way to generate one new point, which lies on the curve
alongside the original four control points.

Since each window of four control points can only generate one new point, the process has to be run
repeatedly to create a smooth curve.

"""
import numpy as np


def four_point_subdivision(data, iterations=10, weight=.0625):
    """Four Point Subdivision algorithm.

    There must be at least four control points to run the algorithm. Also, by varying the number of
    iterations, you can control the smoothness of the curve when rendered. Lastly, the weight
    parameter can greatly alter the shape of the curve. By default, it closely resembles Lagrange
    interpolation.

    :param data: List of control points. Each point is also structured as a list: [x, y, ...].
    :param iterations: Optional. Number of subdivision levels.
    :param weight: Optional. Weight parameter.
    :return: New list of points that represent the curve.
    """
    if not data or len(data) < 4:
        return None
    data = np.array(data, dtype='float32')
    data = np.vstack((data[0], data, data[-1]))
    for _ in range(iterations):
        # Generate new points from a moving window of four points.
        new_data_points = []
        for i in range(0, len(data) - 3):
            new_point = ((0.5 + weight) * (data[i + 1] + data[i + 2])) - \
                        (weight * (data[i] + data[i + 3]))
            new_data_points.append(new_point)
        # Combine the original control points with the new points.
        sub_data = data[2:-2]
        idx_new = 0
        idx_old = 0
        new_data = []
        for i in range(0, len(sub_data) + len(new_data_points)):
            if i % 2 == 0:
                new_data.append(new_data_points[idx_new])
                idx_new = idx_new + 1
            else:
                new_data.append(sub_data[idx_old])
                idx_old = idx_old + 1
        data = np.vstack((data[:2], new_data, data[-2:]))
        print(data)
    return data
