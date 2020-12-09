from tf_agents.environments import utils
# import pygame
from environment.AstracraftEnvironment import AstracraftEnvironment

# pygame.display.set_mode((800, 600))
environment = AstracraftEnvironment(800, 600)
utils.validate_py_environment(environment, episodes=1)