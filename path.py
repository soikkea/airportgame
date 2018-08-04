# -*- coding: utf-8 -*-

import logging
import abc

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
            pygame.draw.line(screen, colors.BLUE, vec2int(
                previous_point), vec2int(point), 2)
            previous_point = point

    def draw_subpath(self, screen, distance):
        subpath = self.get_subpath(distance)
        previous_point = subpath[0]
        for point in subpath[1:]:
            pygame.draw.line(screen, colors.BLUE, vec2int(
                previous_point), vec2int(point), 2)
            previous_point = point

    def get_length(self):
        length = 0.0
        previous_point = self.points[0]
        for point in self.points[1:]:
            length += previous_point.distance_to(point)
            previous_point = point
        return length

    def get_subpath(self, distance):
        if distance > self.length:
            return self.points[-1:]
        if distance < 0.0:
            return self.points[0:]
        length = 0.0
        previous_point = self.points[0]
        for i, point in enumerate(self.points[1:]):
            current_length = previous_point.distance_to(point)
            if length <= distance and distance <= length + current_length:
                # Point in this part
                relative_distance = distance - length
                dir_vector = (point - previous_point).normalize()

                return [previous_point + dir_vector * relative_distance] + self.points[i + 1:]
            else:
                length += current_length
            previous_point = point
        self.logger.warning("This should never happen!")
        return self.points[-1:]

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
                # Point in this part
                relative_distance = distance - length
                dir_vector = (point - previous_point).normalize()
                return previous_point + dir_vector * relative_distance
            else:
                length += current_length
            previous_point = point
        self.logger.warning("This should never happen!")
        return self.points[-1]


class PathEnsemble(abc.ABC):
    def __init__(self):
        self.paths = []
        self.length = 0.0

    def draw(self, screen):
        for path in self.paths:
            path.draw(screen)

    def calculate_length(self):
        self.length = 0.0
        for path in self.paths:
            self.length += path.length

    def get_point_along_path(self, distance):
        length = 0.0
        for path in self.paths:
            if length <= distance <= length + path.length:
                return path.get_point_along_path(distance - length)
            else:
                length += path.length
        
        # distance > self.length
        return path.get_point_along_path(distance - (length - path.length))


class RectanglePathEnsemble(PathEnsemble):
    def __init__(self, top_left, bottom_right):
        super().__init__()
        self.left_x = top_left[0]
        self.top_y = top_left[1]
        self.right_x = bottom_right[0]
        self.bottom_y = bottom_right[1]
        self.width = self.right_x - self.left_x
        self.height = self.bottom_y - self.top_y

        p1 = [(self.left_x + self.width * 0.5, self.top_y),
              (self.right_x, self.top_y)]
        p2 = [(self.right_x, self.top_y),
              (self.right_x, self.bottom_y)]
        p3 = [(self.right_x, self.bottom_y),
              (self.left_x, self.bottom_y)]
        p4 = [(self.left_x, self.bottom_y),
              (self.left_x, self.top_y)]
        p5 = [(self.left_x, self.top_y),
              (self.left_x + self.width * 0.5, self.top_y)]

        for p in [p1, p2, p3, p4, p5]:
            to_vec = [pygame.math.Vector2(x) for x in p]
            path = PointsPath(to_vec)
            self.paths.append(path)

        self.calculate_length()
