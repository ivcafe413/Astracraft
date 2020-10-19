import pygame

class Spritesheet():
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def getImage(self, x, y, w, h):
        image = pygame.Surface([w, h]).convert()
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        image.set_colorkey((255, 255, 255))
        
        return image