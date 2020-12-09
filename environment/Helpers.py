import numpy as np

__objectTypes = {
    "Player": 1,
    "Hitzone": 2
}

def GameStateToObservation(gameState):
    # Initialize the observation array
    # observation = np.zeros((2,3), dtype=np.int32)
    observation = []
    for o in gameState.gameObjects:
        # left = o.left
        # right = o.right
        # top = o.top
        # bottom = o.bottom
        observation.append((o.rect.x, o.rect.y, __objectTypes.get(o.__class__.__name__)))
        # Set values in the observation array
        # for x in range(left, right):
        #     for y in range(top, bottom):
        #         observation[x][y] = np.array([__objectTypes.get(o.__class__.__name__)], dtype=np.int32)
    
    # Return the modified observation array
    # print("Observation: {0}".format(observation))
    return np.array(observation, dtype=np.int32)