# -*- coding: utf-8 -*-

import pygame
from colors import *
from textinput import TextInput
from pgtext import PgText

class Game(object):
    '''
    The core of the game.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Set up the font used by the game
        self.pgtext = PgText("Consolas", 25)
        self.clock = pygame.time.Clock()
        self.player = None
        self.textinput = TextInput(self.pgtext)
    
    def update(self):
        '''
        Update game logic.
        '''        
        # How much time has passed since the last call
        self.clock.tick()

        # A new player must be created:
        if self.player is None:
            if not self.textinput.is_active():
                self.textinput.activate()
                self.textinput.set_pos(100, 150)
            pass
        return True
    
    def draw(self, screen):
        screen.fill(GREEN)
        self.pgtext.display_text("AirPortGame", screen)
        if self.player is None:
            self.pgtext.display_text("Please enter your name: ", screen, 100, 100, RED)
            self.textinput.draw(screen)
        self.show_fps(screen)
        pygame.display.flip()
    
    
    
    def show_fps(self, screen):
        '''
        Displays the current FPS on screen
        '''
        fps = self.clock.get_fps()
        self.pgtext.display_text("FPS: {0:.2f}".format(fps), screen, 600, 10)
        pass
