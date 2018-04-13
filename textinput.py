# -*- coding: utf-8 -*-

class TextInput(object):
    """
    Class for interpreting text input from keyboard.
    """
    def __init__(self, pgtext):
        self.active = False
        self.return_pressed = False
        self.value = ""
        self.x = 0
        self.y = 0
        self.pgtext = pgtext
        pass
    
    def update(self, events):
        pass
    
    def draw(self, screen):
        if not self.active:
            return
        pass
    
    def activate(self):
        self.active = True
    
    def deactivate(self):
        self.active = False
    
    def is_active(self):
        return self.active
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
