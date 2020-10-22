import pygame

from engine.actors.Player import Player # TODO: Dependency Injection to handle game object types

class GameState:
    def __init__(self):
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
        # No collision handling yet
        for o in self.gameObjects:
            o.update()