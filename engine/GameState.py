import pygame

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
        hitzoneOptions = type('', (), {})()
        hitzoneOptions.x = 400
        hitzoneOptions.y = 0
        hitzoneOptions.w = 20
        hitzoneOptions.h = 20
        hitzoneOptions.color = (255, 0, 0)

        self.hitzone = Hitzone(hitzoneOptions)
        self.gameObjects.add(self.hitzone)

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

    def update(self):
        collisionIndex = Index((0, 0, self.width, self.height))
        for o in self.gameObjects:
            o.update()
            if o.collidable:
                collisionIndex.insert(o, (o.rect.left, o.rect.top, o.rect.right, o.rect.bottom))

        for i in self.collidableObjects:
            collisions = collisionIndex.intersect((i.rect.left, i.rect.top, i.rect.right, i.rect.bottom))
            
            if(len(collisions) > 1): # Intersecting more than self
                # logging.info("Collision!")
                CollisionHandler(collisions)