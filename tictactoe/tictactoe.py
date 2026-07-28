"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # X moves first, so X is up whenever both players have made equally
    # many moves.
    moves = sum(cell is not EMPTY for row in board for cell in row)
    return X if moves % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j)
            for i in range(3)
            for j in range(3)
            if board[i][j] is EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError(f"invalid action: {action}")

    # Deep copy so the caller's board (and every board already on the
    # minimax search stack) is left untouched.
    new_board = copy.deepcopy(board)
    i, j = action
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = []
    for i in range(3):
        lines.append([board[i][0], board[i][1], board[i][2]])   # rows
        lines.append([board[0][i], board[1][i], board[2][i]])   # columns
    lines.append([board[0][0], board[1][1], board[2][2]])       # diagonal
    lines.append([board[0][2], board[1][1], board[2][0]])       # anti-diagonal

    for line in lines:
        if line[0] is not EMPTY and line[0] == line[1] == line[2]:
            return line[0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    return all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    won = winner(board)
    if won == X:
        return 1
    if won == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    alpha = -math.inf
    beta = math.inf
    best_action = None

    if player(board) == X:
        # X maximizes: keep the action with the highest achievable value.
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action), alpha, beta)
            if value > best_value:
                best_value, best_action = value, action
            alpha = max(alpha, best_value)
    else:
        # O minimizes.
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action), alpha, beta)
            if value < best_value:
                best_value, best_action = value, action
            beta = min(beta, best_value)

    return best_action


def max_value(board, alpha, beta):
    """
    Returns the best value X can force from this board, pruning branches
    that a rational minimizer would never allow to be reached.
    """
    if terminal(board):
        return utility(board)

    value = -math.inf
    for action in actions(board):
        value = max(value, min_value(result(board, action), alpha, beta))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


def min_value(board, alpha, beta):
    """
    Returns the best value O can force from this board, with the same
    pruning in the opposite direction.
    """
    if terminal(board):
        return utility(board)

    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action), alpha, beta))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value
