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

    # Main game loop
    while running:
        # Event handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        # Update text input
        if game.textinput.is_active:
            game.textinput.update(events)

        game.update()
        game.draw(screen)
    
    pygame.quit()
    
if __name__ == "__main__":
    main()