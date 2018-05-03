# -*- coding: utf-8 -*-

import pygame
from colors import *
from textinput import TextInput
from pgtext import PgText
from player import Player
from airfield import Airfield
from flight import Flight
import random

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

        self.time_since_last_flight_created = 0
        self.incoming_flights = []

        self.selected_flight = None

        # Screen surface that has the size of 800 x 600
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        # Start game loop
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
                if (event.type == pygame.KEYDOWN and 
                    event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Select flight
                    # TODO:FINISH
                    pass
            # Update text input
            if self.textinput.is_active:
                self.textinput.update(elapsed_time, events)

            self.update(elapsed_time)
            self.draw(self.screen)
        return
    
    def update(self, elapsed_time):
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
                else:
                    self.player = Player("I am too important to input a name.")
                self.textinput.deactivate
                # TODO: Choose difficulty
                # TODO: Initialize Airfield
                self.airfield = Airfield(offset=self.center_airfield())
        else:
            # Game is running normally
            self.create_flight(elapsed_time)
        return True
    
    def draw(self, screen):
        screen.fill(GREEN)
        self.pgtext.display_text("AirPortGame", screen)
        if self.player is None:
            self.pgtext.display_text("Please enter your name: ", screen, 100, 100, RED)
            self.textinput.draw(screen)
        else:
            self.airfield.draw(screen)
            for flight in self.incoming_flights:
                flight.draw(screen)
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
        y = self.WINDOW_HEIGHT / 2 - (Airfield.FIELD_HEIGHT
            / 2)
        return (x, y)
    

    def create_flight(self, elapsed_time):
        time_limit = 180 * 1000

        self.time_since_last_flight_created += elapsed_time
        
        creation_rate = (self.time_since_last_flight_created 
            / time_limit) 
        
        # Limit creation of new planes when there are too many
        if len(self.incoming_flights) > 9:
            creation_rate = 0.0005
        
        chance = random.random()
        if chance < creation_rate:
            self.time_since_last_flight_created = 0
            # TODO: Create name for flights
            name = ""

            x = random.randint(0, self.WINDOW_WIDTH - 1)
            y = random.randint(0, self.WINDOW_HEIGHT - 1)
            new_flight = Flight(name, None, x=x, y=y)
            self.incoming_flights.append(new_flight)
    

    def find_closest_flight_in_range(self, x, y, max_range):
        """
        Return the flight closest to (x, y) within max_range
        """
        # TODO: FINISH THIS
        pass
