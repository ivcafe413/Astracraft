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
from environment.Helpers import GameStateToObservation

class AstracraftEnvironment(py_environment.PyEnvironment):
    def __init__(self, screen_width, screen_height):
        self.env_width = screen_width
        self.env_height = screen_height

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
        self._game_state = GameState(screen_width, screen_height)
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec
    
    def _reset(self):
        self._game_state = GameState(self.env_width, self.env_height)
        observation = GameStateToObservation(self._game_state)

        self._episode_ended = False
        return ts.restart(observation)

    def _step(self, action):
        # The episode is over, reset
        if self._episode_ended:
            return self.reset() # Returns the FIRST TimeStep

        # Action 0 = No move
        # Action 1-8 = Cardinal direction (1 = N, rotating clockwise)
        # Zero out all movement flags
        self._game_state.player.moving_up = 0
        self._game_state.player.moving_down = 0
        self._game_state.player.moving_left = 0
        self._game_state.player.moving_right = 0
        # Set flag for moving North
        if action in (8, 1, 2):
            self._game_state.player.moving_up = 1
        # East
        if action in (2, 3, 4):
            self._game_state.player.moving_right = 1
        # South
        if action in (4, 5, 6):
            self._game_state.player.moving_down = 1
        # West
        if action in (6, 7, 8):
            self._game_state.player.moving_left = 1
        # After applying chosen action/movement, update game state
        self._game_state.update()

        # Episode ends when time runs out, for a simple situation
        if self._game_state.timeElapsed >= 3600: # 60 FPS * 60 seconds = 3600 frames/time steps
            self._episode_ended = True

        observation = GameStateToObservation(self._game_state)
        if self._episode_ended:
            reward = self._game_state.score
            return ts.termination(observation, reward)
        else:
            time_step = ts.transition(observation, reward=0.0)
            print("Frames Elapsed: ", self._game_state.timeElapsed)
            return time_step
            

        