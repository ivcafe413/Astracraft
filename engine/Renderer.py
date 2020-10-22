import pygame
from engine.Spritesheet import Spritesheet

class Renderer:
    def __init__(self, options):
        self.screen = pygame.display.set_mode((options.width, options.height))
        # Setting game in Driver now
        # self.game = options.game

    def render(self):
        self.screen.fill((34, 139, 34)) # Test Forest Green
        self.draw()
        # pygame.display.update() # Optimized, but not OpenGL friendly
        pygame.display.flip()

    def draw(self):
        # for o in self.game.gameObjects:
        #     o.draw(self.screen)
        x = 0
        y = 0
        self.spritesheet = Spritesheet("World blocks.png")
        Background = self.spritesheet.getImage(1, 1, 50, 50)
        for i in range(12):
            for j in range(16):
                self.screen.blit(Background, [x, y])
                x = x + 50
            x = 0
            y = y + 50
        self.game.gameObjects.draw(self.screen)