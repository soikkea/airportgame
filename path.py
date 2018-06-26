# -*- coding: utf-8 -*-

import logging

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
        self.length = self.get_length()
        assert(self.length is not None)
        self.logger = logging.getLogger(__name__)
    
    def draw(self, screen):
        previous_point = self.points[0]
        for point in self.points[1:]:
            pygame.draw.line(screen, colors.BLUE, vec2int(previous_point), vec2int(point), 2)
            previous_point = point
    
    def get_length(self):
        length = 0.0
        previous_point = self.points[0]
        for point in self.points[1:]:
            length += previous_point.distance_to(point)
            previous_point = point
        return length
    
    def get_point_along_path(self, distance):
        if distance > self.length:
            return self.points[-1]
        if distance < 0.0:
            return self.points[0]
        length = 0.0
        previous_point = self.points[0]
        for point in self.points[1:]:
            current_length = previous_point.distance_to(point)
            if length <= distance and distance <= length + current_length:
                # Point in this leg
                relative_distance = distance - length
                dir_vector = (point - previous_point).normalize()
                return previous_point + dir_vector * relative_distance
            else:
                length += current_length
            previous_point = point
        self.logger.warning("This should never happen!")
        return self.points[-1]
