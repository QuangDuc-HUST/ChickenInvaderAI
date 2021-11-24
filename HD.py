from Model import *

def ship_run(space:'Space'):
	"""
	given space.figure"""
	# available = []
	
	ship = space.spaceship
	ship_x, ship_y = ship.get_position()
	print(f'ship x, y = {ship_x},{ship_y}')
	fig = space.figure.copy()
	buls_x = [bul.get_position()[1] for bul in space.bullets ]
	print(f'bils_x = {buls_x}')
	# inv_num = len(space.invaders)
	# bul_num = len(space.bullets)
	def left_safe():
		if ship_y != 0: 
			if fig[ship_x-1, ship_y-1] not in [4, 7]:
				return True
		return False

	def right_safe():
		if ship_y != space.width -1: 
			if fig[ship_x-1, ship_y+1] not in [4, 7]:
				return True
		return False

	def middle_safe():
		return fig[ship_x-1, ship_y] not in [4, 7]

	def act(line:'str'=None):
		'''
		return action
		'''
		if middle_safe():
			print('middle safe')
			count = buls_x.count(ship_y)
			print(count)
			mid = 0
			print('fig[0, ship_y] = ', fig[0, ship_y])
			if fig[0, ship_y] == 1:
				mid += 1
			print('fig[1, ship_y] = ', fig[1, ship_y])

			if fig[1, ship_y] == 1:
				mid +=1
			print('mid = ', mid)
			if mid in [1,2] and count < mid:
				print('check available')
				if ship.available:
					print('ok')
					return 'w'

		if left_safe():
			print('left safe')
			# left = fig[0, ship_y-1]+ fig[1, ship_y-1]
			left = 0
			if fig[0, ship_y-1] == 1:
				left += 1
			if fig[1, ship_y-1] == 1:
				left +=1
			c_left = buls_x.count(ship_y - 1)
			if left in [1, 2] and c_left < left:
				print('go left')
				return 'a'
		if right_safe():
			print('right safe')
			# right = (fig[0, ship_y+1] + fig[1, ship_y+1])
			right = 0
			if fig[0, ship_y+1] == 1:
				right += 1
			if fig[1, ship_y+1] == 1:
				right +=1
			c_right = buls_x.count(ship_y + 1)
			if right in [1, 2] and c_right < right: 
				print('go right')
				return 'd'
		try:
			y = space.invaders[-1].get_position()[1]
		except:
			y = 0
		if left_safe():
			if right_safe():
				if y > ship_y:
					return 'd'
			elif y< ship_y:
				return 'a'
			return 'a'

		elif right_safe():
			return 'd'
		return 's'
	return act()

def left_safe(space: 'Space'):
	ship_x, ship_y = space.spaceship.get_position()
	fig = space.figure.copy()
	if ship_y != 0: 
		if fig[ship_x-1, ship_y-1] not in [4, 11]:
			return True
	return False

def right_safe(space: 'Space'):
	ship_x, ship_y = space.spaceship.get_position()
	fig = space.figure.copy()
	if ship_y != space.width -1: 
		if fig[ship_x-1, ship_y+1] not in [4, 11]:
			return True
	return False

def middle_safe(space: 'Space'):
	ship_x, ship_y = space.spaceship.get_position()
	fig = space.figure.copy()
	return fig[ship_x-1, ship_y] not in [4, 11]

def threaten(space:'Space'):
	ship_x, ship_y = space.spaceship.get_position()
	mid_thre = space.figure[ship_x -2, ship_y] in [4,11]
	if ship_y == 0 :
		left_thre = True
	else: 
		left_thre = space.figure[ship_x -2, ship_y-1] in [4,11]
	if ship_y == space.width -1 :
		right_thre = True
	else:
		right_thre =  space.figure[ship_x -2, ship_y+1] in [4,11]
	
	return mid_thre and left_thre and right_thre
	'''
	is a threaten occurs?
	'''


def copy_space(space:'Space'):
	child_space = Space(space.height, space.width)
	copy_fig = space.figure
	for i in range(len(space.figure)):
		for j in range(len(space.figure[0])):
			if copy_fig[i][j] == 1:
				_ = Invader(i,j, child_space)
			elif copy_fig[i][j] == 4:
				_ = Egg(i, j, child_space)
			elif copy_fig[i][j] == 11:
				_ = Bullet(i,j, child_space)
				_ = Egg(i, j, child_space)
			elif copy_fig[i][j] == 2:
				child_ship = SpaceShip(i,j,child_space)
				child_ship.available = space.spaceship.available
				
			elif copy_fig[i][j] == 7:
				_ = Bullet(i,j, child_space)
	return child_space, child_ship

def rel_bullets_invaders(space:'Space'):
	for bullet in space.bullets.copy():	
			bullet.move()

	for invader in space.invaders.copy():
		for bullet in space.bullets.copy():
			if bullet.collide(invader):
				space.bullets.remove(bullet)
				space.invaders.remove(invader)
				space.figure[bullet.x, bullet.y ] -=8

def ship_eggs_rel(space: 'Space'):
	for egg in space.eggs.copy():
			egg.drop()
		
	for egg in space.eggs.copy():
		if space.spaceship.collide(egg):
			print(f'collision occurs at x= {space.spaceship.x} , y ={space.spaceship.y}')
			return True
	return False

def nearest_invader(space:'Space'):
	loc = []
	for i in range(len(space.invaders)):
		loc.append(abs(space.spaceship.y - space.invaders[i].y))
	try:
		for i in range(len(space.bullets)):
			loc.pop(loc.index(abs(space.spaceship.y - space.bullets[i].y)))
	except:
		return -1
	if len(loc) == 0:
		return 0
	return min(loc)
def local_search(space:'Space'):
	'''
	return an action of ship with lowest cost 
	'''
	actions = ['w', 'a', 'd', 'remain']
	cost = {'w':2, 'a': 3, 'd': 3, 'remain': 1}
	current_fig = space.figure
	decision = None
	minimum_g = float('inf')
	for act in actions.copy():
		child_space, child_ship = copy_space(space)

		if act == 'w' and not child_ship.available:
			actions.remove(act)
			continue
		
		inline_inv = sum([1 for i in range(2) if child_space.figure[i][child_ship.y] == 1 ])
		inline_bul = sum([1 for bul in child_space.bullets if bul.y == child_ship.y])

		# print(inline_inv)
		if inline_inv - inline_bul == 0 and 'w' in actions:
			actions.remove('w')
			continue
			

		print(f'action: {act}')
		rel_bullets_invaders(child_space)
		child_ship.move(act)

		die = ship_eggs_rel(child_space)
		will_die = not right_safe(child_space) and not left_safe(child_space) and not middle_safe(child_space)
		if die or will_die:
			print('Die or will die ')
			actions.remove(act)
			continue
		# else:	
			#if die
		if threaten(child_space):
			print('FOUND A THREATEN!!!!!')
			if not bool(local_search(child_space)):
				print('This threaten will lead to death!!!')
				actions.remove(act)
				continue

		# print(f'left safe {left_safe(child_space)}')
		# print(f'Test child_space: go {act}')
		if act == 'w':
			nearest_inv = 0
		else:
			nearest_inv = nearest_invader(child_space)
		print(f"Nearest chicken: {nearest_inv}")
		f = 2* (len(child_space.invaders) - len(child_space.bullets)) + cost[act] + 3*(nearest_inv)
		if minimum_g > f:
			minimum_g = f
			decision = act
		# if act == 'w':
		# 	f -= 3 
		print(f'heuristic {f}')
		# child_space.show()

	print(f'possible actions : {actions}')
	# for pos_act in actions
	print(f'Optimal decision: {decision}')
	return decision