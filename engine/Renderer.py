import pygame

class Renderer:
    def __init__(self, options):
        self.screen = pygame.display.set_mode((options.width, options.height))
        self.game = options.game

    def render(self):
        self.screen.fill((34, 139, 34)) # Test Forest Green
        self.draw()
        pygame.display.update()

    def draw(self):
        for o in self.game.gameObjects:
            o.draw(self.screen)