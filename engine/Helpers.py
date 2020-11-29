import numpy as np

__objectTypes = {
    "Player": 1,
    "Hitzone": 2
}

def GameStateToObservation(gameState):
    # Initialize the observation array
    observation = np.zeros((gameState.env_width, gameState.env_height, 1), dtype=np.int32)
    for o in gameState.gameObjects:
        left = o.left
        right = o.right
        top = o.top
        bottom = o.bottom

        # Set values in the observation array
        for x in range(left, right):
            for y in range(top, bottom):
                observation[x][y] = np.array([__objectTypes.get(o.__class__.__name__)], dtype=np.int32)
    
    # Return the modified observation array
    return observation