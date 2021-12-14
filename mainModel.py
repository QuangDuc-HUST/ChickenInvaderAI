from visualize_mode import display
from Model import GameModel
from LL import online  # Sourcecode: LL
from HD import local_search  # Sourcecode: HD
from QD import miniMax, testAsearch  # Sourcecode: QD


# Just be normal game, input
def getinput(space):
    return input('Your next move is: ')


def main():
    game = GameModel()
    game.initialize(height=9, width=7, num=14)

    # One time

    # game.run(local_search)

    # game.run(online)
    # game.run(getinput)

    # print(game.getStatesStatistic())
    # print(game.getActionsStatistic())

    # game.run(testinputOffline)
    # game.run(testAsearch)
    # game.run(miniMax)

    # print(game.getActionsStatistic())
    # print(len(game.getActionsStatistic()))

    # __SAVE DATA__
    # game.saveData('Test1')
    # display(game.getStatesStatistic())

    # Evaluatate multiple time

    eva = game.getEvaluate()

    eva.evamultitime(local_search, times=25)

    # eva.evamultitime(online, 25)
    # eva.saveGame('Testmulti')


if __name__ == '__main__':
    main()
