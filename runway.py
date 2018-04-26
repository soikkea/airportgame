# -*- coding: utf-8 -*-

import math
import pygame
# TODO:
# from flight import Flight
import colors
from pgtext import draw_text

class Runway(object):
    """
    A part of an airfield
    """
    RUNWAY_WAIT_TIME = 45
    RUNWAY_COLOR = (192, 192, 192)
    RUNWAY_WIDTH = 15
    RUNWAY_LENGTH_SHORT = 70
    RUNWAY_LENGTH_MED = 100
    RUNWAY_LENGTH_LONG = 150

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
        # pygame.draw.line(screen, self.RUNWAY_COLOR, self.start_pos, self.end_pos, 
        # self.RUNWAY_WIDTH)
        runway_background = pygame.Surface((self.RUNWAY_WIDTH, self.get_full_length()), pygame.SRCALPHA)
        runway_background.fill(self.RUNWAY_COLOR)
        runway_background = pygame.transform.rotate(runway_background, self.get_angle())
        w, h = runway_background.get_size()
        mid_x = (self.start_pos[0] + self.end_pos[0]) / 2 
        mid_y = (self.start_pos[1] + self.end_pos[1]) / 2
        dest = (mid_x - w / 2, mid_y - h / 2) 
        screen.blit(runway_background, dest)
        # DEBUG:
        # pygame.draw.circle(screen, (255, 0, 0), self.start_pos, 5, 5)
        # pygame.draw.circle(screen, (255, 0, 0), self.end_pos, 5, 5)
    

    def paint(self, screen):
        runway_background = pygame.Surface((self.RUNWAY_WIDTH, self.get_full_length()), pygame.SRCALPHA)

        edge_offset = 5
        line_length = 5
        line_width = 2
        number_size = 18

        x = self.RUNWAY_WIDTH / 2
        final_y = self.get_full_length() - edge_offset
        start_y = edge_offset

        painted = False
        while not painted:
            end_y = start_y + line_length
            if end_y > final_y:
                end_y = final_y
                painted = True
            pygame.draw.line(runway_background, colors.WHITE, (x, start_y), (x, end_y), 
                line_width)
            start_y = end_y + line_length

        runway_background = pygame.transform.rotate(runway_background, self.get_angle())
        w, h = runway_background.get_size()
        mid_x = (self.start_pos[0] + self.end_pos[0]) / 2 
        mid_y = (self.start_pos[1] + self.end_pos[1]) / 2
        dest = (mid_x - w / 2, mid_y - h / 2) 
        screen.blit(runway_background, dest)

        draw_text("Consolas", number_size, str(self.number), screen, self.end_pos, colors.BLACK)
    

    def get_full_length(self):
        if self.length == 1:
            return Runway.RUNWAY_LENGTH_SHORT
        elif self.length == 2:
            return Runway.RUNWAY_LENGTH_MED
        elif self.length == 3:
            return Runway.RUNWAY_LENGTH_LONG
        else:
            return None
    

    def get_angle(self):
        unrotated = pygame.math.Vector2(0, self.get_full_length())
        rotated = pygame.math.Vector2(self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1])
        return rotated.angle_to(unrotated)
