# System level imports
import sys
import logging
from collections import defaultdict

# Third-party imports
import pygame

# Project package imports
from engine.GameState import GameState
from engine.Renderer import Renderer

# Constants
TARGET_FPS = 60
LOOP_MS_PF = (1 / TARGET_FPS) * 1000

# Class definition
class Driver:
    # Constructor function, creates new instance of class
    def __init__(self): # 0 additional arguments, self is self-reference
        pygame.init()

        # Renderer, handles rendering functions on behalf of the game
        rendererOptions = type('', (), {})()
        rendererOptions.width = 800
        rendererOptions.height = 600
        self.gameRenderer = Renderer(rendererOptions)
        # Renderer before GameState, since Spritesheet depends on display.set_mode
        
        # Game state object, tracks state of game and all objects in game
        self.gameState = GameState() # Example of tightly coupled code.
        # TODO: Refactor coupled code, separate dependencies
        self.gameRenderer.game = self.gameState

        # Internal variables to handle frame ticks/FPS
        self.clock = pygame.time.Clock()
        self.currentTime = 0

        # Event Handler dictionaries
        self.keydownHandlers = defaultdict(list)
        self.keyupHandlers = defaultdict(list)

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

    def start(self):
        # Initial Key Bindings
        # Sets actions for both key up and key down
        # Could also handle other events (mouse events, etc.)
        self.keydownHandlers[pygame.K_LEFT].append(self.gameState.action_left)
        self.keydownHandlers[pygame.K_RIGHT].append(self.gameState.action_right)
        self.keydownHandlers[pygame.K_UP].append(self.gameState.action_up)
        self.keydownHandlers[pygame.K_DOWN].append(self.gameState.action_down)

        self.keyupHandlers[pygame.K_LEFT].append(self.gameState.action_left)
        self.keyupHandlers[pygame.K_RIGHT].append(self.gameState.action_right)
        self.keyupHandlers[pygame.K_UP].append(self.gameState.action_up)
        self.keyupHandlers[pygame.K_DOWN].append(self.gameState.action_down)

        # Game Loop Start
        # TODO: Implement some kind of "done/not done", not infinite loop
        while True:
            # Increment time tracker with ms passed since last call
            self.currentTime += self.clock.get_time()
            # Process current event queue
            self.handle_events()

            # While enough time has passed to process at least one frame
            while self.currentTime >= LOOP_MS_PF:
                # Update the game state one tick for each frame time block
                self.gameState.update() # Passing in update MS diff?
                self.currentTime -= LOOP_MS_PF

            # Once game state is caught up, render the game
            self.gameRenderer.render() # TODO: Passing in leftover ticks for delta rendering?
            # self.gameRenderer.drawDebug() # TODO: Need to comment this out for live

            # Tracking FPS in window caption, should be for debug only
            fps = self.clock.get_fps()
            pygame.display.set_caption("FPS: {0:2f}".format(fps))

            # Tell the system to wait until enough time has passed to hit the next frame
            self.clock.tick(TARGET_FPS)

def main():
    # Sets logging to display on information logs and above
    logging.basicConfig(level=logging.INFO)
    # Start the game
    Driver().start()