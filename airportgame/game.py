# -*- coding: utf-8 -*-
"""Implementation of the core game loop."""


import random

import logging

import pygame

from airportgame.colors import RED, GREEN
from airportgame.textinput import TextInput
from airportgame.pgtext import PgText
from airportgame.player import Player
from airportgame.airfield import Airfield
from airportgame.flight import Flight
from airportgame.path import EllipticalPathEnsemble


class Game(object):
    """
    The core of the game.
    """
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    BORDER_MARGIN = 60

    def __init__(self, skip_name_input=False):
        """
        Constructor
        """
        # Set up the font used by the game
        self.pgtext = PgText("Consolas", 25)
        self.clock = pygame.time.Clock()
        self.player = None
        self.textinput = TextInput(self.pgtext, color=RED)

        self.airfield = None

        self.max_fps = 60

        self.time_since_last_flight_created = 0
        self.incoming_flights = []
        self.paths = []

        self.selected_flight = None
        self.selected_runway = None

        self.skip_name_input = skip_name_input

        self._draw_subpaths = True

        self.logger = logging.getLogger(__name__)

        # Screen surface that has the size of 800 x 600
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH,
                                               self.WINDOW_HEIGHT))
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
                if (event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_r:
                        if self.airfield is not None:
                            self.airfield.reset_airfield()
                    elif event.key == pygame.K_s:
                        self._draw_subpaths = not self._draw_subpaths
                if self.player is not None:
                    # Only do this if game is properly initialized
                    if event.type == pygame.MOUSEBUTTONUP:
                        # Select flight
                        # TODO:FINISH
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        flight_under_mouse = self.find_closest_flight_in_range(mouse_x, mouse_y)
                        runway_under_mouse = self.find_closest_runway_in_range(mouse_x, mouse_y)
                        if self.selected_flight is None:
                            self.selected_flight = flight_under_mouse
                        else:
                            if runway_under_mouse is not None:
                                self.selected_runway = runway_under_mouse
                                self.logger.debug("Runway %d selected", self.selected_runway.number)
                                self.selected_flight.generate_landing_path(self.selected_runway)
                            else:
                                self.selected_runway = None
                                self.selected_flight = flight_under_mouse
                                self.logger.debug("Runway deselected")
            # Update text input
            if self.textinput.is_active:
                self.textinput.update(elapsed_time, events)

            self.update(elapsed_time)
            self.draw(self.screen)
        return

    def update(self, elapsed_time):
        """
        Update game logic.
        """
        # A new player must be created:
        if self.player is None:
            if not self.skip_name_input:
                if not self.textinput.is_active():
                    self.textinput.activate()
                    self.textinput.set_pos(100, 150)
                if self.textinput.was_return_pressed():
                    if len(self.textinput.get_value()) > 0:
                        self.player = Player(self.textinput.get_value())
                    else:
                        self.player = Player("I am too important to input a name.")
                    self.textinput.deactivate()
                    # TODO: Choose difficulty
            else:
                self.player = Player("Debug Mode On")
            self.airfield = Airfield(offset=self.center_airfield())
            self.create_circling_flight_paths()
        else:
            # Game is running normally
            self.create_flight(elapsed_time)
            for flight in self.incoming_flights:

                #TODO: DEBUG, Make this better
                if flight.path is None:
                    path_num = random.randint(0, len(self.paths) - 1)
                    flight.set_path(self.paths[path_num])

                flight.update(elapsed_time)

            self.remove_landed_flights()
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
                flight.draw(screen, draw_subpath=self._draw_subpaths)
            if self.selected_flight is not None:
                self.selected_flight.draw_selection_box(screen)
            if self.selected_runway is not None:
                self.selected_runway.draw_selection_circle(screen)
            if ((self.selected_flight is not None) and
                (self.selected_runway is not None)):
                self.selected_flight.draw_path(screen)
            # TODO: DEBUGGING
            for path in self.paths:
                path.draw(screen)
        self.show_fps(screen)
        pygame.display.flip()

    def show_fps(self, screen):
        """
        Displays the current FPS on screen
        """
        fps = self.clock.get_fps()
        self.pgtext.display_text("FPS: {0:.2f}".format(fps), screen, 600, 10)

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

    def find_closest_flight_in_range(self, x, y, max_range=10):
        """
        Return the flight closest to (x, y) within max_range.
        """
        closest_flight = None
        closest_distance = max_range
        point = pygame.math.Vector2(x, y)
        for flight in self.incoming_flights:
            distance = point.distance_to(flight.get_pos())
            if distance < closest_distance:
                closest_distance = distance
                closest_flight = flight
        return closest_flight

    def find_closest_runway_in_range(self, x, y,
                                     max_range=Airfield.MINIMUM_DISTANCE):
        """
        Returns the closest runway within max_range.
        """
        closest_runway = None
        closest_distance = max_range
        point = pygame.math.Vector2(x, y)
        for runway in self.airfield.get_runways():
            distance = point.distance_to(runway.get_start_pos())
            if distance < closest_distance:
                closest_distance = distance
                closest_runway = runway
        # DEBUG
        if closest_runway is not None:
            self.logger.debug("Clicked at: %s, runway #%d at: %s", point, closest_runway.get_number(), (closest_runway.get_start_pos()))
        return closest_runway

    def create_circling_flight_paths(self, n=3):
        left_x1 = Game.BORDER_MARGIN
        airfield_offset = self.airfield.get_offset()
        left_x2 = airfield_offset[0] - Game.BORDER_MARGIN
        assert left_x1 < left_x2
        right_x1 = (airfield_offset[0] + self.airfield.FIELD_WIDTH
                                       + Game.BORDER_MARGIN)
        right_x2 = Game.WINDOW_WIDTH - Game.BORDER_MARGIN
        assert right_x1 < right_x2
        top_y1 = Game.BORDER_MARGIN
        top_y2 = airfield_offset[1] - Game.BORDER_MARGIN
        assert top_y1 < top_y2
        bottom_y1 = (airfield_offset[1] + self.airfield.FIELD_HEIGHT
                                        + Game.BORDER_MARGIN)
        bottom_y2 = Game.WINDOW_HEIGHT - Game.BORDER_MARGIN
        assert bottom_y1 < bottom_y2

        left_dx = (left_x2 - left_x1) / (n - 1)
        right_dx = (right_x2 - right_x1) / (n - 1)
        top_dy = (top_y2 - top_y1) / (n - 1)
        bottom_dy = (bottom_y2 - bottom_y1) / (n - 1)

        top_left = pygame.math.Vector2(left_x1, top_y1)
        bottom_right = pygame.math.Vector2(right_x2, bottom_y2)

        d_top_left = pygame.math.Vector2(left_dx, top_dy)
        d_bottom_right = pygame.math.Vector2(right_dx, bottom_dy)
        for i in range(n):
            xy1 = top_left + i * d_top_left
            xy2 = bottom_right - i * d_bottom_right
            # self.paths.append(RectanglePathEnsemble(xy1, xy2, circular=True))
            self.paths.append(EllipticalPathEnsemble(xy1, xy2, circular=True))

    def remove_landed_flights(self):
        for i in range(len(self.incoming_flights) -1, -1, -1):
            if self.incoming_flights[i].get_status() == Flight.STATUS_LANDED:
                if id(self.incoming_flights[i]) == id(self.selected_flight):
                    self.selected_flight = None
                del self.incoming_flights[i]
