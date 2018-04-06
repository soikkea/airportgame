# -*- coding: utf-8 -*-

import pygame
from game import Game

# The main function
def main():

    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("AirController - Remastered")

    # Screen surface that has the size of 800 x 600
    screen = pygame.display.set_mode((800, 600))

    # The running status of the game
    running = True

    # Initialize game
    game = Game()
    clock = pygame.time.Clock()

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.draw(screen)
    
    pygame.quit()
    
if __name__ == "__main__":
    main()