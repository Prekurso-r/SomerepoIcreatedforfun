# My_CS50_Projects

Solutions for CS50's Introduction to Artificial Intelligence with Python.

## degrees

Finds the shortest connection between two actors via the movies they starred in
("six degrees of Kevin Bacon"). Implemented as a breadth-first search over the
actor graph, so the first path found is guaranteed to be a shortest one.

```
cd degrees
python degrees.py small
```

The large IMDb dataset (`degrees/large/`) is excluded from this repo — it is
~56 MB of course-distribution data. Download it from the CS50 distribution and
place it at `degrees/large/` to run `python degrees.py large`.

## tictactoe

An unbeatable tic-tac-toe AI using minimax with alpha-beta pruning. Pruning
only skips branches a rational opponent would never allow, so it returns the
same move as plain minimax, just faster.

```
cd tictactoe
pip install -r requirements.txt
python runner.py
```
