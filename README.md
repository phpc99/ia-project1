# Cogito
Cogito is a nice little puzzle game for Windows in which you must use the vertical and horizontal levers to arrange the pieces to match the given pattern.

Heuristics: Number of pieces outside of the objective position or using the Manhattan Distance (computed by counting the number of moves along the grid that each tile is displaced from its goal position, and summing these values over all tiles).

# Features

- Implemented game-state representation to track player moves, available actions, and goal conditions;
- Designed and compared uninformed search algorithms such as Breadth-First Search, Depth-First Search, and Uniform Cost Search;
- Implemented informed search algorithms, including Greedy Search, A*, and Weighted A*, using domain-specific heuristics;
- Allowed both manual gameplay and automated solving through AI search techniques;
- Evaluated algorithms based on solution quality, execution time, and memory efficiency;
- Included a visual or textual interface to display the board state and illustrate the solving process.

# Screenshots

### Main menu
![mainmenu](https://github.com/phpc99/ia-project1/blob/main/mainmenu.png)

### Difficulty Selection
![diffmenu](https://github.com/phpc99/ia-project1/blob/main/difficultymenu.png)

### Algorithm Selection for AI Mode
![aimode](https://github.com/phpc99/ia-project1/blob/main/aimode.png)

### Easy Mode
![easy](https://github.com/phpc99/ia-project1/blob/main/game1.png)

### Normal Mode
![normal](https://github.com/phpc99/ia-project1/blob/main/game2.png)

### Victory
![end](https://github.com/phpc99/ia-project1/blob/main/end.png)

# How to compile
Make sure you are in the CogitoGame folder then run the command _python main.py_

# Authors

- Afonso Gouveia Dias 
- Pedro Henrique Pessôa Camargo
