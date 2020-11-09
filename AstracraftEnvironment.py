import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

from engine.GameState import GameState

class AstracraftEnvironment(py_environment.PyEnvironment):
    def __init__(self, screen_width, screen_height):
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(screen_width, screen_height, 1),
            dtype=np.int32,
            minimum=0,
            name='observation'
        )
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(1,),
            dtype=np.int32,
            minimum=0,
            maximum=8,
            name='action'
        )
        self._game_state = GameState()
        self._state = self._game_state.gameObjects
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec
    
    def _reset(self):
        self._game_state = GameState()
        self._state = self._game_state.gameObjects
        self._episode_ended = False
        # return ts.restart(np.array([self._state], dtype=np.int32))