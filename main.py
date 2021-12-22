#
#
# main.py : running game
#
#
from Model import GameModel
from visualization import online_play, visualize_play
from algorithms.LL import greedy_bfs  
from algorithms.HD import local_search  
from algorithms.QD import expectimax_getaction


def getinput(space):
    """
    Normal game where gets input from the keyboard
    """

    return input('Your next move is: ')


def main():
    """
    You must declare GameModel with its initialization of  height, width, number of chickens (9, 7, 14)

    If you just play 'human model' then use online_play(game) with game: GameModel

    else:
        You choose one algorithm to run by game.run(algorithm)
        If you want to visualize the result of the algorithm. Save data by game.saveData(filename) then
        visualize_play(filename)
    """

    # Initialize Game
    game = GameModel()
    game.initialize(height=9, width=7, num=14)

    # PLAY GAME
    ## Human mode
    # online_play(game)
    # game.run(getinput)

    # Auto mode
    # game.run(local_search)
    # game.run(expectimax_getaction, maxdepth=3 , maxrandom=3)
    game.run(greedy_bfs)

    # __SAVE DATA__
    game.saveData('Test')

    # __VISUALIZATION__
    visualize_play('Test')




    ####
    # Evaluate multiple time
    # eva = game.getEvaluate()
    # eva.evamultitime(local_search, times= 50)
    # eva.evamultitime(expectimax_getaction, times= 5, maxdepth=3, maxrandom=3)
    # eva.evamultitime(a_star_search, 25)
    # eva.saveGame('Testmulti')


if __name__ == '__main__':
    main()
