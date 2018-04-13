# -*- coding: utf-8 -*-

import pygame
from colors import *

class PgText(object):
    """
    Helper class for creating and drawing text using PyGame
    """

    def __init__(self, font, size=25):
        self.font = pygame.font.SysFont(font, size)
    
    def create_text(self, string, color=BLACK):
        '''
        Returns a new Surface with string written on it using self.font and
        antialiasing. Default color is BLACK.
        '''
        return self.font.render(string, True, color)
    
    def display_text(self, text, screen, x=10, y=10, color=BLACK):
        '''
        Displays the text in 'text' on the screen.
        '''
        screen.blit(self.create_text(text, color), [x, y])