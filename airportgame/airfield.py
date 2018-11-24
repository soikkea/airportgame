# -*- coding: utf-8 -*-
"""Implementation of the Airfield class."""

import logging
import random
import math

import pygame

from airportgame.runway import Runway
from airportgame.utilities import vec2tuple


class Airfield():
    """
    Airfield that contains runways.
    """
    FIELD_HEIGHT = 200
    FIELD_WIDTH = 400

    MINIMUM_DISTANCE = 40
    TRANSPARENCY_COLORKEY = (1, 2, 3)

    EDGE_BUFFER = 15

    def __init__(self, offset=(0, 0)):
        self.logger = logging.getLogger(__name__ + "." + type(self).__name__)

        # TODO: airfield size based on difficulty
        self.max_runways = 10
        self.min_runways = 3

        self.offset = offset

        # Airfield is created here
        self.reset_airfield()

    def reset_airfield(self):
        """Reset current airfield and create a new one"""
        self.logger.debug("Resetting airfield")
        self.runway_list = []

        self.create_airfield()

        self.airfield_map = pygame.Surface((self.FIELD_WIDTH, self.FIELD_HEIGHT))
        self.airfield_map.fill(self.TRANSPARENCY_COLORKEY)
        self.airfield_map.set_colorkey(self.TRANSPARENCY_COLORKEY)
        self.update_map()

    def create_airfield(self):
        """
        Randomly fills the airfield with runways
        """
        number_of_runways = random.randint(self.min_runways,
                                           self.max_runways)

        # Initialize the list of runways
        runways = [0] * number_of_runways

        length = 0
        for i in range(number_of_runways):

            # Make sure that there is at least one runway of each length
            if i <= 2:
                length += 1
            else:
                length = random.randint(1, 3)

            # Get the full length of the runway.
            runway_length = Runway.RUNWAY_LENGTH_ENUM[length]

            start_point_found = False

            while not start_point_found:
                s_x, s_y = self.get_random_point_inside_airfield()

                start_point_found = self.compare_points((s_x, s_y), i)

            start = (s_x, s_y)

            end_point_found = False

            # Counter to prevent infinite loops
            temp = 0

            while not end_point_found:

                temp += 1

                angle = random.random() * math.pi * 2.0
                e_x = math.cos(angle) * runway_length
                e_y = math.sin(angle) * runway_length

                # Make sure the endpoints are inside the airfield
                if s_x + e_x > self.FIELD_WIDTH or s_x + e_x < 0:
                    e_x = s_x - e_x
                else:
                    e_x = s_x + e_x
                if s_y + e_y > self.FIELD_HEIGHT or s_y + e_y < 0:
                    e_y = s_y - e_y
                else:
                    e_y = s_y + e_y

                e_x = int(e_x)
                e_y = int(e_y)

                end = (e_x, e_y)
                end_point_found = (self.compare_points(end, i) and
                                   self.point_inside_airfield(end))

                if temp == 1000:
                    # Just use this one if we actually end up here
                    self.logger.warning(
                        "Unoptimal runway end point for runway #%d !", (i + 1))
                    end_point_found = True

            # start point should be to the left of end:
            if e_x < s_x:
                start, end = end, start

            runways[i] = (start, end)

            if not self.point_inside_airfield(start):
                self.logger.warning("Runway %d start outside airfield!", i+1)
            if not self.point_inside_airfield(end):
                self.logger.warning("Runway %d end outside airfield!", i+1)

            new_runway = Runway(self.add_offset_to_tuple(start),
                                self.add_offset_to_tuple(end), i+1, length)
            self.runway_list.append(new_runway)

        return


    def get_runways(self):
        """Return a list of the runways on the airfield.

        Returns:
            list -- A list of runways.
        """

        return self.runway_list

    @staticmethod
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

    def compare_points(self, point, index):
        """
        Checks that the starting and ending points of all other runways are far enough
        of the one being tested.
        """
        if index == 0:
            return True

        for runway_i in range(index):
            runway = self.runway_list[runway_i]
            start, end = runway.get_start_and_end_pos()
            start = self.remove_offset_from_tuple(start)
            end = self.remove_offset_from_tuple(end)

            if (self.distance_between(point, start) < self.MINIMUM_DISTANCE or
                    self.distance_between(point, end) < self.MINIMUM_DISTANCE):
                return False
            if self.dist_to_segment(start, end, point) < (self.MINIMUM_DISTANCE):
                return False
        return True


    def update_map(self):
        """Draws and paints the runways on the airfield map."""

        for runway in self.runway_list:
            runway.draw(self.airfield_map, self.get_offset())

        for runway in self.runway_list:
            runway.paint(self.airfield_map, self.get_offset())

    def get_airfield_map(self):
        """Return the map of the airfield.

        Returns:
            Surface -- The map of the airfield.
        """

        return self.airfield_map

    def draw(self, screen):
        """Draws the airfield.

        Arguments:
            screen {Surface} -- Surface to draw on.
        """

        screen.blit(self.airfield_map, self.offset)

    def get_offset(self):
        """Return the offset of the airfield.

        Returns:
            Vector2 -- Offset
        """

        return pygame.math.Vector2(self.offset)

    def add_offset_to_tuple(self, point):
        """Adds elementwise the given point tuple to the offset.

        Arguments:
            point {tuple} -- A tuple of two numbers.

        Returns:
            x -- New x coordinate
            y -- New y coordinate
        """

        offset_x, offset_y = self.offset
        return (point[0] + offset_x, point[1] + offset_y)

    def remove_offset_from_tuple(self, point):
        """Subtract elementwise the offset from the given point tuple.

        Arguments:
            point {tuple} -- A tuple of two numbers.

        Returns:
            x -- New x coordinate
            y -- New y coordinate
        """
        offset_x, offset_y = self.offset
        return (point[0] - offset_x, point[1] - offset_y)

    def point_inside_airfield(self, point, use_buffer=True):
        """Returns true if the given point is inside the airfield.

        Arguments:
            point {tuple} -- Coordinates of a point.

        Keyword Arguments:
            use_buffer {bool} -- Whether EDGE_BUFFER should be used.
                (default: {True})

        Returns:
            bool -- True if point is inside the airfield.
        """

        buffer = self.EDGE_BUFFER if use_buffer else 0
        is_inside = (
            (buffer <= point[0] <= self.FIELD_WIDTH - buffer) and
            (buffer <= point[1] <= self.FIELD_HEIGHT - buffer)
        )
        return is_inside

    def get_random_point_inside_airfield(self):
        x = random.randint(self.EDGE_BUFFER, self.FIELD_WIDTH - self.EDGE_BUFFER)
        y = random.randint(self.EDGE_BUFFER, self.FIELD_HEIGHT - self.EDGE_BUFFER)
        return x, y

    def dist_to_segment(self, start, end, point):
        # https://stackoverflow.com/a/1501725
        segment_length = self.distance_between(start, end)
        if segment_length == 0:
            return self.distance_between(start, point)
        try:
            vec_a = point - start
            vec_b = end - start
        except TypeError:
            start = pygame.math.Vector2(start)
            vec_a = pygame.math.Vector2(point) - start
            vec_b = pygame.math.Vector2(end) - start
        projection = vec_a.dot(vec_b) / (segment_length ** 2)
        t = max(0, min(1, projection))
        projection_point = start + t * vec_b
        return self.distance_between(point, vec2tuple(projection_point))
