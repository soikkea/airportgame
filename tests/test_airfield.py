"""Tests for airfield module."""

import unittest

from airportgame.airfield import Airfield


class TestAirfield(unittest.TestCase):

    def test_dist_to_segment(self):
        field = Airfield()
        a = (0, 0)
        b = (0, 10)
        for c_y in [0, 5, 10]:
            c = (5, c_y)
            self.assertAlmostEqual(field.dist_to_segment(a, b, c), 5)


if __name__ == '__main__':
    unittest.main()
