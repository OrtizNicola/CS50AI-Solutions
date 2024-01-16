"""
Tic Tac Toe Player
"""

import math
import copy

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
    # If the board is empty (9 cells available -> odd) it's X's turn
    # In the second move there's 9 cells available -> even, it's O's turn
    # ...
    # X plays when number of empty cells is odd, O, when it's even
    NumOfEmptyCells = 0

    for row in range(3):
        NumOfEmptyCells += board[row].count(EMPTY)
    
    return X if NumOfEmptyCells % 2 != 0 else O
   
def actions(board):
    # Possible actions = EMPTY cells
    PossibleActions = set()

    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                PossibleActions.add((row, col))

    return PossibleActions

def result(board, action):
    # Return a new board with the player whose turn it is in the place of the action
    if board[action[0]][action[1]] != EMPTY:
        raise Exception(f"{action} is not a valid action")
    else:
        NewBoard = copy.deepcopy(board)
        NewBoard[action[0]][action[1]] = player(board)

    return NewBoard


def winner(board):
    # Goes through every possible combination when there's a winner, if there's none, it returns none
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]: # Goes through each row
            if board[i][0] != EMPTY:
                return board[i][0]
        if board[0][i] == board[1][i] == board[2][i]: # Goes through each column
            if board[0][i] != EMPTY:
                return board[0][i]
            
    if board[0][0] == board[1][1] == board[2][2]: # Looks for a winner in the left to right diagonal
        if board[0][0] != EMPTY:
            return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0]: # Looks for a winner in the right to left diagonal
        if board[0][2] != EMPTY:
            return board[0][2]

    return None

def terminal(board):
    # If there's a winner the game is over, if there's not but the board is full the game is over
    # The game continues if none of the above happened
    if winner(board) is not None:
        return True
    else:
        NumOfEmptyCells = 0

        for row in range(3):
            NumOfEmptyCells += board[row].count(EMPTY) 

        return True if NumOfEmptyCells == 0 else False

def utility(board):
    # Returns values for each player
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def MaxValue(state, alpha, beta):
    # Calculates the best value and move in a maximizing position
    if terminal(state):
        return (utility(state), None)
    BestAction = None
    for action in actions(state):
        ScoreOfTheAction = MinValue(result(state, action), alpha, beta)[0] 
        if alpha < ScoreOfTheAction:
            alpha = ScoreOfTheAction
            BestAction = action
        if beta <= alpha:
            break
    return (alpha, BestAction)

def MinValue(state, alpha, beta):
    # Calculates the best value and move in a minimizing position
    if terminal(state):
        return (utility(state), None)
    BestAction = None
    for action in actions(state):
        ScoreOfTheAction = MaxValue(result(state, action), alpha, beta)[0]
        if ScoreOfTheAction < beta:
            beta = ScoreOfTheAction
            BestAction = action
        if beta <= alpha:
            break
    return (beta, BestAction)

def minimax(board):
    # minimax algorithm using alpha-beta pruning
    if player(board) == X:
        return MaxValue(board, -2, 2)[1]
    if player(board) == O:
        return MinValue(board, -2, 2)[1]

### Note: If there's more than one winning move, the algorithm doesn't necessarily returns the fastest one