import pygame
import tensorflow as tf

from tf_agents.environments import tf_py_environment

from environment.AstracraftEnvironment import AstracraftEnvironment

tf.compat.v1.enable_v2_behavior()

# Set up display for rendering our Astracraft game
# We'll use pygame for this
pygame.init()
screen = pygame.display.set_mode((800, 600))

train_py_env = AstracraftEnvironment(800, 600)
eval_py_env = AstracraftEnvironment(800, 60)

train_env = tf_py_environment.TFPyEnvironment(train_py_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)