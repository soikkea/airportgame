# -*- coding: utf-8 -*-

"""Implementation of the Runway class."""

import logging

import pygame
# TODO:
# from flight import Flight
import airportgame.colors as colors
from airportgame.pgtext import draw_text
from airportgame.utilities import vec2tuple


class Runway():
    """
    A part of an airfield
    """
    RUNWAY_WAIT_TIME = 45
    RUNWAY_COLOR = (192, 192, 192)
    RUNWAY_WIDTH = 15
    RUNWAY_LENGTH_SHORT = 70
    RUNWAY_LENGTH_MED = 100
    RUNWAY_LENGTH_LONG = 150
    RUNWAY_LENGTH_ENUM = {
        1: RUNWAY_LENGTH_SHORT,
        2: RUNWAY_LENGTH_MED,
        3: RUNWAY_LENGTH_LONG
    }

    def __init__(self, start_pos, end_pos, number, length):
        """
        start_pos (tuple)
        end_pos (tuple)
        length (int): 1...3
        """
        self.number = number
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.taken = False
        self.cooldown = 0
        self.length = length

        # Debugging
        assert(self.length in [1, 2, 3])

        self.flight = None
        self.queue = []
        #  Stores the extra time added to the cooldown per flight.
        self.addition = {}
        self.open = True

        self.wait_time = self.RUNWAY_WAIT_TIME
        # TODO: Add Flight.INCOMING_DISTANCE to wait time
        self.cool_down_time = self.wait_time

        self.logger = logging.getLogger(type(self).__name__)
        # TODO: Finish


    def get_start_and_end_pos(self):
        """Get the start and end positions of the runway.

        Returns:
            tuple -- start and end points.
        """

        return (self.start_pos, self.end_pos)

    def get_number(self):
        """Get the number of the runway.

        Returns:
            int -- Number of the runway.
        """

        return self.number

    def draw(self, screen, offset):
        """Draws the runway.

        Arguments:
            screen {Surface} -- Surface to draw on.
            offset {Vector} -- Offset of the Airfield.
        """

        runway_background = pygame.Surface(
            (self.RUNWAY_WIDTH, self.get_full_length()), pygame.SRCALPHA)
        runway_background.fill(self.RUNWAY_COLOR)
        runway_background = pygame.transform.rotate(runway_background,
                                                    self.get_angle())
        w, h = runway_background.get_size()
        start_pos = self.get_unoffsetted_point_tuple(self.start_pos,
                                                     vec2tuple(offset))
        end_pos = self.get_unoffsetted_point_tuple(self.end_pos,
                                                   vec2tuple(offset))
        mid_x = (start_pos[0] + end_pos[0]) / 2
        mid_y = (start_pos[1] + end_pos[1]) / 2
        dest = (mid_x - w / 2, mid_y - h / 2)
        screen.blit(runway_background, dest)


    def paint(self, screen, offset):
        """Paints the middle line and the number of the runway.

        Arguments:
            screen {Surface} -- Surface to draw on.
            offset {Vector} -- Offset of the Airfield.
        """

        runway_background = pygame.Surface(
            (self.RUNWAY_WIDTH, self.get_full_length()), pygame.SRCALPHA)

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
        start_pos = self.get_unoffsetted_point_tuple(self.start_pos, vec2tuple(offset))
        end_pos = self.get_unoffsetted_point_tuple(self.end_pos, vec2tuple(offset))
        mid_x = (start_pos[0] + end_pos[0]) / 2
        mid_y = (start_pos[1] + end_pos[1]) / 2
        dest = (mid_x - w / 2, mid_y - h / 2)
        screen.blit(runway_background, dest)

        # Draw the runway number
        try:
            draw_text(
                "Consolas", number_size, str(self.number), screen,
                self.get_unoffsetted_point_tuple(
                    self.start_pos, vec2tuple(offset)
                ),
                colors.BLACK
            )
        except pygame.error:
            self.logger.error("Could not draw text!")

    def get_full_length(self):
        """Get the full length of the runway.

        Returns:
            int -- Length of the runway.
        """

        assert(self.length in [1, 2, 3])
        length = self.RUNWAY_LENGTH_ENUM.get(self.length, None)

        if length is None:
            self.logger.error("Runway length is None. This should never happen!")
        return length


    def get_angle(self):
        """Get the angle of the runway. Returns the angle in degrees, with
        angle 0 pointing in the positive y direction and angle 90 pointing in
        the positive x direction.

        Returns:
            float -- angle of the runway.
        """

        unrotated = pygame.math.Vector2(0, self.get_full_length())
        rotated = pygame.math.Vector2(self.end_pos[0] - self.start_pos[0],
                                      self.end_pos[1] - self.start_pos[1])
        return rotated.angle_to(unrotated)


    def get_start_pos(self):
        """Return the starting point of the runway.

        Returns:
            Vector2 -- Starting point of the runway.
        """

        return pygame.math.Vector2(self.start_pos)

    def get_end_pos(self):
        """Return the ending point of the runway.

        Returns:
            Vector2 -- Ending point of the runway.
        """
        return pygame.math.Vector2(self.end_pos)

    def draw_selection_circle(self, screen):
        """Draw a circle indicating that this runway has been selected.

        Arguments:
            screen {Surface} -- Surface to draw to.
        """

        pos = self.get_start_pos()
        pos = (int(pos.x), int(pos.y))
        pygame.draw.circle(screen, colors.YELLOW, pos, 20, 3)

    def get_direction_vector(self):
        """Return an unit vector that points in the same direction as the
        runway.

        Returns:
            Vector2 -- Unit vector.
        """

        return pygame.math.Vector2(self.end_pos[0] -
                                   self.start_pos[0],
                                   self.end_pos[1] -
                                   self.start_pos[1]).normalize()

    def get_approach_point(self):
        """Get an "approach" point that all landing flights must pass through.

        Returns:
            Vector2 -- Point.
        """

        my_vect = self.get_direction_vector()
        assert(my_vect is not None)
        assert(self.get_full_length() is not None)
        return self.get_start_pos() - my_vect * 0.5 * self.get_full_length()

    def get_unoffsetted_point_tuple(self, point, offset):
        return (point[0] - offset[0], point[1] - offset[1])

