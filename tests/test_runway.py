"""Tests for runway class."""

import unittest

from airportgame.runway import Runway


class TestRunway(unittest.TestCase):

    def test_get_angle(self):
        origin = (0, 0)
        y = (0, 1)
        x = (1, 0)
        runway1 = Runway(origin, y, 1, 1)
        runway2 = Runway(origin, x, 1, 1)

        self.assertNotAlmostEqual(runway1.get_angle(), runway2.get_angle())
        self.assertAlmostEqual(runway1.get_angle(), 0)
        self.assertAlmostEqual(runway2.get_angle(), 90)