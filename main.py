"""
@author : Léo Imbert
@created : 04/10/2025
@updated : 04/10/2025
"""

from engine import *
import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #pygame.NOFRAME
        self.clock = pygame.time.Clock()
        self.running = True

        self.engine = Engine(0, 0, 360, 640, 0.2)
        self.engine.add_body(Rect(100, 100, 50, 50, vx=3, vy=2, color=RED))
        self.engine.add_body(Rect(260, 200, 80, 80, vx=-2, vy=1, color=BLUE))
        self.engine.add_body(Rect(0, 300, 100, 20, color=GREEN, static=True))

        self.run()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

            self.screen.fill(BLACK)

            self.engine.update()
            self.engine.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    Game()