#
#
# Source code: Greedy BFS Algorithm	
#
#

import copy

def nextSpace(space, action, isAgent, isIStep):
    """
    Return the copy of the space if the agent or the chickens do an action
    """
    newspace = copy.deepcopy(space)
    if isAgent:
        if isIStep:
            newspace.step += 1
        for bullet in newspace.bullets.copy():
            bullet.move()
        for invader in newspace.invaders.copy():
            for bullet in newspace.bullets.copy():
                if bullet.collide(invader):
                    newspace.bullets.remove(bullet)
                    newspace.invaders.remove(invader)
                    newspace.figure[bullet.x, bullet.y] -= 8

        for egg in newspace.eggs.copy():
            egg.drop()   
        newspace.spaceship.move(action)
    else:
        
        newspace.invader_actions()
    return newspace


ACTIONS = ['a', 'd', 'w', 'remain']


def getpositions(space):
    """
    Auxiliary function:
    Return position of objects, agents in the current state
    """
    ship = space.spaceship.get_position()
    lstbullets = [x.get_position() for x in space.bullets]
    lstinvaders = [x.get_position() for x in space.invaders]
    lsteggs = [x.get_position() for x in space.eggs]
    return ship, lstbullets, lstinvaders, lsteggs


def get_legal_actions(space):
    """
    Return lst of legal actions in current state
    """
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
    """
    Return the distance of nearest invader or to the middle if there is no chicken
    """
    ship, lstbullets, lstinvaders, lsteggs = getpositions(space)
    # big number
    min_distance = 100 * space.width
    if lstinvaders:
        for invader in lstinvaders:
            temp = abs(invader[1] - ship[1])
            if temp < min_distance:
                min_distance = temp
    else:
        min_distance = abs(ship[1] - space.width // 2)
    return min_distance


def top_egg(space):
    """
    Return the horizontal distance from the spaceship to the position of the consecutive eggs
    """
    ship, lstbullets, lstinvaders, lsteggs = getpositions(space)
    for egg1 in lsteggs:
        if egg1[0] in [2, 1]:
            for egg2 in lsteggs:
                if egg2 == egg1:
                    continue
                elif egg2[0] == egg1[0]:
                    if egg2[1] - egg1[1] in [1, -1]:
                        return abs(ship[1] - egg2[1])
    return space.width


def expected_chicken(space):
    """
    Return the number total of will-die and die chickens
    """
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
    
    return space.num - actual_chicken + willdie_chicken


def utility(space):
    """
    Return utility value of the state
    """
    ship, lstbullets, lstinvaders, lsteggs = getpositions(space)

    result = 0

    for egg in lsteggs:
        if egg == ship:
            result -= 3 * space.width

    result += space.width * expected_chicken(space)
    result -= nearest_invader(space)
    result -= top_egg(space)

    return result


def expectimax_getaction(space, maxdepth, randomdepth):
    """
    Return an action of the sequence else remain
    """
    score, actions = maxValue(space, 0, maxdepth, randomdepth)
    return actions[0] if len(actions) > 0 else 'remain'


def maxValue(space, depth, maxdepth, randomdepth):
    """
    Return maxScore, maxScoreActions in MAX agent
    """
    if space.check_winning() or space.check_losing() or depth == maxdepth:
        return utility(space), []

    max_score = float('-inf')
    max_score_actions = None

    legal_actions = get_legal_actions(space)

    for action in legal_actions:
        if not depth:
            score, actions = expectedValue(nextSpace(space, action, isAgent=True, isIStep=False), depth, maxdepth,
                                           randomdepth)
        else:
            score, actions = expectedValue(nextSpace(space, action, isAgent=True, isIStep=True), depth, maxdepth,
                                           randomdepth)
        if score > max_score:
            max_score = score
            max_score_actions = [action] + actions

    return max_score, max_score_actions


def expectedValue(space, depth, maxdepth, randomdepth):
    """
    Return expected score, [] in EXP agent
    """
    if space.check_winning() or space.check_losing() or depth == maxdepth:
        return utility(space), []
    
    expected_score = 0

    if space.step % 3:
        rd = 1
    else:
        rd = randomdepth

    for _ in range(rd):
        score, actions = maxValue(nextSpace(space, 'remain', isAgent=False, isIStep=True), depth + 1, maxdepth,
                                  randomdepth)
        expected_score += score / rd

    return expected_score, []
