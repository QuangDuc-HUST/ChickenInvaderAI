from Model import GameModel
from LL import online ## Sourcecode: LL
from HD import local_search ## Sourcecode: HD
from QD import miniMax, testinputOffline  ## Sourcecode: QD

## Just be normal game, input
def getinput(space):
	return input('Your next move is: ')


def main():
	game = GameModel()
	
	game.initialize(height=10, width=7, num=14)

	## One time

	# game.run(online,isOnline=True)
	# game.run(getinput,isOnline=True)
	# game.run(local_search, isOnline=True)
	

	game.run(testinputOffline, isOnline=False)
	# game.run(miniMax, isOnline=False)

	# print(game.getActionsStatistic())
	# print(len(game.getActionsStatistic()))

	##  Evaluatate multiple time

	# eva = game.getEvaluate()
	# eva.evamultitime(local_search, True, 10)
	# eva.evamultitime(online, True, 10)



if __name__ == '__main__':
	main()