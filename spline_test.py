# Testing splines

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import pygame

from colors import BLACK, RED, WHITE
import pgtext
import splines

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    texter = pgtext.PgText("Consolas")

    points = []

    spline = None

    running = True
    while running:

        # *** EVENT HANDLING ***
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_c):
                points.clear()
                spline = None
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                points.append((mouse_x, mouse_y))
                logger.debug("Clicked x: %d, y: %d", mouse_x, mouse_y)
                spline = splines.CatmullRom(points)

        
        # *** DRAWING ***
        screen.fill(BLACK)
        spline_length = -1
        if spline is not None:
            spline.draw(screen)
            spline_length = spline.get_length()
        for point in points:
            pygame.draw.circle(screen, RED, point, 5)
            #logger.debug("Point drawn at x: %d, y: %d", *point)
        texter.display_text(f"{spline_length}", screen, color=WHITE)
        pygame.display.flip()


if __name__ == '__main__':
    main()
    pygame.quit()