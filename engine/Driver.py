# System level imports
import logging

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
        # pygame.init()
        # Moving pygame display.set_mode out of Renderer/GameState to remove dependency
        gameWidth = 800
        gameHeight = 600
        # Game state object, tracks state of game and all objects in game
        self.gameState = GameState(gameWidth, gameHeight)
        # screen = pygame.display.set_mode((gameWidth, gameHeight))

        # Renderer, handles rendering functions on behalf of the game
        rendererOptions = type('', (), {})()
        rendererOptions.width = gameWidth
        rendererOptions.height = gameHeight
        # rendererOptions.screen = screen
        self.gameRenderer = Renderer(rendererOptions)
        # Renderer before GameState, since Spritesheet depends on display.set_mode
        
        # TODO: Refactor coupled code, separate dependencies
        self.gameRenderer.game = self.gameState

        # Internal variables to handle frame ticks/FPS
        self.clock = pygame.time.Clock()
        self.currentTime = 0

    def start(self):
        # Game Loop Start
        # TODO: Implement some kind of "done/not done", not infinite loop
        while True:
            # Increment time tracker with ms passed since last call
            self.currentTime += self.clock.get_time()
            
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