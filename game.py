# -*- coding: utf-8 -*-

import pygame

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
        screen.fill((0, 255, 0))
        pygame.display.flip()
