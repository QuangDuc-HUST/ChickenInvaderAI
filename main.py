#
#
#main.py : running game
#
#
from visualization import online_play, visualize_play
from Model import GameModel
from algorithms.LL import a_star_search  # Sourcecode: LL
from algorithms.HD import local_search  # Sourcecode: HD
from algorithms.QD import expectimax_getaction


def getinput(space):
    '''
    Normal game where gets input from the keyboard.
    '''
    return input('Your next move is: ')


def main():
    '''
    You must declare GameModel with its initilization of  height, width, number of chickens (9, 7, 14)

    If you just play 'human model' then use online_play(game) with game: GameModel

    else:
        You choose one algorithm to run by game.run(algorithm)
        If you want to visualize the result of the algorthm. Save data by game.saveData(filename) then visualize_play(filename)
    '''

    ## Initilize game 
    game = GameModel()
    game.initialize(height=9, width=7, num=14)


    # Play game
    ## Human mode
    # online_play(game)

    ## Auto mode
    # game.run(local_search)
    # game.run(getinput)
    game.run(a_star_search)
    # game.run(expectimax_getaction)

    # __SAVE DATA__
    game.saveData('Test')

    ## Evaluatate multiple time
    # eva = game.getEvaluate()

    # eva.evamultitime(local_search, times= 100)
    # eva.evamultitime(expectimax_getaction, times= 100)
    # eva.evamultitime(a_star_search, 25)

    # eva.saveGame('Testmulti1')
    visualize_play('Test')

if __name__ == '__main__':
    main()
