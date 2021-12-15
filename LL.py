# slow but thorough
def online(space):
    def possible(x, y):
        # possible places mean that we can reach it within next few moves
        nonlocal space
        return abs(y - space.spaceship.y) <= space.spaceship.x - x

    def not_enough_bullets():
        nonlocal space
        no_of_invaders = len([i for i in space.invaders if i.y == space.spaceship.y])
        no_of_bullets = len([i for i in space.bullets if i.y == space.spaceship.y])
        return no_of_bullets < no_of_invaders

    def can_move_left():
        nonlocal space
        return space.spaceship.y - 1 >= 0 and space.figure[space.spaceship.x - 1][space.spaceship.y - 1] != 4

    def can_move_right():
        nonlocal space
        return space.spaceship.y + 1 <= space.width - 1 and space.figure[space.spaceship.x - 1][space.spaceship.y + 1] != 4

    def has_invaders(y):
        nonlocal space
        return y in [i.y for i in space.invaders]

    def action():
        nonlocal space
        # because in each rows there always exists some blanks for the ship to stay
        # so we will check the best blank position to move

        # find nearest row that has eggs
        nearest_row = None
        for i in range(1, space.height):
            if 4 in list(space.figure[space.spaceship.x - i]):
                nearest_row = space.spaceship.x - i
                break
        else:
            return 'w'
        # find the blank positions in this row
        blank_positions = [i for i in range(space.width) if space.figure[nearest_row][i] not in [4, 11]]

        # also make a list of dangerous places for later purposes
        danger = [i for i in range(space.width) if i not in blank_positions]
        # then sort the lists in the order of the distance from horizontal position of the ship to each of them
        blank_positions = sorted(blank_positions, key=lambda x: abs(x - space.spaceship.y))
        danger = sorted(danger, key=lambda x: abs(x - space.spaceship.y))

        # now we check if we are in the safe position or not
        # if we are safe, we will try to look for the next closest possible place that has better value in case there
        # are no invaders in front of us which may only happen with low probability or just stay in there
        # else we will move to the safe position

        if space.spaceship.y in blank_positions:
            if space.spaceship.y in [i.y for i in space.invaders] and not_enough_bullets():
                # shoot them
                return 'w'
            else:
                # now we will find the next closet possible position
                for i in blank_positions[1:]:
                    if possible(nearest_row, i) and has_invaders(i):
                        # determine to go left or right depends on this position
                        if i > space.spaceship.y and can_move_right():
                            return 'd'
                        elif i < space.spaceship.y and can_move_left():
                            return 'a'
                # else we have to try some threatening moves if we want to win the game
                else:
                    for i in danger:
                        if has_invaders(i):
                            if i > space.spaceship.y and can_move_right():
                                return 'd'
                            elif i < space.spaceship.y and can_move_left():
                                return 'a'
                    return 'w'
        else:
            # in here we can check whether it is necessary to move now
            # if not, we can shoot
            if abs(space.spaceship.y - blank_positions[0]) < space.spaceship.x - nearest_row:
                return 'w'

            # move to the safe place if work calls for it
            if blank_positions[0] > space.spaceship.y and can_move_right():
                return 'd'
            elif blank_positions[0] < space.spaceship.y and can_move_left():
                return 'a'
            return 'w'

    return action()

# Node
'''class Node:
    def __init__(self, figure, heuristic, invaders, eggs, bullets, ship_y, shoot, move):
        self.f = figure
        self.h = heuristic
        self.e = eggs
        self.i = invaders
        self.m = move
        self.b = bullets
        self.ship_y = ship_y
        self.s = shoot

    def __lt__(self, other):
        # inverse the heap
        return self.h > other.h


def search(space):
    import copy
    import heapq
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
    # checking if we reach the leaf of tree function

    def check(f):
        for i in range(len(f)):
            for j in range(len(f[i])):
                if f[i][j] in [4, 11]:
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
    # if it just fired, we can't should right now, we have to wait until the next step to fire
    if figure[ship_x - 3][ship_y] in [7, 11]:
        shoot = False
    else:
        shoot = True
    # creat list for using heap
    A = []
    # push the current states to the heap
    heapq.heappush(A, Node(figure, 0, invaders_positions, eggs_positions, bullets_positions, ship_y, shoot, []))
    # the heap will keep track of the state that has the highest heuristic
    while True:
        # pop the best state
        map = heapq.heappop(A)
        # because when we get the information about the environment, its bullets and invaders were changed,
        # we do the rest which is egg dropping
        f, e = change_eggs(map.f, map.e)
        # check if we reach the leaf
        if map.i == [] or check(f):
            if map.m == []:
                return 'w'
            else:
                print(map.m)
                print(map.h)
                return map.m[0]
        else:
            for move in ['w', 'a', 'd']:
                # make copies
                f_temp = copy.deepcopy(f)
                i_temp = copy.deepcopy(map.i)
                b_temp = copy.deepcopy(map.b)
                temp_point = map.h
                temp_shoot = map.s
                temp_path = map.m
                if move == 'a':
                    if map.ship_y - 1 == -1:
                        continue
                    temp_y = map.ship_y - 1
                    temp_shoot = True
                elif move == 'd':
                    if map.ship_y + 1 == w:
                        continue
                    temp_y = map.ship_y + 1
                    temp_shoot = True
                else:
                    temp_y = map.ship_y
                    if temp_shoot:
                        f_temp[h - 2][map.ship_y] += 7
                        b_temp.append((h - 2, map.ship_y))
                        # success of bullet
                        # a bullet is considered to be a good one is the bullet that will kill a invaders in the future
                        # if it is a efficient action, it will get points depends on the time that the bullet is shot
                        # the sooner it is shot, the larger points
                        # otherwise, it will loose points in the same way
                        column = [f_temp[t][map.ship_y] for t in range(h)]
                        if column.count(1) >= column.count(7) + column.count(11):
                            temp_point += 2 * (10 - len(map.m))
                        else:
                            temp_point -= 10 - len(map.m)
                    else:
                        temp_point -= 10 - len(map.m)
                    # change variable to make sure it cant shoot in the next step ( like the environment )
                    temp_shoot = not temp_shoot
                # move the ship in the grid
                f_temp[h - 1][map.ship_y] -= 2
                f_temp[h - 1][temp_y] += 2
                if (h - 1, temp_y) not in e:
                    # if that actions don't lead to collision with an egg, we will go for it
                    f_temp, i_temp, b_temp = change_bullets(f_temp, i_temp, b_temp)
                    heapq.heappush(A, Node(f_temp, temp_point, i_temp, e, b_temp, temp_y, temp_shoot, temp_path + [move]))'''

'''
    def dfs_visit(figure, invaders, eggs, bullets, ship_y, path, shoot, success_bullets):
        nonlocal best_value, best_way, best_bullet
        f, e = change_eggs(figure, eggs)

        if invaders == [] or check(f):
            if path == []:
                best_way = ['w']
            else:
                r = rate(f)
                if success_bullets > best_bullet:
                    best_value = r
                    best_way = path
                    best_bullet = success_bullets
        else:
            for move in ['w', 'a', 'd']:
                f_temp = copy.deepcopy(f)
                i_temp = copy.deepcopy(invaders)
                b_temp = copy.deepcopy(bullets)
                temp_point = success_bullets
                if move == 'a':
                    if ship_y - 1 == -1:
                        continue
                    temp_y = ship_y - 1
                    shoot = True
                elif move == 'd':
                    if ship_y + 1 == w:
                        continue
                    temp_y = ship_y + 1
                    shoot = True
                else:
                    temp_y = ship_y
                    if shoot:
                        f_temp[h - 2][ship_y] += 7
                        b_temp.append((h - 2, ship_y))
                        # test success of bullet
                        column = [f_temp[t][ship_y] for t in range(h)]
                        if column.count(1) >= column.count(7) + column.count(11):
                            temp_point = success_bullets + 2*(10 - len(path))
                        else:
                            temp_point = success_bullets - 10 + len(path)
                    shoot = not shoot

                f_temp[h-1][ship_y] -= 2
                f_temp[h-1][temp_y] += 2
                if (h-1, temp_y) not in e:
                    f_temp, i_temp, b_temp = change_bullets(f_temp, i_temp, b_temp)
                    dfs_visit(f_temp, i_temp, e, b_temp, temp_y, path + [move], shoot, temp_point)

    dfs_visit(figure, invaders_positions, eggs_positions, bullets_positions, ship_y, [], shoot, 0)
    print(best_way)
    print(best_bullet)
    return best_way[0]

'''

