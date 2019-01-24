"""Main menu implementation."""

import pygame as pg

from airportgame.colors import RED


class Menu():
    def __init__(self, pgtext, width, height, x=0, y=0):
        self.buttons = ["New Game", "Quit"]
        self.show_menu = True
        self.pgtext = pgtext
        self.width = width
        self.height = height
        self.x = x
        self.y = y
    
    def update(self, elapsed_time, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    self.show_menu = False
                elif event.key == pg.K_2:
                    pg.event.post(pg.event.Event(pg.QUIT))
    
    def init_graphics(self):
        pass
    
    def draw(self, screen):
        self.pgtext.display_text("1. New Game", screen, 100, 100, RED)
        self.pgtext.display_text("2. Quit", screen, 100, 150, RED)
