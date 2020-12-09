import sys
import math
import pygame

from collections import defaultdict
from pyqtree import Index

from engine.actors.Player import Player # TODO: Dependency Injection to handle game object types
from engine.actors.Hitzone import Hitzone
from engine.CollisionHandler import CollisionHandler

from constants import VICTORY_EVENT

class GameState:
    def __init__(self, width, height):
        # pygame.init()
        self.width = width
        self.height = height
        # self.screen = pygame.display.set_mode((width, height))
        # Now using SpriteGroup
        self.gameObjects = pygame.sprite.Group()

        # Now tracking Game Win/Loss state variables
        self.gameOver = False
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
        options.speed = 5
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

        # Event Handler dictionaries
        self.keydownHandlers = defaultdict(list)
        self.keyupHandlers = defaultdict(list)
        # Initial Key Bindings
        # Sets actions for both key up and key down
        # Could also handle other events (mouse events, etc.)
        # self.keydownHandlers[pygame.K_LEFT].append(self.action_left)
        # self.keydownHandlers[pygame.K_RIGHT].append(self.action_right)
        # self.keydownHandlers[pygame.K_UP].append(self.action_up)
        # self.keydownHandlers[pygame.K_DOWN].append(self.action_down)

        # self.keyupHandlers[pygame.K_LEFT].append(self.action_left)
        # self.keyupHandlers[pygame.K_RIGHT].append(self.action_right)
        # self.keyupHandlers[pygame.K_UP].append(self.action_up)
        # self.keyupHandlers[pygame.K_DOWN].append(self.action_down)

    # Event Handler function
    def handle_events(self):
        # pygame.event.get() clears the event queue, prevents crashing/freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydownHandlers[event.key]:
                    handler(event.type)
            elif event.type == pygame.KEYUP:
                for handler in self.keyupHandlers[event.key]:
                    handler(event.type)
            elif event.type == VICTORY_EVENT:
                # font = pygame.font.SysFont("sysfont10", 48)
                # text = font.render("VICTORY!!!", False, (255, 255, 255))
                # textRect = text.get_rect()
                # textRect.center = (400, 300)
                # self.gameRenderer.screen.blit(text, textRect)
                # pygame.display.flip()
                self.gameOver = True
                self.score = (1800 - self.timeElapsed)/60 # 30 seconds - (frames * 60FPS )
                # pygame.time.wait(1500)
                # pygame.quit()
                # sys.exit(0)

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
    
    # def FindPos(self):
    #     for x in self.filledSpaces:
    #         if x in self.emptySpaces:
    #             self.emptySpaces.remove(x)
    #     PosVar = random.choice(self.emptySpaces)
    #     self.filledSpaces.append(PosVar)
    #     if PosVar == 1:
    #         PosX=0
    #         PosY=0
    #     if PosVar == 17 or 33:
    #         PosX=0
    #         PosY=0
    #     if PosVar == 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 or 10 or 11 or 12 or 13 or 14 or 15 or 16:
    #         PosVar=PosVar-1
    #         PosX=50*PosVar
    #         PosY=0
    #     if PosVar == 18 or 19 or 20 or 21 or 22 or 23 or 24 or 25 or 26 or 27 or 28 or 29 or 30 or 31 or 32:
    #         PosVar=PosVar-17
    #         PosX=50*PosVar
    #         PosY=50

    def update(self):
        if(self.timeElapsed >= 100): # 30 seconds * 60fps = 1800 frames
            # GAME OVER - LOSE
            self.gameOver = True
            self.score = -(math.hypot(self.player.rect.x-self.hitzone.rect.x, self.player.rect.y-self.hitzone.rect.y)) # - distance from hitbox
            return
        
        collisionIndex = Index((0, 0, self.width, self.height)) # Create the empty collision index (Quad Tree)
        for o in self.gameObjects:
            o.update()
            if o.collidable:
                collisionIndex.insert(o, (o.rect.left, o.rect.top, o.rect.right, o.rect.bottom))

        for i in self.collidableObjects:
            collisions = collisionIndex.intersect((i.rect.left, i.rect.top, i.rect.right, i.rect.bottom))
            
            if(len(collisions) > 1): # Intersecting more than self
                # logging.info("Collision!")
                CollisionHandler(collisions)

        self.timeElapsed += 1
        # Process current event queue
        self.handle_events()
        
        # if self.timeElapsed % 180 == 0:
        #     for x in self.filledSpaces:
        #         if x in self.emptySpaces:
        #             self.emptySpaces.remove(x)
        #     StnVar = random.choice(self.emptySpaces)
        #     self.filledSpaces.append(StnVar)
        #     StnVar = StnVar/2
        #     StnX = StnVar*50
        #     StnY = StnVar*50
        #     hitzoneOptions = type('', (), {})()
        #     hitzoneOptions.x = 0
        #     hitzoneOptions.y = 0
        #     hitzoneOptions.w = 50
        #     hitzoneOptions.h = 50
        #     hitzoneOptions.color = (255, 0, 0)

        #     self.hitzone = Hitzone(hitzoneOptions)
        #     self.gameObjects.add(self.hitzone)
