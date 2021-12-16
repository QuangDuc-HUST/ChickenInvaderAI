Chicken Invader Project -  Artificial Intellegence 2021
=========

<p align="center">
  <img src="https://i.ibb.co/z7dFmf2/Intro-1.png" />
</p>


Overview
---------
An easier version of Chicken Invader game implemented in python 3 including simple GUI for visualization and enjoyment.


Our game repository has three main parts:
- Model: including the heart of the game (environments, agents) and evaluation system.
- Algorithms: guild of the agent (spaceship) to reach the goal.
- Visualization: GUI of the game.

Now we go to in the details.

Model 
----
Related files : `Model.py`.

The full backend of this Chicken Invader game, you can start with GUI or without GUI.

There are three sections in this part:
1.  Environment: Including spaceship agent, invaders (chickens), the space, eggs, bullets and actions of each object. 

2.  Model: Including the logic, the procedure of the game (such as the order of action's agents).

3.  Evaluation system: Evaluate the efficiency and effectiveness of each proposed algorithm.


Algorithms
-----
Related folder: `algorithms`\
We use two AI algorithms: 

1.  Local search for agent.
2.  Expectimax for agent.

Visualization
-----
Related files: `visualization.py`.

There are two modes of the GUI in this game:

1.  Human mode : Get input from the keyboard in each turn of the spaceship.

2.  Auto mode: The input is the series of actions of one of those above algorithms.

Note: in each mode, we also have 'play back' mode so as to watch what happened.

Usage:
------
### Installation
Dependences:  `requirements.txt`. Go to the main folder then type
```
python -m pip install -r requirements.txt
```
In here, we use two more additional packages `numpy` and `pygame`.

### Start a game
See usage on `main.py`

### Examples:
```
main.py


# Declare the game model
game = GameModel()
# Initilize the game with height = 9, width = 7, num of chicken = 14
game.initialize(height=9 , width= 7, num=14)
# Choose the algorithm to perform (E.g local search)
game.run(local_search)
```


Game rule
-------
Information in the report.


Other files and folders
-----
- `main.py` file: the full environment to play the game (control room).
- `exception.py` file: Including some exception class related to  the game.
- `data` folder: saved folder for series of action in one game.                    
- `assets` folder: images folder used for visualization.
- `draft` folder: old files.










