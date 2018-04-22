# -*- coding: utf-8 -*-

import pygame
from colors import *
from textinput import TextInput
from pgtext import PgText
from player import Player
from airfield import Airfield

class Game(object):
    '''
    The core of the game.
    '''
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    def __init__(self):
        '''
        Constructor
        '''
        # Set up the font used by the game
        self.pgtext = PgText("Consolas", 25)
        self.clock = pygame.time.Clock()
        self.player = None
        self.textinput = TextInput(self.pgtext, color=RED)

        self.airfield = None

        self.max_fps = 60

        # Screen surface that has the size of 800 x 600
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.game_loop()
    
    def game_loop(self):
        """
        Main game loop
        """
        running = True
        while running:
            # How much time has passed since the last call (milliseconds)
            # Limit FPS to max_fps
            elapsed_time = self.clock.tick(self.max_fps)

            # Event handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            # Update text input
            if self.textinput.is_active:
                self.textinput.update(elapsed_time, events)

            self.update()
            self.draw(self.screen)
        return
    
    def update(self):
        '''
        Update game logic.
        '''
        # A new player must be created:
        if self.player is None:
            if not self.textinput.is_active():
                self.textinput.activate()
                self.textinput.set_pos(100, 150)
            if self.textinput.was_return_pressed():
                if len(self.textinput.get_value()) > 0:
                    self.player = Player(self.textinput.get_value())
                    self.textinput.deactivate
                    # TODO: Choose difficulty
                    # TODO: Initialize Airfield
                    self.airfield = Airfield(offset=self.center_airfield())
                else:
                    self.textinput.activate()
            
        return True
    
    def draw(self, screen):
        screen.fill(GREEN)
        self.pgtext.display_text("AirPortGame", screen)
        if self.player is None:
            self.pgtext.display_text("Please enter your name: ", screen, 100, 100, RED)
            self.textinput.draw(screen)
        else:
            self.airfield.draw(screen)
        self.show_fps(screen)
        pygame.display.flip()
    
    
    
    def show_fps(self, screen):
        '''
        Displays the current FPS on screen
        '''
        fps = self.clock.get_fps()
        self.pgtext.display_text("FPS: {0:.2f}".format(fps), screen, 600, 10)
        pass
    

    def center_airfield(self):
        x = self.WINDOW_WIDTH / 2 - (Airfield.FIELD_WIDTH / 2)
        y = self.WINDOW_HEIGHT / 2 - (Airfield.FIELD_HEIGHT / 2)
        return (x, y)
