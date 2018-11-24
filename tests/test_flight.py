"""Tests for runway class."""

import unittest

from pygame.math import Vector2

from airportgame.flight import Flight


class TestRunway(unittest.TestCase):

    def setUp(self):
        self.flight = Flight("", None, 0, 0)

    def test_rotate_to_vector(self):
        up = Vector2(0, 1)
        left = Vector2(-1, 0)
        right = Vector2(1, 0)
        down = Vector2(0, -1)

        self.flight.rotate_to_vector(up)
        self.assertAlmostEqual(self.flight.direction, 0)
        self.assertEqual(up, self.flight.get_direction_vector())
        self.flight.rotate_to_vector(down)
        self.assertAlmostEqual(self.flight.direction, 180)
        self.assertEqual(down, self.flight.get_direction_vector())
        self.flight.rotate_to_vector(right)
        self.assertAlmostEqual(self.flight.direction, 90)
        self.assertEqual(right, self.flight.get_direction_vector())
        self.flight.rotate_to_vector(left)
        self.assertAlmostEqual(self.flight.direction, -90)
        self.assertEqual(left, self.flight.get_direction_vector())
