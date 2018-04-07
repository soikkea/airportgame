# -*- coding: utf-8 -*-

import pygame
from colors import *

class Game(object):
    '''
    The core of the game.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Set up the font used by the game
        self.font = pygame.font.SysFont("Consolas", 25)
    
    def draw(self, screen):
        screen.fill(GREEN)
        self.display_text("AirPortGame", screen)
        pygame.display.flip()
    
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
