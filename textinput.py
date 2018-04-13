# -*- coding: utf-8 -*-

from colors import BLACK

class TextInput(object):
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
        self.cursor_tick += elapsed_time
        if self.cursor_tick > 500:
            self.show_cursor = not self.show_cursor
            self.cursor_tick = 0
    
    def draw(self, screen):
        if not self.active:
            return
        text = self.value
        if self.show_cursor:
            text += "_"
        self.pgtext.display_text(text, screen, self.x, self.y, self.color)
    
    def activate(self):
        self.active = True
    
    def deactivate(self):
        self.active = False
    
    def is_active(self):
        return self.active
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
