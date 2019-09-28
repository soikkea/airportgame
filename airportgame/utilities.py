"""General utility functions."""
# -*- coding: utf-8 -*-

import math

def vec2int(vector):
    """Vector to integer tuple.

    Arguments:
        vector {Vector2} -- Vector

    Returns:
        tuple -- A tuple of ints.
    """

    return (int(vector[0]), int(vector[1]))

def vec2tuple(vector):
    """Vector to tuple.

    Arguments:
        vector {Vector2} -- Vector

    Returns:
        tuple -- Vector converted to a tuple.
    """

    return (vector[0], vector[1])

def distance_between(a, b):
        """
        Calculates the distance between two points
        """
        a_x = a[0]
        a_y = a[1]
        b_x = b[0]
        b_y = b[1]
        distance = math.sqrt((a_x - b_x) ** 2 + (a_y - b_y) ** 2)
        return distance
