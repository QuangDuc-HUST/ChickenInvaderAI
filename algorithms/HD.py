#
#
# Source code: Local Search Algorithm	
#
#
import copy

def greedy_search(space) -> (str):
	"""
	return a direction w/a/d/remain which has minimum heuristic value
	"""
	pos_actions = possible_acitons(space)
	return pos_actions[0][0]


def possible_acitons(space) -> (list):
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

def heuristic(space, act:'str') :
	'''
	return heuristic value of action act
	'''
	fig = (space.figure)
	_, ship_y = space.spaceship.get_position()
	cost = {'w' :0, 'a': 3, 'd':3, 'remain': 2}
	alive_chicken = [max(list(fig[:,i]).count(1) - list(fig[:,i]).count(11) - list(fig[:,i]).count(7), 0) for i in range((space.width)) ]
	if (list(fig[:,ship_y]).count(1) == list(fig[:,ship_y]).count(11)+ list(fig[:,ship_y]).count(7)) and act == 'w':     # check whether action 'w' of ship can kill an invader
		nearest_invader = 0 
	else:
		try:     # try except for case list of alive chicken all 0
			nearest_invader = min([abs(ship_y - i) for i in range(space.width) if alive_chicken[i] != 0 ])
		except:
			nearest_invader = 0

	h = 2 * sum(alive_chicken) + 3 * nearest_invader
	g = cost[act]
	return h+ g, nearest_invader


def nearest_zero(space, i:int) -> (int):
	"""
	find nearest hole which ship can stay there to avoid egg after i steps
	return an int"""
	fig = space.figure
	ship_x, ship_y = space.spaceship.get_position()
	row_raw = fig[ship_x - i ][:]
	row = [1 if row_raw[j] in [4,11] else 0 for j in range(len(row_raw))]
	# print(row)
	ret = min([abs(ship_y - k) for k in range(len(row)) if row[k] == 0 ])
	# print(f'nearest 0 of {i} row above is {ret}')
	return ret

def dangerous_state(space) -> (bool):
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
