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

    ## Initialize Game 
    game = GameModel()
    game.initialize(height=9, width=7, num=14)


    # PLAY GAME
    ## Human mode
    # online_play(game)

    ## Auto mode
    # game.run(local_search)
    # game.run(getinput)
    game.run(a_star_search)
    # game.run(expectimax_getaction, maxdepth=3, maxrandom=3)

    ### SAVE and VISUALIZATION
    FILENAME = 'Test'

    # __SAVE DATA__
    game.saveData(FILENAME)

    # __VISUALIZATION___
    visualize_play(FILENAME)

    ## Evaluatate multiple time
    # eva = game.getEvaluate()

    # eva.evamultitime(local_search, times= 25)
    # eva.evamultitime(expectimax_getaction, times= 5, maxdepth = 3, maxrandom = 4)
    # eva.evamultitime(a_star_search, 5)

    # eva.saveGame('Testmulti1')
    

if __name__ == '__main__':
    main()
