# -*- coding: utf-8 -*-

import random
import math

import pygame.draw as pgdraw
import pygame.math as pgmath

import colors
from path import PointsPath
from utilities import vec2int

class Flight(object):
    """
    A class representing a single flight
    """
    INCOMING_DISTANCE = 150
    WAITING_DISTANCE = 60
    ICON_SIZE = 5
    SELECTION_BOX_WIDTH = 2
    SPEED = 0.01

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
    

    def draw(self, screen):
        pgdraw.circle(screen, (0, 0, 0), vec2int(self.get_pos()), self.ICON_SIZE, 0)
        dir_vect = pgmath.Vector2(0, 1).rotate(-self.direction) * Flight.ICON_SIZE * 2
        vect_point = dir_vect + self.get_pos()
        new_x = int(vect_point[0])
        new_y = int(vect_point[1])
        pgdraw.line(screen, (0, 0, 0,), (self.x, self.y), (new_x, new_y))

        if (self.path is not None):
            self.path.draw_subpath(screen, self.path_pos)

    def update(self, elapsed_time):
        if self.path is not None:
            distance_travelled = elapsed_time * self.SPEED
            self.path_pos += distance_travelled
            new_pos = self.path.get_point_along_path(self.path_pos)
            old_pos = self.get_pos()
            self.update_pos(new_pos)
            self.rotate_to_vector(new_pos-old_pos)
    
    def rotate_to_vector(self, vec):
        if vec.length() > 0.0:
            self.direction = -pgmath.Vector2(0, 1).angle_to(vec)
            
    def update_pos(self, vector_pos):
        self.x = vector_pos[0]
        self.y = vector_pos[1]

    def draw_selection_box(self, screen):
        pgdraw.rect(screen, colors.BLUE, [self.x - Flight.ICON_SIZE, self.y - Flight.ICON_SIZE, Flight.ICON_SIZE * 2, Flight.ICON_SIZE * 2], Flight.SELECTION_BOX_WIDTH)

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
        points.append(my_pos + self.get_direction_vector() * runway.get_full_length() * 0.5)
        points.append(runway.get_approach_point())
        points.append(runway.get_start_pos())
        points.append(runway.get_end_pos())
        self.path = PointsPath(points)
        self.path_pos = 0.0
