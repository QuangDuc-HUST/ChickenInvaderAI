import copy

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

MAX_DEPTH = 3
MAX_RANDOM = 3
ACTIONS = ['a', 'd', 'w', 'remain']

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
    available_action = ACTIONS[:]
    ship, lstbullets, lstinvaders, lsteggs = getpositions(space)
    if not ship[1]:
        available_action.remove('a')
    
    if ship[1] == space.width - 1:
        available_action.remove('d')

    if not space.spaceship.available:
        available_action.remove('w')

    return available_action

def nearest_invader(space):
    '''
    Return the distance of nearest invader or to the middle if there is no chicken
    '''
    ship, lstbullets, lstinvaders, lsteggs = getpositions(space)
    min = 2.5 * space.width
    if lstinvaders:
        for invader in lstinvaders:
            temp = abs(invader[1] - ship[1])
            if temp < min:
                min = temp
    else:
        min = abs(ship[1] - space.width // 2)
    return min

def top_egg(space):
    '''
    return the number of eggs 
    '''
    ship, lstbullets, lstinvaders, lsteggs = getpositions(space)
    num = 0
    for egg in lsteggs:
        if egg[0] == 2: 
            if ship[1] == egg[1] - 1 or ship[1] == egg[1] or ship[1] == egg[1] + 1:
                num += 1
        
        # elif egg[0] == 2:
        #     if ship[1] == egg[1] - 1 or ship[1] == egg[1] or ship[1] == egg[1] + 1:
        #         num += 1
    return num

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

    result  = 0

    for egg in lsteggs:
        if egg == ship:
            result -=  4* space.width ## Die or not

    result -= expected_chicken(space) * 3 ## 
    result -= nearest_invader(space)
    result -= 2 * top_egg(space)


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
        # print(f'Action {action} : {score}')
        if score > max_score:
            max_score = score
            max_score_actions = [action] + actions
        
    
    return max_score, max_score_actions

def expectedValue(space, depth):
    '''
    return expected score
    '''
    if space.check_winning() or space.check_losing() or depth == MAX_DEPTH:
        return evaluate(space), []
    
    expected_score = 0

    if space.step % 3:
        rd =  1
    else:
        rd  = MAX_RANDOM

    for _ in range(rd):
        score, actions = maxValue(nextSpace(space, 'remain', False), depth + 1)
        expected_score += score / rd

    return expected_score , []
