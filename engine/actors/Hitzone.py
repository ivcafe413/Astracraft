import pygame

from engine.actors.GObject import GObject

class Hitzone(GObject):
    def __init__(self, options):
        super().__init__(options)

        self.collidable = True
    
    def playerhit(self, player):
        # Occurs on player hitting a hitzone
        pass

    def drawDebug(self, surface):
        # pygame.draw.rect(surface, self.color, self.rect)
        # surface.blit(self.image, self.rect)
        pass