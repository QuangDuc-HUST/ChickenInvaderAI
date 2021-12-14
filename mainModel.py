from player_mode import online_play
from Model import GameModel
from LL import online  # Sourcecode: LL
from HD import local_search  # Sourcecode: HD
from QD import expectimax_getaction

# Just be normal game, input
def getinput(space):
    return input('Your next move is: ')


def main():
    game = GameModel()
    game.initialize(height=9, width=7, num=14)

    # One time

    # game.run(local_search)
    game.run(online)
    # game.run(getinput)
    # game.run(expectimax_getaction)
    # online_play(game)
    # game.run(testinputOffline)
    # game.run(testAsearch)
    # game.run(miniMax)

        
    # print(game.getStatesStatistic())
    # print(game.getActionsStatistic())


    # __SAVE DATA__
    # game.saveData('Test1')

    # Evaluatate multiple time

    # eva = game.getEvaluate()

    # eva.evamultitime(local_search, times= 25)

    # eva.evamultitime(online, 25)
    # eva.saveGame('Testmulti')



if __name__ == '__main__':
    main()
