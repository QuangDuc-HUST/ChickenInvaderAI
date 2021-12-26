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


def main():
    """
    You must declare GameModel with its initialization of height, width, number of chickens (9, 7, 14) before running any algorithms.

    If you just play 'human model' then use online_play(game).

    else:
        You choose one algorithm to run by game.run(algorithm), for instance:

        game.run(local_search) for local search algorithm
        game.run(greedy_bfs) for greedy best-first algorithm
        game.run(expectimax_getaction) for expectimax algorithm

        In case you want to visualize the result of the algorithm.
            Save data by game.saveData(filename) then ## Now it'll be the filename in data folder 
            then visualize_play(filename) 
    """

    # __INITIALIZE GAME__
    game = GameModel()
    game.initialize(height=9, width=7, num=14)

    # __PLAY GAME__
    # Human mode
    # online_play(game)

    # Auto mode
    game.run(local_search)
    # game.run(expectimax_getaction, maxdepth=3 , maxrandom=3)
    # game.run(greedy_bfs)

    # __SAVE DATA__
    game.saveData('Game1')

    # __VISUALIZATION__
    visualize_play('Game1')




    ############ This part for analysis
    # Evaluate multiple time
    # eva = game.getEvaluate()
    # eva.evamultitime(local_search, times= 50)
    # eva.evamultitime(expectimax_getaction, times= 5, maxdepth=3, maxrandom=3)
    # eva.evamultitime(a_star_search, 25)
    # eva.saveGame('Testmulti')
    #############

if __name__ == '__main__':
    main()
