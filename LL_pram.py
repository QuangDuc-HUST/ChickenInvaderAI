def search(space):
    # because the eggs is spawned randomly, we only can search for what will happen in the next few steps
    # the method will search all strategies until all the current eggs in the space disappear
    import copy
    # environment changing function
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
    # function that check if we reach the leaf of searching tree

    def check(f):
        for i in range(len(f)):
            for j in range(len(f[i])):
                if f[i][j] in [4, 11]:
                    return False
        return True

    '''def rate(f):
        completeness = 0
        no_of_alive_invaders = 0
        for j in range(w):
            bullets = 0
            invaders = 0
            for i in range(h):
                if f[i][j] == 1:
                    invaders +=1
                    no_of_alive_invaders += 1
                if f[i][j] in [7, 11]:
                    bullets += 1
            completeness += min([invaders, bullets])
        return completeness + 14 - no_of_alive_invaders'''
    # some variables of the environment
    figure = list([list(i) for i in space.figure])
    invaders_positions = [(i.x, i.y) for i in space.invaders]
    eggs_positions = [(i.x, i.y) for i in space.eggs]
    bullets_positions = [(i.x, i.y) for i in space.bullets]
    ship_x, ship_y = space.spaceship.x, space.spaceship.y
    w, h = space.width, space.height
    # best_bullet variable that use to rate the efficiency of a solution
    best_bullet = -99999
    # and the solution
    best_way = []
    # check whether the ship shoot before
    # if it just fired, we can't should right now, we have to wait until the next step to fire
    if figure[ship_x - 3][ship_y] in [7, 11]:
        shoot = False
    else:
        shoot = True
    # dfs

    def dfs_visit(figure, invaders, eggs, bullets, ship_y, path, can_shoot, success_bullets):
        nonlocal best_way, best_bullet
        # because when we get the information about the environment, its bullets and invaders were changed,
        # we do the rest which is egg dropping
        f, e = change_eggs(figure, eggs)
        # check if we reach the leaf then use the heuristic point to rate
        if invaders == [] or check(f):
            # this use to deal at the beginning of the game when we can't search for anything yet
            # since there are no eggs
            if path == []:
                best_way = ['w']
            else:
                if success_bullets > best_bullet:
                    best_way = path
                    best_bullet = success_bullets
        # each step we have 3 possible actions, so we will use dfs for them
        else:
            for move in ['w', 'a', 'd']:
                # making copies to avoid collision with other searching branches
                f_temp = copy.deepcopy(f)
                i_temp = copy.deepcopy(invaders)
                b_temp = copy.deepcopy(bullets)
                temp_point = success_bullets
                # move left
                if move == 'a':
                    # check if we can move to the left
                    if ship_y - 1 == -1:
                        continue
                    # move if we can
                    # position of the ship
                    temp_y = ship_y - 1
                    can_shoot = True
                elif move == 'd':
                    # check if we can move to the right
                    if ship_y + 1 == w:
                        continue
                    # move if we can
                    # position of the ship
                    temp_y = ship_y + 1
                    can_shoot = True
                else:
                    # shoot
                    temp_y = ship_y
                    if can_shoot:
                        f_temp[h - 2][ship_y] += 7
                        b_temp.append((h - 2, ship_y))
                        # success of bullet
                        # a bullet is considered to be a good one is the bullet that will kill a invaders in the future
                        # if it is a efficient action, it will get points depends on the time that the bullet is shot
                        # the sooner it is shot, the larger points
                        # otherwise, it will loose points in the same way
                        column = [f_temp[t][ship_y] for t in range(h)]
                        if column.count(1) >= column.count(7) + column.count(11):
                            temp_point = success_bullets + 2*(10 - len(path))
                        else:
                            temp_point = success_bullets - 10 + len(path)
                    # change variable to make sure it cant shoot in the next step ( like the environment )
                    can_shoot = not can_shoot
                # move the ship in the grid
                f_temp[h-1][ship_y] -= 2
                f_temp[h-1][temp_y] += 2
                if (h-1, temp_y) not in e:
                    # if that actions don't lead to collision with an egg, we will go for it
                    f_temp, i_temp, b_temp = change_bullets(f_temp, i_temp, b_temp)
                    dfs_visit(f_temp, i_temp, e, b_temp, temp_y, path + [move], can_shoot, temp_point)
    # call dfs from the root
    dfs_visit(figure, invaders_positions, eggs_positions, bullets_positions, ship_y, [], shoot, 0)
    # return the first move of the best path
    return best_way[0]
