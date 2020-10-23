from itertools import islice

def PlayerHitzoneCollision(player, hitzone1):
    # Player colliding with solid object
    # Calculate impact vector
    
    pass

__pairCompare = {("Player", "Hitzone"): PlayerHitzoneCollision}

def CollisionHandler(objects):
    # Two or more objects are colliding in an area
    # Need to determine resolution order

    # Who was moving
    movingObjects = list(filter(lambda mo: mo.moving, objects))
    # nonMovingObjects = list(set(objects) - set(movingObjects))

    # Analyze each moving object
    for mo in movingObjects:
        # allOthers = islice(objects, 1, None)
        allOthers = list(set(objects) - set([mo]))
        for other in allOthers:
            # Make sure two objects are indeed touching
            if mo.bounds.colliderect(other.bounds):
                # Run pair collision function (switcher)
                collisionFunc = __pairCompare.get(
                    (mo.__class__.__name__, other.__class__.__name__)
                )
                collisionFunc(mo, other)
