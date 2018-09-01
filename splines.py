import numpy as np
import pygame

from colors import BLUE
from utilities import vec2int

CATMULL_ROM = 0.5 * np.array(
    [
        [0., -1.,  2., -1.],
        [2.,  0., -5.,  3.],
        [0.,  1.,  4., -3.],
        [0.,  0., -1.,  1.]
    ]
)


class CatmullRom(object):
    def __init__(self, points):
        self._points = points
        self._n_points = len(points)
    
    def get_point(self, start_point, t):
        pg_matrix = self._get_pg(start_point)
        t_vec = np.array([
            [1.0],
            [t],
            [t**2],
            [t**3]
        ], ndmin=2)
        assert t_vec.shape == (4, 1), t_vec.shape
        point = pg_matrix.dot(t_vec)
        return (point[0], point[1])
    
    def _get_pg(self, start):
        if self._n_points == 0:
            return np.zeros((2, 4))
        points = []
        if start == 0:
            points.append(self._points[0])
        else:
            points.append(self._points[start - 1])
        points.append(self._points[start])
        for i in range(1, 3):
            if start + i >= self._n_points:
                points.append(self._points[self._n_points - 1])
            else:
                points.append(self._points[start + i])
        p_matrix = np.array(points).T
        assert p_matrix.shape == (2, 4)
        return p_matrix.dot(CATMULL_ROM)
    
    def draw(self, screen, n=10):
        for segment in range(0, self._n_points - 1):
            for t in np.linspace(0, 1, n):
                point = vec2int(self.get_point(segment, t))
                pygame.draw.circle(screen, BLUE, point, 3)
    
    def add_point(self, point):
        self._points.append(point)
        raise NotImplementedError()
    
    def clear(self):
        self._points.clear()
