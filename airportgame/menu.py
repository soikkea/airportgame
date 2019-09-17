"""Main menu implementation."""

from enum import IntEnum

import pygame as pg

from airportgame.colors import RED
from airportgame.pgtext import PgTextFactory


class MenuButtons(IntEnum):
    NEW_GAME = 0
    QUIT = 1


class Menu():

    def __init__(self, pgtext, width, height, x=0, y=0):
        """Main menu for the game.

        Arguments:
            pgtext {PgText} -- PgText object.
            width {int} -- width of the menu.
            height {int} -- height of the menu.

        Keyword Arguments:
            x {int} -- x offset (default: {0})
            y {int} -- y offset (default: {0})
        """
        self.buttons = ["New Game", "Quit"]
        self.show_menu = True
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
                    return self.new_game_pressed()
                if event.key == pg.K_2:
                    return self.quit_pressed()
            if event.type == pg.MOUSEBUTTONUP:
                mouse_x, mouse_y = pg.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    button_rect = button.get_rect()
                    if not button_rect.collidepoint(mouse_x, mouse_y):
                        continue
                    if i == MenuButtons.NEW_GAME:
                        return self.new_game_pressed()
                    if i == MenuButtons.QUIT:
                        return self.quit_pressed()
        return None

    def new_game_pressed(self):
        self.show_menu = False
        return

    def quit_pressed(self):
        pg.event.post(pg.event.Event(pg.QUIT))
        return

    def init_graphics(self):
        new_game = self.pgtext_factory.create_text("1. New Game", RED, 100, 100)
        quit_game = self.pgtext_factory.create_text("2. Quit", RED, 100, 150)
        self.buttons = [new_game, quit_game]

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)
