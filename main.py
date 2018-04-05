# -*- coding: utf-8 -*-

import pygame

# The main function
def main():

    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("AirPortGame")

    # Screen surface that has the size of 800 x 600
    screen = pygame.display.set_mode((800, 600))

    # The running status of the game
    running = True

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    
if __name__ == "__main__":
    main()