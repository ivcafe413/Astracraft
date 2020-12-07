import pygame
import random

from pyqtree import Index

from engine.actors.Player import Player # TODO: Dependency Injection to handle game object types
from engine.actors.Hitzone import Hitzone
from engine.CollisionHandler import CollisionHandler

class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # self.gameObjects = [] # Array of game objects
        # Now using SpriteGroup
        self.gameObjects = pygame.sprite.Group()

        # Now tracking Game Win/Loss state variables
        self.timeElapsed = 0 # Keep track of total time (in frames) in GameState
        self.score = 0 # Initialize score to 0

        # keeping track of spaces
        self.emptySpaces = [*range(1, 97)]
        self.filledSpaces = []

        # Method to create anonymous object
        options = type('', (), {})()
        # TODO: Player/gameObject initialization needs to be config'd
        options.x = 400
        options.y = 300
        options.w = 20
        options.h = 20
        options.speed = 3
        options.color = (128, 128, 128)

        self.player = Player(options) # TODO: Dependency injection 
        # self.gameObjects.append(self.player)
        self.gameObjects.add(self.player)

        # First Hitzone
        # hitzoneOptions = type('', (), {})()
        # hitzoneOptions.x = 400
        # hitzoneOptions.y = 0
        # hitzoneOptions.w = 20
        # hitzoneOptions.h = 20
        # hitzoneOptions.color = (255, 0, 0)

        # self.hitzone = Hitzone(hitzoneOptions)
        # self.gameObjects.add(self.hitzone)

        self.collidableObjects = list(filter(lambda o: o.collidable == True, self.gameObjects))

        # Player Actions Available (type == Key Up or Down)
    def action_left(self, type):
        # Overworld
        self.player.toggle_movement("left")

    def action_right(self, type):
        self.player.toggle_movement("right")

    def action_up(self, type):
        self.player.toggle_movement("up")

    def action_down(self, type):
        self.player.toggle_movement("down")
    
    def FindPos(self):
        for x in self.filledSpaces:
            if x in self.emptySpaces:
                self.emptySpaces.remove(x)
        PosVar = random.choice(self.emptySpaces)
        self.filledSpaces.append(PosVar)
        if PosVar == 1:
            PosX=0
            PosY=0
        if PosVar == 17 or 33:
            PosX=0
            PosY=0
        if PosVar == 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 or 10 or 11 or 12 or 13 or 14 or 15 or 16:
            PosVar=PosVar-1
            PosX=50*PosVar
            PosY=0
        if PosVar == 18 or 19 or 20 or 21 or 22 or 23 or 24 or 25 or 26 or 27 or 28 or 29 or 30 or 31 or 32:
            PosVar=PosVar-17
            PosX=50*PosVar
            PosY=50

    def update(self):
        collisionIndex = Index((0, 0, self.width, self.height)) # Create the empty collision index (Quad Tree)
        self.timeElapsed += 1
        for o in self.gameObjects:
            o.update()
            if o.collidable:
                collisionIndex.insert(o, (o.rect.left, o.rect.top, o.rect.right, o.rect.bottom))

        for i in self.collidableObjects:
            collisions = collisionIndex.intersect((i.rect.left, i.rect.top, i.rect.right, i.rect.bottom))
            
            if(len(collisions) > 1): # Intersecting more than self
                # logging.info("Collision!")
                CollisionHandler(collisions)
        
        if self.timeElapsed % 180 == 0:
            for x in self.filledSpaces:
                if x in self.emptySpaces:
                    self.emptySpaces.remove(x)
            StnVar = random.choice(self.emptySpaces)
            self.filledSpaces.append(StnVar)
            StnVar = StnVar/2
            StnX = StnVar*50
            StnY = StnVar*50
            hitzoneOptions = type('', (), {})()
            hitzoneOptions.x = 0
            hitzoneOptions.y = 0
            hitzoneOptions.w = 50
            hitzoneOptions.h = 50
            hitzoneOptions.color = (255, 0, 0)

            self.hitzone = Hitzone(hitzoneOptions)
            self.gameObjects.add(self.hitzone)