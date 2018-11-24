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


def draw_text(font, size, text, screen, dest, color):
    font = pygame.font.SysFont(font, size)
    screen.blit(font.render(text, True, color), dest)