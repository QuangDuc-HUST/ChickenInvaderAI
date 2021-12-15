from visualization import online_play, visualize_play
from Model import GameModel
from algorithms.LL import online  # Sourcecode: LL
from algorithms.HD import local_search  # Sourcecode: HD
from algorithms.QD import expectimax_getaction
# from argparse import ArgumentParser


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

    ## Evaluatate multiple time
    # eva = game.getEvaluate()

    # eva.evamultitime(local_search, times= 100)
    # eva.evamultitime(expectimax_getaction, times= 100)
    # eva.evamultitime(online, 25)

    # eva.saveGame('Testmulti1')


if __name__ == '__main__':
    main()
