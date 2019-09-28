"""Tests for runway class."""

import unittest

from airportgame.path import EllipticalPathEnsemble
from airportgame.utilities import distance_between


class TestEllipticalPathEnsemble(unittest.TestCase):

    def test_endpoints(self):
        path = EllipticalPathEnsemble((0, 0), (1, 1), circular=True)
        start = path.get_point_along_path(0)
        end = path.get_point_along_path(path.length * 0.999999)
        self.assertLess(distance_between(start, end), 1e-5)
