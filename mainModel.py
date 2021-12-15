from Model import GameModel
from LL_double_pram import search ## Sourcecode: LL
from HD import local_search ## Sourcecode: HD

## Just be normal game, input
def getinput(space):
	return input('Your next move is: ')


def main():
	game = GameModel()
	
	game.initialize(height=10, width=7, num=14)

	## One time
	game.run(search,isOnline=True)
	# game.run(getinput,isOnline=True)
	# game.run(local_search, isOnline=True)
	
	# print(game.getActionsStatistic())
	# print(len(game.getActionsStatistic()))

	##  Evaluatate multiple time
	'''eva = game.getEvaluate()

	eva.evamultitime(local_search, True, 10)
	eva.evamultitime(online, True, 10)'''



if __name__ == '__main__':
	main()