import copy
import random

#Auxiliary function
def nextSpace(space, action, isAgent):

    newspace = copy.deepcopy(space)

    if isAgent:
    # print(f'Next space step: {newspace.step}')
        newspace.step += 1
        for bullet in newspace.bullets:
            bullet.move()

        for invader in newspace.invaders:
            for bullet in newspace.bullets:
                if bullet.collide(invader):
                    newspace.bullets.remove(bullet)
                    newspace.invaders.remove(invader)
                    newspace.figure[bullet.x, bullet.y ] -=8

        for egg in newspace.eggs.copy():
            egg.drop()   
        newspace.spaceship.move(action)

    else:

        

        newspace.invader_actions()
    # print(f'OLD SPACE: {space}')
    # print(f'NEW SPACE: {newspace}')
    return newspace

MAX_DEPTH = 4
MAX_RANDOM = 2
ACTIONS = ['w', 'a', 'd', 'remain']

def getpositions(space):

    ship = space.spaceship.get_position()
    lstbullets = [x.get_position() for x in space.bullets]
    lstinvaders = [x.get_position() for x in space.invaders]
    lsteggs = [x.get_position() for x in space.eggs]
    return ship, lstbullets, lstinvaders, lsteggs


def get_legal_actions(space):
    '''
    return lst of legal actions
    '''
    # available_actions = [True, True, True, True]
    # ship, lstbullets, lstinvaders, lsteggs = getpositions(space)
    # for egg in lsteggs:
    #     if egg[0] == 8:
    #         if ship[1] == egg[1] - 1:
    #             available_actions[1] = False
    #         elif ship[1] == egg[1] + 1:
    #             available_actions[2] = False
    #         elif ship[1] == egg[1]:
    #             available_actions
    if not space.spaceship.available:
        return ['a', 'd', 'remain']

    return ACTIONS

def nearest_invader(space):
    '''
    Return the distance of nearest invader
    '''
    ship, lstbullets, lstinvaders, lsteggs = getpositions(space)
    min = space.width + 10
    for invader in lstinvaders:
        temp = abs(invader[1] - ship[1])
        if temp < min:
            min = temp
    return min

def expected_chicken(space):
    '''
    return the number of real chicken
    '''
    ship, lstbullets, lstinvaders, lsteggs = getpositions(space)
    actual_chicken = len(lstinvaders)
    willdie_chicken = 0

    for i in range(space.width):
        chickens = 0
        bullets = 0
        for chicken in lstinvaders:
            if chicken[1] == i:
                chickens += 1
        
        for bullet in lstbullets:
            if bullet[1] == i:
                bullets += 1

        willdie_chicken += min(chickens, bullets)
    
    return actual_chicken - willdie_chicken

def evaluate(space):
    '''
    return evaluate value of the state.
    '''
    ship, lstbullets, lstinvaders, lsteggs = getpositions(space)

    for egg in lsteggs:
        if egg == ship:
            return -float('inf')

    result = -nearest_invader(space)
    result -= expected_chicken(space) * 3



    # dic = {}

    # for invader in lstinvaders:
    #     y = invader[1]
    #     if y not in dic:
    #         dic[y] = [invader]
    #     else:
    #         dic[y].append(invader)
        
    # ## Eggs and ship:
    # for egg in lsteggs:
    #     currentdistant = Manhattan(egg, ship)
    #     if not currentdistant: 
    #         result -= 99 * space.height * 2
    #     elif egg[0] == space.height - 1:
    #         continue
    #     else:
    #         result += 0.9 *(-space.height * 2 + currentdistant)
    
    # for bullet in lstbullets:
    #     ybullet = bullet[1]
    #     if ybullet in dic:
    #         result += 2 * space.height

    # for invader in lstinvaders:
    #     result +=   2.5 * (space.width - abs(invader[1] - ship[1]) )

    return result




def expectimax_getaction(space):
    '''
    return an action else remain
    '''
    score, actions = maxValue(space, 0)
    return actions[0] if len(actions) > 0 else 'remain'


def maxValue(space, depth):
    '''
    return maxScore and maxScoreActions
    '''
    if space.check_winning() or space.check_losing() or depth == MAX_DEPTH:
        return evaluate(space), []

    max_score = float('-inf')
    max_score_actions = None

    legal_actions = get_legal_actions(space)

    for action in legal_actions:
        score, actions = expectedValue(nextSpace(space, action, True), depth)
        if score > max_score:
            max_score = score
            max_score_actions = [action] + actions
        
    
    return max_score, max_score_actions

def expectedValue(space, depth):
    '''
    return expected score
    '''
    if space.check_winning() or space.check_losing() or depth == MAX_DEPTH:
        # print(f'depth: {depth}')
        return evaluate(space), []
    
    expected_score = 0

    if space.step % 3:
        rd =  1
    else:
        rd  = MAX_RANDOM

    for _ in range(rd):
        score, actions = maxValue(nextSpace(space, 'remain', False), depth + 1)
        expected_score += score / rd
        # print(MAX_RANDOM)


    return expected_score , []
    





if __name__ == '__main__':
    print('Hello')
