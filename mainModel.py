from Model import GameModel
from LL import simple_move ## Sourcecode: LL
from HD import local_search ## Sourcecode: HD

## Just be normal game, input
def getinput(space):
	return input('Your next move is: ')


def main():
	game = GameModel()
	
	game.initialize(height=10, width=7, num=14)

	game.run(simple_move,isOnline=True)

	# game.run(getinput,isOnline=True)

	# game.run(local_search, isOnline=True)





if __name__ == '__main__':
	main()