import os
import pygame

from constants import ROOT_PATH

class Spritesheet():
    def __init__(self, filename):
        # Will hardcode asses reference for now        
        spritesheetfile = os.path.join(ROOT_PATH, 'game', 'assets', filename)
        print(spritesheetfile)
        self.spritesheet = pygame.image.load(spritesheetfile).convert()

    def getImage(self, x, y, w, h):
        image = pygame.Surface([w, h]).convert()
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        image.set_colorkey((255, 255, 255))
        
        return image