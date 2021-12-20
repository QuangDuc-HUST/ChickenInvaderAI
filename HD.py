import copy
import numpy as np
from Model import *


# def left_safe(space: 'Space'):
# 	ship_x, ship_y = space.spaceship.get_position()
# 	fig = space.figure.copy()
# 	if ship_y != 0: 
# 		if fig[ship_x-1, ship_y-1] not in [4, 11]:
# 			return True
# 	return False

# def right_safe(space: 'Space'):
# 	ship_x, ship_y = space.spaceship.get_position()
# 	fig = space.figure.copy()
# 	if ship_y != space.width -1: 
# 		if fig[ship_x-1, ship_y+1] not in [4, 11]:
# 			return True
# 	return False

# def middle_safe(space: 'Space'):
# 	ship_x, ship_y = space.spaceship.get_position()
# 	fig = space.figure.copy()
# 	return fig[ship_x-1, ship_y] not in [4, 11]

# def threaten(space:'Space'):
# 	ship_x, ship_y = space.spaceship.get_position()
# 	mid_thre = space.figure[ship_x -2, ship_y] in [4,11]
# 	if ship_y == 0 :
# 		left_thre = True
# 	else: 
# 		left_thre = space.figure[ship_x -2, ship_y-1] in [4,11]
# 	if ship_y == space.width -1 :
# 		right_thre = True
# 	else:
# 		right_thre =  space.figure[ship_x -2, ship_y+1] in [4,11]
	
# 	return mid_thre and left_thre and right_thre
# 	'''
# 	is a threaten occurs?
# 	'''


# def copy_space(space:'Space'):
# 	child_space = Space(space.height, space.width)
# 	copy_fig = space.figure
# 	for i in range(len(space.figure)):
# 		for j in range(len(space.figure[0])):
# 			if copy_fig[i][j] == 1:
# 				_ = Invader(i,j, child_space)
# 			elif copy_fig[i][j] == 4:
# 				_ = Egg(i, j, child_space)
# 			elif copy_fig[i][j] == 11:
# 				_ = Bullet(i,j, child_space)
# 				_ = Egg(i, j, child_space)
# 			elif copy_fig[i][j] == 2:
# 				child_ship = SpaceShip(i,j,child_space)
# 				child_ship.available = space.spaceship.available
				
# 			elif copy_fig[i][j] == 7:
# 				_ = Bullet(i,j, child_space)
# 	return child_space, child_ship

# def rel_bullets_invaders(space:'Space'):
# 	for bullet in space.bullets.copy():	
# 			bullet.move()

# 	for invader in space.invaders.copy():
# 		for bullet in space.bullets.copy():
# 			if bullet.collide(invader):
# 				space.bullets.remove(bullet)
# 				space.invaders.remove(invader)
# 				space.figure[bullet.x, bullet.y ] -=8

# def ship_eggs_rel(space: 'Space'):
# 	for egg in space.eggs.copy():
# 			egg.drop()
		
# 	for egg in space.eggs.copy():
# 		if space.spaceship.collide(egg):
# 			print(f'collision occurs at x= {space.spaceship.x} , y ={space.spaceship.y}')
# 			return True
# 	return False

# def nearest_invader(space:'Space'):
# 	loc = []
# 	for i in range(len(space.invaders)):
# 		loc.append(abs(space.spaceship.y - space.invaders[i].y))
# 	try:
# 		for i in range(len(space.bullets)):
# 			loc.pop(loc.index(abs(space.spaceship.y - space.bullets[i].y)))
# 	except:
# 		return -1
# 	if len(loc) == 0:
# 		return 0
# 	return min(loc)
# def local_search(space:'Space'):
	# '''
	# return an action of ship with lowest cost 
	# '''
	# actions = ['w', 'a', 'd', 'remain']
	# cost = {'w':3, 'a': 2, 'd': 2, 'remain': 1}
	# current_fig = space.figure
	# decision = None
	# minimum_g = float('inf')
	# for act in actions.copy():
	# 	child_space, child_ship = copy_space(space)

	# 	if act == 'w' and not child_ship.available:
	# 		actions.remove(act)
	# 		continue
		
	# 	inline_inv = sum([1 for i in range(2) if child_space.figure[i][child_ship.y] == 1 ])
	# 	inline_bul = sum([1 for bul in child_space.bullets if bul.y == child_ship.y])

	# 	# print(inline_inv)
	# 	if inline_inv - inline_bul == 0 and 'w' in actions:
	# 		actions.remove('w')
	# 		continue
			

	# 	print(f'action: {act}')
	# 	rel_bullets_invaders(child_space)
	# 	child_ship.move(act)

	# 	die = ship_eggs_rel(child_space)
	# 	will_die = not right_safe(child_space) and not left_safe(child_space) and not middle_safe(child_space)
	# 	if die or will_die:
	# 		print('Die or will die ')
	# 		actions.remove(act)
	# 		continue
	# 	# else:	
	# 		#if die
	# 	if threaten(child_space):
	# 		print('FOUND A THREATEN!!!!!')
	# 		if not bool(local_search(child_space)):
	# 			print('This threaten will lead to death!!!')
	# 			actions.remove(act)
	# 			continue

	# 	# print(f'left safe {left_safe(child_space)}')
	# 	# print(f'Test child_space: go {act}')
	# 	if act == 'w':
	# 		nearest_inv = 0
	# 	else:
	# 		nearest_inv = nearest_invader(child_space)
	# 	print(f"Nearest chicken: {nearest_inv}")
	# 	f = 3* (len(child_space.invaders) - len(child_space.bullets)) + cost[act] + 2*(nearest_inv)
	# 	if minimum_g > f:
	# 		minimum_g = f
	# 		decision = act
	# 	# if act == 'w':
	# 	# 	f -= 3 
	# 	print(f'heuristic {f}')
	# 	# child_space.show()

	# print(f'possible actions : {actions}')
	# # for pos_act in actions
	# print(f'Optimal decision: {decision}')
	# return decision

def greedy_search(space:'Space') -> (str):
	"""
	return a direction w/a/d/remain which has minimum heuristic value
	"""
	pos_actions = possible_acitons(space)
	return pos_actions[0][0]


def possible_acitons(space:'Space') -> (list):
	"""
	return list of possible actions sorted by heuristic function
	"""
	pos_actions = []
	actions = ['w', 'remain','a','d']
	print(space.spaceship.available)
	for act in actions:
		new_space = copy.deepcopy(space)
		print(f'action: {act}')
		if (not new_space.spaceship.available) and act == 'w':
			continue
		new_space.update_bullet()
		new_space.spaceship.move(act)
		new_space.update_egg()
		losing = new_space.check_losing()
		is_losing = dangerous_state(new_space)
		if losing or is_losing:
			continue
		else:
			pos_actions.append((act,heuristic(new_space, act)))
	pos_actions.sort(key=(lambda x:(x[1][0], x[1][1]) ))
	return pos_actions

def heuristic(space:'Space', act:'str') :
	'''
	return heuristic value of action act
	'''
	fig = (space.figure)
	_, ship_y = space.spaceship.get_position()
	cost = {'w' :0, 'a': 3, 'd':3, 'remain': 2}
	alive_chicken = [max(list(fig[:,i]).count(1) - list(fig[:,i]).count(11) - list(fig[:,i]).count(7), 0) for i in range((space.width)) ]
	if (fig[0,ship_y] == 1) and act == 'w':
		nearest_invader = 0 
	else:
		try:
			nearest_invader = min([abs(ship_y - i) for i in range(space.width) if alive_chicken[i] != 0 ])
		except:
			nearest_invader = 0
	# print(f'nearest invaders = {nearest_invader}')
	h = 2 * sum(alive_chicken) + 3 * nearest_invader
	g = cost[act]
	return h+ g, nearest_invader

# def nearest_zero(fig:'np.array', i:int, ship_x, ship_y) -> (int):
def nearest_zero(space:'Space', i:int) -> (int):
	"""
	find nearest hole which ship can stay there to avoid egg after i steps
	return an int"""
	fig = space.figure
	ship_x, ship_y = space.spaceship.get_position()
	# print(ship_x, ship_y)
	# ship_x = space.height - 1
	row_raw = fig[ship_x - i ][:]
	row = [1 if row_raw[j] in [4,11] else 0 for j in range(len(row_raw))]
	# print(row)
	ret = min([abs(ship_y - k) for k in range(len(row)) if row[k] == 0 ])
	# print(f'nearest 0 of {i} row above is {ret}')
	return ret

def dangerous_state(space:'Space') -> (bool):
	"""
	return True if the current state is dangerous for ship
	False otherwise.
	(can check in any case including chicken lay more than 3 eggs at a specific step)
	"""
	max_egg = 3
	for i in range(1,max_egg):
		if nearest_zero(space, i) > i:
			return True
	return False

if __name__ == '__main__':
	fig = np.array([[1, 1, 1, 1, 1, 1, 1],
					[1, 1, 1, 1, 1, 1, 1],
					[0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 4, 0],
					[0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0],
					[0, 0, 4, 7, 4, 4, 0],
					[0, 0, 0, 2, 0, 0, 0]])
	space = Space(9,7)
	space.initialize(14)
	for i in range(30):
		space.update_bullet()
		a = input()
		space.spaceship.move(greedy_search(space))
		space.update_egg()
		space.step +=1
		# space.update_egg()

		space.invader_actions()
		space.show()	
		print(possible_acitons(space))
