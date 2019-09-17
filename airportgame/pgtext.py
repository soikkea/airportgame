"""Utilities for displaying text in pygame."""

# -*- coding: utf-8 -*-


import pygame
from airportgame.colors import *


class PgText():
    """
    Helper class for creating and drawing text using PyGame
    """

    def __init__(self, font, size=25):
        self.font = pygame.font.SysFont(font, size)

    def create_text(self, string, color=BLACK):
        """
        Returns a new Surface with string written on it using self.font and
        antialiasing. Default color is BLACK.
        """
        return self.font.render(string, True, color)

    def display_text(self, text, screen, x=10, y=10, color=BLACK):
        """
        Displays the text in 'text' on the screen.
        """
        screen.blit(self.create_text(text, color), [x, y])


class PgTextObject():

    def __init__(self, text, color, x, y, text_surface):
        self._text = text
        self._color = color
        self._x = x
        self._y = y
        self._text_surface = text_surface

    def draw(self, screen):
        screen.blit(self._text_surface, [self._x, self._y])

    def get_rect(self):
        return self._text_surface.get_rect().move(self._x, self._y)


class PgTextFactory():

    def __init__(self, pg_text):
        self.pg_text = pg_text

    def create_text(self, string, color, x, y):
        surface = self.pg_text.create_text(string, color)
        return PgTextObject(string, color, x, y, surface)


def draw_text(font, size, text, screen, dest, color):
    """Draw text on screen.

    Arguments:
        font {str} -- Name of font.
        size {int} -- Size of font.
        text {str} -- Text to draw.
        screen {Surface} -- Surface to draw on.
        dest {tuple} -- Position to draw to.
        color {tuple} -- Color of the text.
    """

    font = pygame.font.SysFont(font, size)
    screen.blit(font.render(text, True, color), dest)
