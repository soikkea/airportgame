# -*- coding: utf-8 -*-

import pygame
from game import Game

# The main function
def main():

    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("AirController - Remastered")

    # Initialize game
    game = Game()
    
    pygame.quit()
    
if __name__ == "__main__":
    main()