def exp_search(space):
	import read_space
	figure, invaders_positions, eggs_positions, bullets_positions, ship_y, w, h = read_space.input_reader(space)

	def check(f1):
		for i in range(len(f1)):
			for j in range(len(f1[i])):
				if f1[i][j] in [4, 11]:
					return False
		return True

	def check_phase(figure, ship_y):
		left_most_column = [figure[i][0] for i in range(h)]
		right_most_column = [figure[i][-1] for i in range(h)]
		l = left_most_column.count(1)
		r = right_most_column.count(1)
		if l > r:
			return False
		elif l < r:
			return True
		else:
			# corner
			if ship_y == 0:
				return True
			elif ship_y == w - 1:
				return False

	def safe_position(figure, ship_y):
		nearest_row = 2
		for i in range(h-2, -1, -1):
			if 4 in figure[i] or 11 in figure[i]:
				nearest_row = i
				break
		return min([abs(ship_y - i) for i in range(w) if figure[nearest_row][i] in [4, 11]]) < h - 1 - nearest_row

	phase = check_phase(figure, ship_y)
	if check(figure):
		return 'd'
	else:
		pass
