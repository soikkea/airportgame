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
        self.clock = pygame.time.Clock()
        self.player = None
    
    def update(self):
        '''
        Update game logic.
        '''
        # How much time has passed since the last call
        self.clock.tick()

        # A new player must be created:
        if self.player is None:
            pass
    
    def draw(self, screen):
        screen.fill(GREEN)
        self.display_text("AirPortGame", screen)
        if self.player is None:
            self.display_text("Please enter your name: ", screen, 100, 100, RED)
        self.show_fps(screen)
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
    
    def show_fps(self, screen):
        '''
        Displays the current FPS on screen
        '''
        fps = self.clock.get_fps()
        self.display_text("FPS: {0:.2f}".format(fps), screen, 600, 10)
        pass
