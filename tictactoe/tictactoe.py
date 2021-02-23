"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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
    
    #check if board is empty
    if terminal(board):
        return

    #create X and O counters
    Xnumber = 0
    Onumber = 0

    if board == initial_state():
        return X
    else:
        for line in board:
            for j in line:
                if j == X:
                    Xnumber += 1
                elif j == O:
                    Onumber += 1

        if Xnumber == Onumber:
            return X
        else:
            return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #Check if game is over
    if terminal(board):
        return

    action = set()
    for i,row in enumerate(board):
        for j,col in enumerate(row):
            if board[i][j] == EMPTY:
                action.add((i,j))
    return action

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = deepcopy(board)
    if action not in actions(board):
        raise Exception("Action not available!")
    else:
        if player(board) == X:
            board_copy[action[0]][action[1]] = X
        elif player(board) == O:
            board_copy[action[0]][action[1]] = O
    return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O
    #Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == X:
                return X
            elif board[0][i] == O:
                return O
    #Check diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
    if board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] == X:
            return X
        elif board[2][0] == O:
            return O
    return None
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board)!=None:
        return True

    for i, row in enumerate(board):
        for j,col in enumerate(row):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        return max_value(board)[1]
    elif player(board) == O:
        return min_value(board)[1]

def min_value(board):
    """Returns the lowest value of a board"""
    if terminal(board):
        return utility(board), None

    v = float('inf')
    move = None
    for action in actions(board):
        val = max_value(result(board,action))
        if val[0] < v:
            v = val[0]
            move = action
            if v==-1:
                return v,move

    return v, move

def max_value(board):
    """Returns the highest value from  a board"""
    if terminal(board):
        return utility(board), None

    v = float('-inf')
    move = None
    for action in actions(board):
        val = min_value(result(board,action))
        if val[0]>v:
            v=val[0]
            move = action
            if v == 1:
                return v, move

    return v, move





















