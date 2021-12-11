from Model import GameModel
from LL import online  # Sourcecode: LL
from HD import local_search  # Sourcecode: HD
from QD import miniMax, testinputOffline  # Sourcecode: QD
import pickle

# Just be normal game, input
def getinput(space):
    return input('Your next move is: ')


def savedata(game, filename):
    with open(filename, 'wb') as f:
        pickle.dump(game.getStatesStatistic(), f)


def main():
    game = GameModel()
    game.initialize(height=10, width=7, num=14)

    # One time

    # game.run(online, isOnline=True)
    # game.run(getinput,isOnline=True)
    game.run(local_search, isOnline=True)

    # game.run(testinputOffline, isOnline=False)
    # game.run(miniMax, isOnline=False)

    # print(game.getActionsStatistic())
    # print(len(game.getActionsStatistic()))

    # Evaluatate multiple time

    # eva = game.getEvaluate()
    # eva.evamultitime(local_search, True, 10)
    # eva.evamultitime(online, True, 10)

    # __SAVE DATA__
    savedata(game, 'data')
	# eva = game.getEvaluate()
	# eva.evamultitime(local_search, True, 100)
	# eva.evamultitime(online, True, 10)

if __name__ == '__main__':
    main()
