from Model import Space

def heuristic(space:'Space'):
    '''
    Idea: 
    bases on lazers, and how close the eggs to the spaceship by Manhattan distance.
    :-9 * space.height * 2 if distance  = 0
    : 1 lazers : Space.height 
    : - space.height * 2  + Manhattan distance
    args:
    return int value 
    '''
    pass

def ASearch(space: 'Space'):
    '''
    Depth-limited search , fixed = 3
    return: lst of 2 actions
    '''
    pass



def miniMax(space:'Space', depth:int):
    '''
    Idea: fixed depth, in deterministic phrase: Using A* search but we consider it just one ply(3 actions).
    Warning: There might be a tranposition table in this state. 
    args:

    '''
    pass


def testinputOffline(space:'Space', depth:int):
    actions = input('Plz: ').split()
    return actions

