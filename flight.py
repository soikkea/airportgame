# -*- coding: utf-8 -*-

import random

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
    

    def draw(self, screen):
        pgdraw.circle(screen, (0, 0, 0), (self.x, self.y), self.ICON_SIZE, 0)
    

    def draw_selection_box(self, screen):
        pgdraw.rect(screen, colors.BLUE, [self.x - Flight.ICON_SIZE, self.y - Flight.ICON_SIZE, Flight.ICON_SIZE * 2, Flight.ICON_SIZE * 2], Flight.SELECTION_BOX_WIDTH)
    

    def get_pos(self):
        return pgmath.Vector2(self.x, self.y)
