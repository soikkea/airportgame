"""Main menu implementation."""

import pygame as pg

from airportgame.colors import RED
from airportgame.pgtext import PgTextFactory


class Menu():
    def __init__(self, pgtext, width, height, x=0, y=0):
        self.buttons = ["New Game", "Quit"]
        self.show_menu = True
        # TODO: Remove
        # self.pgtext = pgtext
        self.pgtext_factory = PgTextFactory(pgtext)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.buttons = []
        self.init_graphics()
    
    def update(self, elapsed_time, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    self.show_menu = False
                elif event.key == pg.K_2:
                    pg.event.post(pg.event.Event(pg.QUIT))
    
    def init_graphics(self):
        new_game = self.pgtext_factory.create_text("1. New Game", RED, 100, 100)
        quit_game = self.pgtext_factory.create_text("2. Quit", RED, 100, 150)
        self.buttons = [new_game, quit_game]
    
    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)
