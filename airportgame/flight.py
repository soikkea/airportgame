# -*- coding: utf-8 -*-

"""Implementation of the Flight class."""

import logging
import random

import pygame.draw as pgdraw
import pygame.math as pgmath

import airportgame.colors as colors
from airportgame.path import CatmullRomPathMemory
from airportgame.utilities import vec2int


class Flight(object):
    """
    A class representing a single flight
    """
    INCOMING_DISTANCE = 150
    WAITING_DISTANCE = 60
    ICON_SIZE = 5
    SELECTION_BOX_WIDTH = 2
    SPEED = 0.01

    # Status codes
    STATUS_NORMAL = 0
    STATUS_LANDING = 1
    STATUS_LANDED = 2

    def __init__(self, name, plane, x=0, y=0):
        """
        plane must be a Plane object
        """
        self.name = name
        self.plane = plane
        self.x = x
        self.y = y
        #self.direction = random.random() * 2.0 * math.pi
        self.direction = random.random() * 360
        self.path = None
        self.path_pos = None
        self._status = Flight.STATUS_NORMAL
        self.logger = logging.getLogger(__name__)

    def draw(self, screen, draw_subpath=True):
        """Draw the flight (and optinally its path).

        Arguments:
            screen {Surface} -- Surface to draw on.

        Keyword Arguments:
            draw_subpath {bool} -- Whether to draw the path of the flight.
                (default: {True})
        """

        pgdraw.circle(screen, (0, 0, 0), vec2int(self.get_pos()),
                      self.ICON_SIZE, 0)
        dir_vect = pgmath.Vector2(0, 1).rotate(-self.direction) * Flight.ICON_SIZE * 2
        vect_point = dir_vect + self.get_pos()
        new_x = int(vect_point[0])
        new_y = int(vect_point[1])
        pgdraw.line(screen, (0, 0, 0,), (self.x, self.y), (new_x, new_y))

        if (self.path is not None and self.is_landing()) and draw_subpath:
            self.path.draw_subpath(screen, self.path_pos)

    def update(self, elapsed_time):
        if self.path is not None:
            distance_travelled = elapsed_time * self.SPEED
            self.path_pos += distance_travelled
            new_pos = self.path.get_point_along_path(self.path_pos)
            old_pos = self.get_pos()
            self.update_pos(new_pos)
            self.rotate_to_vector(new_pos-old_pos)
            if self._status == Flight.STATUS_LANDING:
                if self.path.is_over(self.path_pos):
                    self._status = Flight.STATUS_LANDED
                    self.logger.debug("FLIGHT HAS LANDED")

    def rotate_to_vector(self, vec):
        if vec.length() > 0.0:
            self.direction = -pgmath.Vector2(0, 1).angle_to(vec)

    def update_pos(self, vector_pos):
        self.x = vector_pos[0]
        self.y = vector_pos[1]

    def draw_selection_box(self, screen):
        pgdraw.rect(screen, colors.BLUE,
                    [self.x - Flight.ICON_SIZE, self.y - Flight.ICON_SIZE,
                    Flight.ICON_SIZE * 2, Flight.ICON_SIZE * 2],
                    Flight.SELECTION_BOX_WIDTH)

    def draw_path(self, screen):
        if self.path is not None:
            self.path.draw(screen)

    def get_pos(self):
        return pgmath.Vector2(self.x, self.y)

    def get_direction_vector(self):
        return pgmath.Vector2(0, 1).rotate(-self.direction)

    def generate_landing_path(self, runway):
        points = []
        my_pos = self.get_pos()
        points.append(my_pos)
        points.append(my_pos + self.get_direction_vector()
                      * runway.get_full_length() * 0.5)
        points.append(runway.get_approach_point())
        points.append(runway.get_start_pos())
        points.append(runway.get_end_pos())
        # self.path = PointsPath(points)
        # self.path = CatmullRomPath(points)
        self.path = CatmullRomPathMemory(points)
        self.path_pos = 0.0
        self._status = Flight.STATUS_LANDING

    def is_landing(self):
        return self._status == Flight.STATUS_LANDING

    def set_path(self, path):
        """Set path that is not a landing path."""
        self.path = path
        self.path_pos = 0.0

    def get_status(self):
        return self._status
