# from Model import Space
import copy
import random

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
    :2 * space height or 0

    ship vs chickens:
    : 3* (space.height * 2 - Manhattan distance)

    args:
    return int value 
    '''
    if space is None:
        return -INF

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
            result += 0.9 *(-space.height * 2 + currentdistant)
    
    for bullet in lstbullets:
        ybullet = bullet[1]
        if ybullet in dic:
            result += 2 * space.height

    for invader in lstinvaders:
        result +=   2.5 * (space.width - abs(invader[1] - ship[1]) )
    return result




def nextSpace(space, action, isAction = True, improveStep = False):

    newspace = copy.deepcopy(space)
    if improveStep:
        newspace.step += 1
    # print(f'Next space step: {newspace.step}')
    for bullet in newspace.bullets:
        bullet.move()

    for invader in newspace.invaders:
        for bullet in newspace.bullets:
            if bullet.collide(invader):
                newspace.bullets.remove(bullet)
                newspace.invaders.remove(invader)
                newspace.figure[bullet.x, bullet.y ] -=8
    if isAction:
        newspace.spaceship.move(action)

    for egg in newspace.eggs.copy():
        egg.drop()

    newspace.invader_actions()
    # print(f'OLD SPACE: {space}')
    # print(f'NEW SPACE: {newspace}')
    return newspace

def nextSpacever2(space,action):
    '''
    Just environment and actions
    '''
    newspace = copy.deepcopy(space)
    if not newspace.step % 3:
        print('You are the right phrase.')
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

def nextSpacever3(space):
    '''
    Just invaders
    '''
    newspace = copy.deepcopy(space)
    newspace.invader_actions()
    return newspace



def ASearch(space, isNext = True):
    '''
    Depth-limited search , fixed = 2
    return: lst of 2 actions
    '''
    MIN = -99 * space.height * 1.5
    ACTIONS = ['a', 'd' , 'w', 'remain']
    max = -float('inf')
    maxactions = ['remain', 'remain']

    ## Testing
    maxSpace = nextSpace(space, ACTIONS[0], True, True)

    ## For minimax

    for firstaction in ACTIONS:
        #######!!!!!!!!!!!########### Becareful: End game
        if isNext:
            firstspace = nextSpace(space, firstaction)
        else:
            firstspace = nextSpace(space, firstaction, True, True)
        # print(f'First space step: {firstspace.step}')
        if heuristic(firstspace) < MIN:
            continue
        for secondaction in ACTIONS:
            secondspace = nextSpace(firstspace, secondaction, True, True)
            heu = heuristic(secondspace)
            # print(f'{firstaction}, {secondaction}, {heu}')

            if heu > max:
                max = heu
                maxactions= [firstaction, secondaction]
                maxSpace = secondspace

    return maxactions , maxSpace


def testAsearch(space, depth: int):
    if not space.step % 3:
        actions = input('First actions: ')
    else:
        actions, _ = ASearch(space)
    return actions



def nextnextSpace(space, action):

    newspace = nextSpace(space, action, True, True)

    _ , newspace = ASearch(newspace, False)

    return newspace


## Minimax
### Auxiliary function

ACTIONS = ['remain', 'a', 'd', 'w']
INF = float('inf')

def terminal_test(space):
    '''
    state : 'Space'
    return Boolean weather terminal or not
    '''
    for egg in space.eggs.copy():
        if space.spaceship.collide(egg):
            return True

    return space.check_winning()
    

def utility(state):
    return heuristic(state)


def miniMax_desicion(space, depth:int, maxPlayer):
    '''
    return utility
    '''
    if depth == 0 or terminal_test(space):
        return utility(space)
    
    if maxPlayer:
        maxEval = -INF
        for action in ACTIONS:
            evaluate = miniMax_desicion(nextSpace(space, action), depth - 1, False)
            maxEval = max(maxEval, evaluate)
        return maxEval
    
    else:
        minEval = INF
        for action in ACTIONS:
            evaluate = miniMax_desicion(nextSpace(space, action), depth - 1, True)
            # print(f'EVALUATE : {evaluate} , action : {action}')
            minEval = min(minEval, evaluate)
        return minEval
    

def miniMax_seletion(space, depth:int):
    '''
    return action based on miniMax_desicion
    '''
    maxvalue = -INF
    maxAction = None
    for action in ACTIONS:
        eva = miniMax_desicion(nextSpace(space, action), depth - 1, False)
        # print(eva)
        if eva > maxvalue:
            maxvalue = eva
            maxAction = action

    return maxAction


def miniMax(space, depth:int):
    '''
    Idea: fixed depth, in deterministic phrase: Using A* search but we consider it just one ply(2 actions).
    Warning: There might be a tranposition table in this state. 
    args:
    space: Space
    depth : depth
    return action
    '''
    if not space.step % 3:
        actions = miniMax_seletion(space, depth)
        # print(f'ACTIONS AFTER MINIMAX: {actions}')
    else:
        actions, _ = ASearch(space)
    return actions


## Expectimax Pseudocode
def successors(space):
    '''
    state: 'Space'
    return list of (state, probability)
    Demo: Just 2 leaf
    '''
    a = random.random()
    newspace1 = nextSpacever3(space)
    _, newspace1 = ASearch(newspace1, False)
    newspace2 = nextSpacever3(space)
    _,newspace2 = ASearch(newspace2, False)
    return [[newspace1, a ], [newspace2, 1 - a]]


        
def value(space, depth, maxPlayer):

    if depth == 0 or terminal_test(space):
        return utility(space)
    
    if maxPlayer:
        maxEval = -INF
        for action in ACTIONS:
            evaluate = value(nextSpacever2(space, action), depth - 1, False)
            maxEval = max(maxEval, evaluate)
        return maxEval
    
    else:
        v = 0
        for suc, pro in successors(space):
            v += value(suc, depth - 1, True) * pro
        # print(v)
        return v

def expectimax(space, depth:int):
    '''
    return action based on value
    '''
    maxvalue = -INF
    maxAction = None
    for action in ACTIONS:
        print('Start explore ' + action)
        eva = value(nextSpacever2(space, action), depth - 1, False)
        print(f'EVA: {eva} in action {action}')
        if eva > maxvalue:
            maxvalue = eva
            maxAction = action

    return maxAction


def expectimax_input(space, depth: int):
    if not space.step % 3:
        actions = expectimax(space, depth)
    else:
        actions , _ = ASearch(space)
    
    return actions


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
