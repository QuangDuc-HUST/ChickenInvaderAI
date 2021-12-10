# from Model import Space
import copy

def Manhattan(x, y):
    '''
    x: (x1,x2)
    y: (y1,y2)
    return Manhattan distance of two points
    '''
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def heuristic(space):
    '''
    Idea: 
    bases on lazers, and how close the eggs to the spaceship by Manhattan distance.
    ship vs eggs:

    :-99 * space.height * 2 if distance  = 0 
    : - space.height * 2  + Manhattan distance
    : 0 if in the bottom 

    bullets and chickens: (effectiveness of the bullets)

    :1 lazers : space.height 
    :3 * distance or 0

    ship vs chickens:
    : 3* (space.height * 2 - Manhattan distance)

    args:
    return int value 
    '''

    ship = space.spaceship.get_position()
    lstbullets = [x.get_position() for x in space.bullets]
    lstinvaders = [x.get_position() for x in space.invaders]
    lsteggs = [x.get_position() for x in space.eggs]

    result = 0

    dic = {}

    for invader in lstinvaders:
        y = invader[1]
        if y not in dic:
            dic[y] = [invader]
        else:
            dic[y].append(invader)
        
    ## Eggs and ship:
    for egg in lsteggs:
        currentdistant = Manhattan(egg, ship)
        if not currentdistant: 
            result -= 99 * space.height * 2
        elif egg[0] == space.height - 1:
            continue
        else:
            result += (-space.height * 2 + currentdistant)
    
    for bullet in lstbullets:
        ybullet = bullet[1]
        if ybullet in dic:
            result += 3 * space.height

    for invader in lstinvaders:
        result += 3 * (space.height * 2 - Manhattan(invader, ship))
    return result

def nextSpace(space, action):

    newspace = copy.deepcopy(space)

    for bullet in newspace.bullets:
        bullet.move()

    for invader in newspace.invaders:
        for bullet in newspace.bullets:
            if bullet.collide(invader):
                newspace.bullets.remove(bullet)
                newspace.invaders.remove(invader)
                newspace.figure[bullet.x, bullet.y ] -=8
    
    newspace.spaceship.move(action)

    for egg in newspace.eggs.copy():
        egg.drop()

    return newspace



def ASearch(space):
    '''
    Depth-limited search , fixed = 2
    return: lst of 2 actions
    '''
    MIN = -99 * space.height * 1.5
    ACTIONS = ['a', 'd' , 'w', 'remain']
    max = -float('inf')
    maxaction = ['remain', 'remain']


    for firstaction in ACTIONS:
        #######!!!!!!!!!!!########### Becareful: End game
        firstspace = nextSpace(space, firstaction)
        # print('First space')
        # print(f'Done action: {firstaction}')
        # print(firstspace.figure)
        if heuristic(firstspace) < MIN:
            continue
        for secondaction in ACTIONS:
            secondspace = nextSpace(firstspace, secondaction)
            heu = heuristic(secondspace)
            # print(f'{firstaction}, {secondaction}, {heu}')

            if heu > max:
                max = heu
                maxaction= [firstaction, secondaction]

    return maxaction


def testAsearch(space, depth: int):
    if not space.step % 3:
        actions = input('First actions: ')
    else:
        actions = ASearch(space)
    return actions


def miniMax(space, depth:int):
    '''
    Idea: fixed depth, in deterministic phrase: Using A* search but we consider it just one ply(2 actions).
    Warning: There might be a tranposition table in this state. 
    args:

    '''
    pass

## Minimax

def miniMax_desicion(space, depth: int):

    pass

def maxValue(space):
    pass

def minValue(space):
    pass

def MCTS(space, depth: int):
    '''
    Idea: Using monte carlo search for working with this state
    https://youtu.be/UXW2yZndl7U
    '''

    pass

def testinputOffline(space, depth:int):
    actions = input('Plz: ').split()
    return actions






if __name__ == '__main__':
    print(Manhattan([1,2], [-4,7]))
