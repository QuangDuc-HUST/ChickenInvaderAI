def input_reader(space):
	figure = list([list(i) for i in space.figure])
	invaders_positions = [(i.x, i.y) for i in space.invaders]
	eggs_positions = [(i.x, i.y) for i in space.eggs]
	bullets_positions = [(i.x, i.y) for i in space.bullets]
	ship_x, ship_y = space.spaceship.x, space.spaceship.y
	w, h = space.width, space.height
	return figure, invaders_positions, eggs_positions, bullets_positions, ship_y, w, h


def change_eggs(figure, eggs):
	next_egg = []
	for x, y in eggs:
		figure[x][y] -= 4
		if x + 1 < len(figure):
			figure[x + 1][y] += 4
			next_egg.append((x + 1, y))
	return figure, next_egg


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


def check(f):
	for i in range(len(f)):
		for j in range(len(f[i])):
			if f[i][j] in [4, 11]:
				return False
	return True
