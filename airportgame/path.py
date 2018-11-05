# -*- coding: utf-8 -*-

import logging
import abc

import numpy as np
import pygame

import airportgame.colors as colors
from airportgame.utilities import vec2int


class Path(abc.ABC):

    def __init__(self, points):
        self.points = points
        self.length = 0.0
        self.logger = logging.getLogger(__name__ + type(self).__name__)

    @abc.abstractmethod
    def draw(self, screen):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def draw_subpath(self, screen, distance):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_length(self):
        raise NotImplementedError()
        
    @abc.abstractmethod
    def get_point_along_path(self):
        raise NotImplementedError()

    def is_over(self, distance):
        return self.length <= distance


class PointsPath(Path):

    def __init__(self, points):
        super().__init__(points)
        self.length = self.get_length()
        assert(self.length is not None)

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


class CatmullRomPath(Path):
    SPLINE_MATRIX = 0.5 * np.array(
        [
            [0., -1.,  2., -1.],
            [2.,  0., -5.,  3.],
            [0.,  1.,  4., -3.],
            [0.,  0., -1.,  1.]
        ]
    )

    def __init__(self, points, n=85):
        super().__init__(points)
        self._n_points = len(self.points)
        self.segment_lengths = None
        self.n = n
        self.length = self.get_length()
    
    def get_point(self, segment, t):
        pg_matrix = self._get_pg(segment)
        t_vec = np.array([
            [1.0],
            [t],
            [t ** 2],
            [t ** 3]
        ], ndmin=2)
        point = pg_matrix.dot(t_vec)
        return (point[0], point[1])
    
    def _get_pg(self, segment):
        if self._n_points == 0:
            return np.zeros((2, 4))
        points = []
        if segment == 0:
            points.append(self.points[0])
        else:
            points.append(self.points[segment - 1])
        points.append(self.points[segment])
        for i in range(1, 3):
            if segment + i >= self._n_points:
                points.append(self.points[self._n_points - 1])
            else:
                points.append(self.points[segment + i])
        p_matrix = np.array(points).T
        return p_matrix.dot(self.SPLINE_MATRIX)

    def draw(self, screen):
        div = 1.0 / self.n
        for segment in range(0, self._n_points - 1):
            previous_point = vec2int(self.points[segment])
            for t in np.linspace(div, 1, self.n):
                point = vec2int(self.get_point(segment, t))
                pygame.draw.line(screen, colors.BLUE, previous_point, point, 2)
                previous_point = point
    
    def draw_subpath(self, screen, distance):
        segment_start, t_start = self.find_segment(distance)
        div = 1.0 / self.n
        previous_point = self.get_point(segment_start, t_start)
        for t in np.linspace(t_start, 1, self.n):
            point = vec2int(self.get_point(segment_start, t))
            pygame.draw.line(screen, colors.BLUE, previous_point, point, 2)
            previous_point = point
        for segment in range(segment_start + 1, self._n_points - 1):
            for t in np.linspace(div, 1, self.n):
                point = vec2int(self.get_point(segment, t))
                pygame.draw.line(screen, colors.BLUE, previous_point, point, 2)
                previous_point = point
            previous_point = point

    def find_segment(self, distance):
        if distance > self.length:
            return self._n_points - 2, 1.0
        total_length = 0.0
        for i, segment in enumerate(self.segment_lengths):
            if total_length <= distance < total_length + segment:
                return i, (distance - total_length) / segment
            else:
                total_length += segment
        return self._n_points - 2, 1.0

    def get_length(self):
        total_length = 0.0
        points_per_segment = np.zeros((self.n, 2))
        self.segment_lengths = [0] * (self._n_points - 1)
        for segment in range(self._n_points - 1):
            for i, t in enumerate(np.linspace(0, 1, num=self.n)):
                points_per_segment[i, :] = self.get_point(segment, t)
            segment_length = np.sum(
                np.linalg.norm(
                    np.diff(points_per_segment, axis=0), axis=1
                )
            )
            self.segment_lengths[segment] = (segment_length)
            total_length += segment_length
        return total_length
    
    def get_point_along_path(self, distance):
        try:
            distance = distance % self.length
        except ZeroDivisionError:
            return self.points[0]
        segment, t = self.find_segment(distance)
        return self.get_point(segment, t)


class CatmullRomPathMemory(CatmullRomPath):

    def __init__(self, points, n=85):
        super().__init__(points, n)
        self._path = np.zeros((n * (self._n_points - 1) , 2))
        for segment in range(self._n_points - 1):
            t = np.linspace(0, 1, num=self.n)
            self._path[segment*n:(segment+1)*n, :] = (
                self.get_points(segment, t)
            )
        self._path_cumulative_length = (
            np.cumsum(
                np.linalg.norm(
                    np.diff(self._path, axis=0),
                    axis=1
                )
            )
        )
    
    def get_points(self, segment, t):
        pg_matrix = self._get_pg(segment)
        n_t = t.size
        t_matrix = np.ones((4, n_t))
        t_matrix[1, :] = t
        t_matrix[2, :] = t ** 2
        t_matrix[3, :] = t ** 3
        path = pg_matrix.dot(t_matrix)
        return path.T
    
    def draw(self, screen):
        int_points = self._path.astype(int)
        previous_point = int_points[0, :]
        for i in range(1, int_points.shape[0]):
            point = int_points[i, :]
            pygame.draw.line(screen, colors.BLUE, previous_point, point, 2)
            previous_point = point
        # for point in self.points:
        #     pygame.draw.circle(screen, colors.BLUE, vec2int(point), 5)
    
    def draw_subpath(self, screen, distance):
        segment_start, t_start = self.find_segment(distance)
        previous_point = self.get_point(segment_start, t_start)
        for j, cumsum in enumerate(self._path_cumulative_length):
            if cumsum > distance:
                break
        int_points = self._path.astype(int)
        for i in range(j, int_points.shape[0]):
            point = int_points[i, :]
            pygame.draw.line(screen, colors.BLUE, previous_point, point, 2)
            previous_point = point


class CubicBSplinePath(CatmullRomPathMemory):
    SPLINE_MATRIX = (1.0 / 6.0) * np.array(
        [
            [1., -3.,  3., -1.],
            [4.,  0., -6.,  3.],
            [1.,  3.,  3., -3.],
            [0.,  0.,  0.,  1.]
        ]
    )


class PathEnsemble(abc.ABC):
    def __init__(self, circular=False):
        self.paths = []
        self.length = 0.0
        self.circular = circular

    def draw(self, screen):
        for path in self.paths:
            path.draw(screen)

    def calculate_length(self):
        self.length = 0.0
        for path in self.paths:
            self.length += path.length

    def get_point_along_path(self, distance):
        length = 0.0
        if self.circular:
            if distance < 0.0:
                while distance < 0.0:
                    distance += self.length
            elif distance > self.length:
                while distance > self.length:
                    distance -= self.length
        for path in self.paths:
            if length <= distance <= length + path.length:
                return path.get_point_along_path(distance - length)
            else:
                length += path.length
        
        # distance > self.length
        return path.get_point_along_path(distance - (length - path.length))


class RectanglePathEnsemble(PathEnsemble):
    def __init__(self, top_left, bottom_right, **kwargs):
        super().__init__(kwargs)
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


class EllipticalPathEnsemble(PathEnsemble):
    def __init__(self, top_left, bottom_right, **kwargs):
        super().__init__(kwargs)
        self.left_x = top_left[0]
        self.top_y = top_left[1]
        self.right_x = bottom_right[0]
        self.bottom_y = bottom_right[1]
        self.width = self.right_x - self.left_x
        self.height = self.bottom_y - self.top_y

        offset = 36

        self.top_middle = pygame.math.Vector2(self.left_x + self.width * 0.5, self.top_y - offset)
        self.right_middle = pygame.math.Vector2(self.right_x + offset, self.top_y + self.height * 0.5)
        self.bottom_middle = pygame.math.Vector2(self.left_x + self.width * 0.5, self.bottom_y + offset)
        self.left_middle = pygame.math.Vector2(self.left_x - offset, self.top_y + self.height * 0.5)
        
        self.left_top = pygame.math.Vector2(self.left_x, self.top_y)
        self.right_top = pygame.math.Vector2(self.right_x, self.top_y)
        self.right_bottom = pygame.math.Vector2(self.right_x, self.bottom_y)
        self.left_bottom = pygame.math.Vector2(self.left_x, self.bottom_y)

        half_width = pygame.math.Vector2(self.width / 2, 0)
        half_height = pygame.math.Vector2(0, self.height / 2)

        p1 = [self.top_middle,
              self.top_middle,
              self.right_top,
              self.right_middle,
              self.right_bottom,
              self.bottom_middle,
              self.left_bottom,
              self.left_middle,
              self.left_top,
              self.top_middle,
              self.top_middle]

        # path = CatmullRomPathMemory(p1)
        path = CubicBSplinePath(p1)
        self.paths.append(path)

        self.calculate_length()
