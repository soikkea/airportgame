# Testing splines

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import pygame

from colors import BLACK, RED, WHITE, GREEN
import pgtext
import splines


class Entity:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.path = None
        self.path_pos = 0
        self.speed = 1
    
    def set_path(self, path):
        self.path = path
        self.path_pos = 0
    
    def update(self, elapsedTime):
        if self.path is not None:
            dist = self.speed * elapsedTime
            self.path_pos += dist
            x, y = self.path.get_point_by_length(self.path_pos)
            self.x = int(x)
            self.y = int(y)

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 5)


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    texter = pgtext.PgText("Consolas")

    points = []

    spline = None

    obj = Entity()

    clock = pygame.time.Clock()
    elapsed_time = clock.tick(60)

    running = True
    while running:

        elapsed_time = clock.tick(60)

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
                obj.set_path(spline)


        obj.update(elapsed_time)

        
        # *** DRAWING ***
        screen.fill(BLACK)
        spline_length = -1
        if spline is not None:
            spline.draw(screen)
            spline_length = spline.get_length()
        for point in points:
            pygame.draw.circle(screen, RED, point, 5)
            #logger.debug("Point drawn at x: %d, y: %d", *point)
        obj.draw(screen)
        texter.display_text(f"{spline_length}", screen, color=WHITE)
        pygame.display.flip()


if __name__ == '__main__':
    main()
    pygame.quit()