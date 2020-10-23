import pygame

from engine.actors.GObject import GObject

from constants import VICTORY_EVENT

# Custom Victory Event
# VICTORY_EVENT = pygame.USEREVENT+1

class Hitzone(GObject):
    def __init__(self, options):
        super().__init__(options)

        self.collidable = True
    
    def playerhit(self, player):
        # Occurs on player hitting a hitzone
        # print("Victory!")
        pygame.event.post(pygame.event.Event(VICTORY_EVENT))

    def drawDebug(self, surface):
        # pygame.draw.rect(surface, self.color, self.rect)
        # surface.blit(self.image, self.rect)
        pass