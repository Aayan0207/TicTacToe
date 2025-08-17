from copy import deepcopy
from random import randint

X = "X"
O = "O"

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if (board[0][0] == board[1][0] == board[2][0] == X) or (
        board[0][0] == board[1][0] == board[2][0] == O
    ):
        return board[0][0]
    elif (board[0][1] == board[1][1] == board[2][1] == X) or (
        board[0][1] == board[1][1] == board[2][1] == O
    ):
        return board[0][1]
    elif (board[0][2] == board[1][2] == board[2][2] == X) or (
        board[0][2] == board[1][2] == board[2][2] == O
    ):
        return board[0][2]
    elif (board[0][0] == board[0][1] == board[0][2] == X) or (
        board[0][0] == board[0][1] == board[0][2] == O
    ):
        return board[0][0]
    elif (board[1][0] == board[1][1] == board[1][2] == X) or (
        board[1][0] == board[1][1] == board[1][2] == O
    ):
        return board[1][0]
    elif (board[2][0] == board[2][1] == board[2][2] == X) or (
        board[2][0] == board[2][1] == board[2][2] == O
    ):
        return board[2][0]
    elif (board[0][0] == board[1][1] == board[2][2] == X) or (
        board[0][0] == board[1][1] == board[2][2] == O
    ):
        return board[0][0]
    elif (board[0][2] == board[1][1] == board[2][0] == X) or (
        board[0][2] == board[1][1] == board[2][0] == O
    ):
        return board[0][2]
    else:
        return None


def initialize():
    """Sets up board for starting the game"""
    return [["" for i in range(3)] for j in range(3)]


def player(board):
    """Returns current player"""
    counter = 0
    for i in board:
        for j in i:
            if not j:
                counter += 1
    if (9 - counter) % 2 == 0:
        return X
    return O


def random_move():
    return randint(0, 2), randint(0, 2)


def result(board, move):
    """Returns resultant board after making a move"""
    board_clone = deepcopy(board)
    if not board_clone[move[0]][move[1]]:
        board_clone[move[0]][move[1]] = player(board)
    return board_clone


def moves(board):
    """Returns all possible moves for current board"""
    actions = set()
    for row in range(3):
        for column in range(3):
            if not board[row][column]:
                actions.add(tuple((row, column)))
    return actions


def is_valid(move, board):
    """Checks if proposed move is valid or not on current board"""
    if not (0 <= move[0] <= 2) or not (0 <= move[1] <= 2):
        return False
    if board[move[0]][move[1]]:
        return False
    return True


def game_over(board):
    """Checks if the game has finished or not"""
    if winner(board):
        return True
    counter = 0
    for row in board:
        for column in row:
            if not column:
                counter += 1
    if counter:
        return False
    return True


def utility(board):
    "Helper function for Minimax"
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def minimax(board):
    "Minimax AI Algorithm"
    if game_over(board):
        return None
    elif player(board) == X:
        return max_value(board)[0]
    elif player(board) == O:
        return min_value(board)[0]


def max_value(board):
    """Tries to maximize value -Minimax"""
    if game_over(board):
        return None, utility(board)
    move, check = None, float("-inf")
    for action in moves(board):
        minimum = min_value(result(board, action))
        if minimum[1] > check:
            move, check = action, minimum[1]
    return move, check


def min_value(board):
    """Tries to minimize value -Minimax"""
    if game_over(board):
        return None, utility(board)
    move, check = None, float("inf")
    for action in moves(board):
        maximum = max_value(result(board, action))
        if maximum[1] < check:
            move, check = action, maximum[1]
    return move, check
