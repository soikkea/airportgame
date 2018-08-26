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
        if len(points) < 4:
            self._points = []
        else:
            self._points = points[-4:]
            assert len(self._points) == 4
        self._p = np.array(self._points).T
        self._valid_points = self._p.shape == (2, 4)
        self._pg = np.zeros((2, 4))
        if self._valid_points:
            self._pg = self._p.dot(CATMULL_ROM)
    
    def get_point(self, t):
        if self._valid_points:
            t_vec = np.array([
                [1.0],
                [t],
                [t**2],
                [t**3]
            ], ndmin=2)
            assert t_vec.shape == (4, 1), t_vec.shape
            point = self._pg.dot(t_vec)
            return (point[0], point[1])
        else:
            return (None, None)
    
    def draw(self, screen, n=10):
        if self._valid_points:
            for t in np.linspace(0, 1, n):
                point = vec2int(self.get_point(t))
                pygame.draw.circle(screen, BLUE, point, 3)
