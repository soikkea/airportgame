# -*- coding: utf-8 -*-

"""Implementation of the TextInput class."""

from pygame.locals import *

from airportgame.colors import BLACK

class TextInput():
    """
    Class for interpreting text input from keyboard.
    """
    def __init__(self, pgtext, max_length = 0, color=BLACK):
        self.active = False
        self.return_pressed = False
        self.value = ""
        self.x = 0
        self.y = 0
        self.pgtext = pgtext
        self.max_length = max_length
        self.cursor_tick = 0
        self.show_cursor = True
        self.color = color

    def update(self, elapsed_time, events):
        """Update state and handle events.

        Arguments:
            elapsed_time {float} -- Time elapsed since last call.
            events {list} -- List of events to handle.
        """

        self.cursor_tick += elapsed_time
        if self.cursor_tick > 500:
            self.show_cursor = not self.show_cursor
            self.cursor_tick = 0

        # Process keyboard events:
        for event in events:
            if event.type == KEYDOWN and not self.return_pressed:
                if event.key == K_BACKSPACE: self.value = self.value[:-1]
                elif event.key == K_RETURN or event.key == K_KP_ENTER: self.return_pressed = True
                elif event.key == K_a: self.value += "a"
                elif event.key == K_b: self.value += "b"
                elif event.key == K_c: self.value += "c"
                elif event.key == K_d: self.value += "d"
                elif event.key == K_e: self.value += "e"
                elif event.key == K_f: self.value += "f"
                elif event.key == K_g: self.value += "g"
                elif event.key == K_h: self.value += "h"
                elif event.key == K_i: self.value += "i"
                elif event.key == K_j: self.value += "j"
                elif event.key == K_k: self.value += "k"
                elif event.key == K_l: self.value += "l"
                elif event.key == K_m: self.value += "m"
                elif event.key == K_n: self.value += "n"
                elif event.key == K_o: self.value += "o"
                elif event.key == K_p: self.value += "p"
                elif event.key == K_q: self.value += "q"
                elif event.key == K_r: self.value += "r"
                elif event.key == K_s: self.value += "s"
                elif event.key == K_t: self.value += "t"
                elif event.key == K_u: self.value += "u"
                elif event.key == K_v: self.value += "v"
                elif event.key == K_w: self.value += "w"
                elif event.key == K_x: self.value += "x"
                elif event.key == K_y: self.value += "y"
                elif event.key == K_z: self.value += "z"
                # TODO: finish the rest of keyboard

    def draw(self, screen):
        """Draw the inputted text.

        Arguments:
            screen {Surface} -- Surface to draw on.
        """

        if not self.active:
            return
        text = self.value
        if self.show_cursor:
            text += "_"
        self.pgtext.display_text(text, screen, self.x, self.y, self.color)

    def activate(self):
        """Activate the text input."""

        self.active = True
        self.return_pressed = False

    def deactivate(self):
        """Deactivates the text input."""
        self.active = False
        self.return_pressed = False

    def is_active(self):
        """Returns True if the text input is active.

        Returns:
            bool -- Activity status.
        """

        return self.active

    def set_pos(self, x, y):
        """Set the position of the text input.

        Arguments:
            x {int} -- x coordinate.
            y {int} -- y coordinate.
        """

        self.x = x
        self.y = y

    def was_return_pressed(self):
        """Returns True if return was pressed.

        Returns:
            bool -- Was return pressed.
        """

        return self.return_pressed

    def get_value(self):
        """Returns the current value of the text input.

        Returns:
            str -- Inputted text.
        """

        return self.value
