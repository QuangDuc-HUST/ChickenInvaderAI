#
#
#main.py : running game
#
#
from visualization import online_play, visualize_play
from Model import GameModel
from algorithms.LL import greedy_bfs  # Sourcecode: LL
from algorithms.HD import greedy_search  # Sourcecode: HD
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
    # game.run(greedy_search)
    # game.run(expectimax_getaction)
    #game.run(a_star_search)
    # __SAVE DATA__
    # game.saveData('Test')

    ## Evaluatate multiple time
    eva = game.getEvaluate()

    #eva.evamultitime(greedy_search, times= 50)
    # eva.evamultitime(expectimax_getaction, times= 5)
    eva.evamultitime(greedy_bfs, 25)

    #eva.saveGame('Test')

    # eva.saveGame('Testmulti1')
    # visualize_play('Test')

if __name__ == '__main__':
    main()
