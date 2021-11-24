def simple_move(space):

    def can_move_left():
        nonlocal space
        return space.spaceship.y - 1 >= 0 and space.figure[space.spaceship.x, space.spaceship.y - 1] != 4

    def can_move_right():
        nonlocal space
        return space.spaceship.y + 1 < space.width and space.figure[space.spaceship.x, space.spaceship.y + 1] != 4

    def dodge():
        nonlocal space
        if can_move_right():
            return 'd'
        if can_move_left():
            return 'a'

    def need_to_dodge():
        nonlocal space
        return space.figure[space.spaceship.x, space.spaceship.y] in [4, 6, 11]

    # find the nearest invaders
    def best_value(lst,val):
        best = 0
        for i in range(len(lst)):
            if abs(lst[i] - val) <= abs(lst[best] - val):
                best = i
        return lst[best]
    # check if we need to dodge
    if need_to_dodge():
        return dodge()

    # otherwise we can perform some slightly tactic moves
    else:
        bullets_col = [i.y for i in space.bullets]
        invaders_col = [i.y for i in space.invaders]
        nearest = best_value(invaders_col, space.spaceship.y)
        # check wether there are enough bullets that are on the way to kill the invaders
        while bullets_col.count(nearest) >= invaders_col.count(nearest):
            invaders_col = [i for i in invaders_col if i != nearest]
            # if all invaders are going to die, we just stay or dodge if work calls for it
            # until all the invaders are deadddddddd
            if invaders_col == []:
                return dodge() if need_to_dodge() else 'remain'
            # else we will try to find the next nearest invaders to execute
            nearest = best_value(invaders_col, space.spaceship.y)

        if nearest > space.spaceship.y and can_move_right():
            return 'd'
        if nearest < space.spaceship.y and can_move_left():
            return 'a'
        else:
            return 'w'
