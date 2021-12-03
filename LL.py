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







