# -*- coding: utf-8 -*-
import logging

import pygame

from game import Game


# TODO: Turn this off when game ready
SKIP_NAME_INPUT = True


# The main function
def main():
    # Initialize logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Initialize pygame
    logger.debug("Initializing pygame")
    pygame.init()
    pygame.display.set_caption("AirController - Remastered")

    # Initialize game
    logger.debug("Initializing game")
    game = Game(skip_name_input=SKIP_NAME_INPUT)
    
    logger.debug("Quiting the game")
    pygame.quit()
    
    
if __name__ == "__main__":
    main()