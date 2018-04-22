# -*- coding: utf-8 -*-

import math
import pygame.draw
# TODO:
# from flight import Flight

class Runway(object):
    """
    A part of an airfield
    """
    RUNWAY_WAIT_TIME = 45
    RUNWAY_COLOR = (192, 192, 192)
    RUNWAY_WIDTH = 15

    def __init__(self, start_pos, end_pos, number, length):
        """
        length: 1...3
        """
        self.number = number
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.taken = False
        self.cooldown = 0
        self.length = length
        self.flight = None
        self.queue = []
        #  Stores the extra time added to the cooldown per flight.
        self.addition = {}
        self.open = True

        self.wait_time = self.RUNWAY_WAIT_TIME
        # TODO: Add Flight.INCOMING_DISTANCE to wait time
        self.cool_down_time = self.wait_time

        # TODO: Finish


    def get_start_and_end_pos(self):
        return (self.start_pos, self.end_pos)
    

    def draw(self, screen):
        pygame.draw.line(screen, self.RUNWAY_COLOR, self.start_pos, self.end_pos, 
        self.RUNWAY_WIDTH)