import copy
import heapq


class Node:
    def __init__(self, figure, heuristic, invaders, eggs, bullets, ship_y, move):
        self.f = figure
        self.h = heuristic
        self.e = eggs
        self.i = invaders
        self.m = move
        self.b = bullets
        self.ship_y = ship_y

    def __lt__(self, other):
        return self.h < other.h


def greedy_bfs(space):
    ###########
    cost_of_success_bullets = 2
    cost_of_failed_bullets = 1
    cost_of_success_in_layer1 = 99
    cost_of_good_moves = 1
    cost_of_bad_moves = 1
    # changing environment function
    # eggs dropping

    def change_eggs(figure, eggs):
        next_egg = []
        for x, y in eggs:
            figure[x][y] -= 4
            if x + 1 < len(figure):
                figure[x + 1][y] += 4
                next_egg.append((x + 1, y))
        return figure, next_egg
    # bullets moving

    def change_bullets(figure, invaders, bullets):
        next_bullet = []
        for x, y in bullets:
            figure[x][y] -= 7
            if (x - 1, y) in invaders:
                figure[x - 1][y] -= 1
            elif (x - 2, y) in invaders:
                figure[x - 2][y] -= 1
            else:
                if x - 2 >= 0:
                    figure[x - 2][y] += 7
                    next_bullet.append((x - 2, y))

        return figure, [(x, y) for x, y in invaders if figure[x][y] == 1], next_bullet
    # heuristic functions

    # 1.Success of bullet
    # a bullet is considered to be a good one is the bullet that will kill a invaders in the future
    # if it is a efficient action, it will lose points since we want to minimize the heuristic point,
    # otherwise, it will get points
    def heuristic1(figure, current_y, point):
        column = [figure[t][current_y] for t in range(h)]
        success_bullets = False
        failed_bullets = False
        success_in_layer1 = False
        # if this column has invaders that need to be killed, we shoot and lose points
        if column.count(1) >= column.count(7) + column.count(11):
            # we prefer to kill invaders in the column that has 2 of them to kill invaders in the column that has only
            # 1 invader to avoid bad situations
            success_bullets = True
            if column.count(1) == 2 and column.count(7) + column.count(11) == 1:
                success_in_layer1 = True
        # otherwise we get point
        else:
            failed_bullets = True
        return point - cost_of_success_bullets * success_bullets + cost_of_failed_bullets * failed_bullets \
               - cost_of_success_in_layer1 * success_in_layer1
    # 2.Making better move
    # If our move in this turn is better than that of the last one, which mean the ship move closer to the
    # columns that contain invaders, it will lose point, otherwise, it will get point.
    # As i said before, we always want to kill invaders in column that has 2 of them so we tend to move to these columns
    # rather than the others

    def heuristic2(figure, previous_move, current_move, point):
        invaders_columns = []
        # find the maximum number of invaders in 1 column
        max_invaders = 0
        for i in range(w):
            col = [figure[k][i] for k in range(h)]
            t = col.count(1) - col.count(7) - col.count(11)
            if t > max_invaders:
                max_invaders = t

        for i in range(w):
            col = [figure[k][i] for k in range(h)]
            # looking for columns that has maximum invaders
            if col.count(1) == col.count(7) + col.count(11) + max_invaders:
                invaders_columns.append(i)
        try:
            # return True if the current action can lead the ship closer to the column
            good_move = min([abs(current_move - k) for k in invaders_columns]) <= min([abs(previous_move - k) for k in
                                                                                       invaders_columns])
        except ValueError:
            # ValueError may occur when we finish the game i.e. all invaders are removed before reach goal state
            good_move = False

        return point + cost_of_bad_moves * (1 - good_move) - cost_of_good_moves * good_move

    # function that check if we reach the goal state

    def no_eggs_in_space(f1):
        for i in range(len(f1)):
            for j in range(len(f1[i])):
                if f1[i][j] in [4, 11]:
                    return False
        return True
    # some variables of the environment
    figure = list([list(i) for i in space.figure])
    invaders_positions = [(i.x, i.y) for i in space.invaders]
    eggs_positions = [(i.x, i.y) for i in space.eggs]
    bullets_positions = [(i.x, i.y) for i in space.bullets]
    ship_x, ship_y = space.spaceship.x, space.spaceship.y
    w, h = space.width, space.height
    # check whether the ship shoot before
    if figure[ship_x - 3][ship_y] in [7, 11]:
        previous_state = ['w']
    else:
        previous_state = ['a or d or remain']
    # create list for heap using
    A = []
    # push the current states to the heap
    heapq.heappush(A, Node(figure, 0, invaders_positions, eggs_positions, bullets_positions, ship_y, previous_state))
    while True:
        # pop the best state
        state = heapq.heappop(A)
        # because when we get the information about the environment, its bullets and invaders were changed,
        # we do the rest which is egg dropping
        f, e = change_eggs(state.f, state.e)
        # check if we reach the terminal state
        if no_eggs_in_space(f):
            if len(state.m) == 1:
                # just for dealing with the first few steps which the states have the 'goal state property'
                # in these case, we just shoot, then move, then shoot...
                return 'w' if state.m[0] == 'a or d or remain' else 'a'
            else:
                # return the first action in the best sequence of actions
                return state.m[1]
        else:
            # if we shot in the previous turn, this turn we can not shoot
            if state.m[-1] == 'w':
                possible_moves = ['a', 'd', 'remain']
            else:
                possible_moves = ['w', 'a', 'd']
            for move in possible_moves:
                # make copies
                # temp stands for temporary
                f_temp = copy.deepcopy(f)
                i_temp = copy.deepcopy(state.i)
                b_temp = copy.deepcopy(state.b)
                temp_point = state.h
                temp_path = state.m
                if move == 'a':
                    if state.ship_y - 1 == -1:
                        continue
                    temp_y = state.ship_y - 1
                elif move == 'd':
                    if state.ship_y + 1 == w:
                        continue
                    temp_y = state.ship_y + 1
                else:
                    temp_y = state.ship_y
                    if move == 'w':
                        f_temp[h - 2][state.ship_y] += 7
                        b_temp.append((h - 2, state.ship_y))
                        temp_point = heuristic1(f_temp, state.ship_y, temp_point)
                # move the ship in the grid
                f_temp[h - 1][state.ship_y] -= 2
                f_temp[h - 1][temp_y] += 2
                temp_point = heuristic2(f_temp, state.ship_y, temp_y, temp_point)
                # collision checking
                if (h - 1, temp_y) not in e:
                    # if that actions don't lead to collision with an egg, we will go for it
                    f_temp, i_temp, b_temp = change_bullets(f_temp, i_temp, b_temp)
                    heapq.heappush(A, Node(f_temp, temp_point, i_temp, e, b_temp, temp_y, temp_path + [move]))
