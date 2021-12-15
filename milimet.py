import sys


def evaluation(state):
	pass


children_for_max = []
children_for_min = []


def minimax(current_state, depth, children, alpha, beta, maximize):
	if depth == 0:
		return evaluation(current_state)

	if maximize:
		max_value = -sys.maxsize
		for child in children:
			temp = minimax(child, depth - 1, children_for_min, alpha, beta, False)
			max_value = max(temp, max_value)
			alpha = max(alpha, temp)
			if alpha >= temp:
				break
		return max_value

	else:
		min_value = sys.maxsize
		for child in children:
			temp = minimax(child, depth - 1, children_for_max, alpha, beta, True)
			min_value = min(temp, min_value)
			beta = min(beta, temp)
			if alpha >= beta:
				break
		return min_value
