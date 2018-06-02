# -*- coding: utf-8 -*-
import logging

import pygame

from game import Game

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
    game = Game()
    
    logger.debug("Quiting the game")
    pygame.quit()
    
if __name__ == "__main__":
    main()