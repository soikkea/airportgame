# -*- coding: utf-8 -*-
"""Main function, initializes pygame and starts the game."""

import logging

import pygame

from airportgame.game import Game


SKIP_NAME_INPUT = False


def main():
    """The main function."""
    # Initialize logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Initialize pygame
    logger.debug("Initializing pygame")
    pygame.init()
    pygame.display.set_caption("AirController - Remastered")

    # Initialize game
    logger.debug("Initializing game")
    Game(skip_name_input=SKIP_NAME_INPUT)

    logger.debug("Quiting the game")
    pygame.quit()


if __name__ == "__main__":
    main()
