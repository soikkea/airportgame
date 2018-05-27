# -*- coding: utf-8 -*-

import random
import math

import pygame.draw as pgdraw
import pygame.math as pgmath

import colors

class Flight(object):
    """
    A class representing a single flight
    """
    INCOMING_DISTANCE = 150
    WAITING_DISTANCE = 60
    ICON_SIZE = 5
    SELECTION_BOX_WIDTH = 2

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
    

    def draw(self, screen):
        pgdraw.circle(screen, (0, 0, 0), (self.x, self.y), self.ICON_SIZE, 0)
        dir_vect = pgmath.Vector2(0, 1).rotate(-self.direction) * Flight.ICON_SIZE * 2
        vect_point = dir_vect + self.get_pos()
        new_x = int(vect_point[0])
        new_y = int(vect_point[1])
        pgdraw.line(screen, (0, 0, 0,), (self.x, self.y), (new_x, new_y))
    

    def draw_selection_box(self, screen):
        pgdraw.rect(screen, colors.BLUE, [self.x - Flight.ICON_SIZE, self.y - Flight.ICON_SIZE, Flight.ICON_SIZE * 2, Flight.ICON_SIZE * 2], Flight.SELECTION_BOX_WIDTH)
    

    def get_pos(self):
        return pgmath.Vector2(self.x, self.y)
