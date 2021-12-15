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
    game.initialize(height=9 , width= 7, num=14)

    # One time

    # online_play(game)
    # game.run(local_search)
    # game.run(getinput)
    # game.run(online)
    game.run(expectimax_getaction)
    # online_play(game)

    # __SAVE DATA__
    game.saveData('Test')

    # Evaluatate multiple time

    # eva = game.getEvaluate()

    # eva.evamultitime(local_search, times= 100)

    # eva.evamultitime(expectimax_getaction, times= 100)
    # eva.evamultitime(online, 25)
    # eva.saveGame('Testmulti1')



if __name__ == '__main__':
    main()
