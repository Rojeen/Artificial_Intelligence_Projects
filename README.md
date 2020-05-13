# AI Projects
soduku.py:

Sudoku solver that implements backtracking search with forward checking using the minimum remaining value heuristic

Input a string that represents the board from left to right starting from the top row. Represent an empty space with a 0.

For example, run "python3 sudoku.py 003020600900305001001806400008102900700000008006708200002609500800203009005010300"

puzzle.py:

Agent that solves the 8-puzzle game using depth-first search (DFS), breadth-first search (DFS), and A* search. Run the program specifying which search you want to use and a list of integers with commas and without spaces to represent the board. Represent the empty space with a 0. Use "dfs" to use depth-first search, "bfs" to use breadth-first search, and "ast" to use A* search.

For example, run "python3 puzzle.py bfs 0,8,7,6,5,4,3,2,1"
______________________________________________________________________________________________________________________________

Machine Learning Models

2048:

Adversarial search agent that plays the 2048-puzzle game using expectiminimax with alpha-beta pruning and heuristic functions with different weights.

Execute the game using "python3 GameManager.py"

Hand Gesture Classifier for Sign Language:

Model that uses Convolutional Neural Networks (CNNs) and Keras to classifier hand gestures for sign language. Uses train.csv for training and test.csv for testing (stored as zipped files here).

Execute by running "python sign_language.py" or using sign_language.ipynb in Google Colab.

K-Means Clustering:

Clustering model that segments and groups the pixels of trees.png according to their RGB values with k-means.

Execute by running "python clustering.py"

Linear Regression:

Linear regression model that uses gradient descent to predict height (m) using age (yr) and weight (kg), using data derived from CDC growth charts data.

Execulte by running "python lr.py data2.csv results2.csv"

Perceptron:

Perceptron model for a linearly seperable dataset.

Execute by running "python pla.py data1.csv results1.csv"

