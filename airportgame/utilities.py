"""General utility functions."""
# -*- coding: utf-8 -*-

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
