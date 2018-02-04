# Command line based Minesweeper in Python3

A text input based game made using Python3.
Pass the grid size and difficulty as command line arguments.
Example:
```
python myMinesweeper.py 6 6 0.3
  a   b   c   d   e   f

 --- --- --- --- --- ---
|   |   |   |   |   |   |  1
 --- --- --- --- --- ---
|   |   |   |   |   |   |  2
 --- --- --- --- --- ---
|   |   |   |   |   |   |  3
 --- --- --- --- --- ---
|   |   |   |   |   |   |  4
 --- --- --- --- --- ---
|   |   |   |   |   |   |  5
 --- --- --- --- --- ---
|   |   |   |   |   |   |  6
 --- --- --- --- --- ---

Enter "stop" to stop the game any time

Enter the column alphabet, row number and optional flag (f) separated b space.

eg1. "a 3 f" will mark a,3 with flag.

eg2. "a 3" will click on a3.
```

Once the game is started, just enter the alphabet column followed by a space and the row number followed by an optional flag f.
Example:
```
a 3 f
```

Also enter "stop" anytime during the game to exit.

Here's a demo of this game.

![Demo](/demo.png)
