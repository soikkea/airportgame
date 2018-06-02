# -*- coding: utf-8 -*-

import pygame

import colors
from utilities import vec2int

# TODO: Abstract class
class Path(object):

    def __init__(self):
        pass

    def draw(self, screen):
        pass


class PointsPath(Path):

    def __init__(self, points):
        self.points = points
    
    def draw(self, screen):
        previous_point = self.points[0]
        for point in self.points[1:]:
            pygame.draw.line(screen, colors.BLUE, vec2int(previous_point), vec2int(point), 2)
            previous_point = point
            
