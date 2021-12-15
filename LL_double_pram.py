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
    # rating function

    def move_rating(f1, previous_move, move):
        invaders_columns = []
        for i in range(w):
            col = [f1[k][i] for k in range(h)]
            if col.count(1) > col.count(7) + col.count(11):
                invaders_columns.append(i)
        try:
            return min([abs(move - k) for k in invaders_columns]) <= min([abs(previous_move - k) for k in
                                                                          invaders_columns])
        except ValueError:
            return False

    # checking if we reach the leaf of tree function

    def check(f1):
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
    # if it just fired, we can't should right now, we have to wait until the next step to fire
    if figure[ship_x - 3][ship_y] in [7, 11]:
        previous_state = ['w']
    else:
        previous_state = ['a or d']
    # creat list for heap using
    A = []
    # push the current states to the heap
    heapq.heappush(A, Node(figure, 0, invaders_positions, eggs_positions, bullets_positions, ship_y, previous_state))
    # the heap will keep track of the state that has the highest heuristic
    while True:
        # pop the best state
        map = heapq.heappop(A)
        # because when we get the information about the environment, its bullets and invaders were changed,
        # we do the rest which is egg dropping
        f, e = change_eggs(map.f, map.e)
        # check if we reach the leaf
        if check(f):
            if len(map.m) == 1:
                return 'd'
            else:
                print(map.m)
                return map.m[1]
        else:
            # if we shot in the previous turn, this turn we should not shoot cuz it makes no senses
            if map.m[-1] == 'w':
                possible_moves = ['a', 'd']
            else:
                possible_moves = ['w', 'a', 'd']
            for move in possible_moves:
                # make copies
                f_temp = copy.deepcopy(f)
                i_temp = copy.deepcopy(map.i)
                b_temp = copy.deepcopy(map.b)
                temp_point = map.h
                temp_path = map.m
                if move == 'a':
                    if map.ship_y - 1 == -1:
                        continue
                    temp_y = map.ship_y - 1
                    # temp_point += move_rating(f_temp, map.ship_y, temp_y)
                elif move == 'd':
                    if map.ship_y + 1 == w:
                        continue
                    temp_y = map.ship_y + 1
                    # temp_point += move_rating(f_temp, map.ship_y, temp_y)
                else:
                    temp_y = map.ship_y
                    f_temp[h - 2][map.ship_y] += 7
                    b_temp.append((h - 2, map.ship_y))
                    # success of bullet
                    # a bullet is considered to be a good one is the bullet that will kill a invaders in the future
                    # if it is a efficient action, it will get points depends on the time that the bullet is shot
                    # the sooner it is shot, the larger the points
                    # otherwise, it will loose points in the same way
                    column = [f_temp[t][map.ship_y] for t in range(h)]
                    if column.count(1) >= column.count(7) + column.count(11):
                        temp_point += 2 * (10 - len(map.m))
                    else:
                        temp_point -= 10 - len(map.m)
                    # change variable to make sure it cant shoot in the next step ( like the environment )
                # move the ship in the grid
                f_temp[h - 1][map.ship_y] -= 2
                f_temp[h - 1][temp_y] += 2
                # if our move in this turn is better than that of the last one, which mean the ship move closer to the
                # columns that contain invaders, it will get bonus points due to the appearance time.
                if move_rating(f, map.ship_y, temp_y):
                    temp_point += 10 - len(map.m)
                if (h - 1, temp_y) not in e:
                    # if that actions don't lead to collision with an egg, we will go for it
                    f_temp, i_temp, b_temp = change_bullets(f_temp, i_temp, b_temp)
                    heapq.heappush(A, Node(f_temp, temp_point, i_temp, e, b_temp, temp_y, temp_path + [move]))