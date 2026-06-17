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
    """
    Returns player who has the next turn on a board.
    """
    #assumed that X goes first 
    # if even number of moves have been made, its X's turn since X goes first
    totalmoves = sum(cell is not EMPTY for row in board for cell in row)
    return X if totalmoves % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # go through every cell, if its empty then its a valid move
    validmoves = set()
    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                validmoves.add((r, c))
    return validmoves

#
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    r, c = action   #here the orignal board must stay unchanged for tree exploration

   #boundary checking
    if not (0 <= r <= 2 and 0 <= c <= 2):
        raise Exception("that move is out of bounds")
    if board[r][c] is not EMPTY:
        raise Exception("that cell is already taken")

    # copy the board first so we dont mess up the original as we need it for minimax
    updatedboard = copy.deepcopy(board)
    updatedboard[r][c] = player(board)
    return updatedboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    #max only 1 winner will exist on the board at a given state
    winninglines = [    # put all possible winning combinations in one list
       
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)],
    ]

    for line in winninglines:
        a, b, c = line
        if board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]]:
            if board[a[0]][a[1]] is not EMPTY:
                return board[a[0]][a[1]]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #someone has won game so it ends or 
    if winner(board) is not None:
        return True

    # if every single cell is filled up aka there is a tie
    boardfull = all(cell is not EMPTY for row in board for cell in row)
    return boardfull


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #called at the terminal board
    result = winner(board)

    if result == X:
        return 1
    elif result == O:
        return -1

    #is a tie
    return 0


def getmax(board):
    # X is the maximizing player that wil try to counter O with  1
    # game is over so just return the score
    if terminal(board):
        return utility(board)

    bestscore = -math.inf  
    for move in actions(board):
        score = getmin(result(board, move))
        if score > bestscore:
            bestscore = score
    return bestscore


def getmin(board):
    # O is the minimizing player that will try to counter X with  -1 meaning if its 0s turn whats the worst score x can get from here
    #game is over so return score
    if terminal(board):
        return utility(board)

    bestscore = math.inf
    for move in actions(board):
        score = getmax(result(board, move))
        if score < bestscore:
            bestscore = score
    return bestscore


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Assummed that X is maximizing player, O is minimizing player, both play 50/50
     #game already over
    if terminal(board):
        return None

    whoseturn = player(board)    
    bestmove = None

    if whoseturn == X:
        # X is the max
        bestscore = -math.inf
        for move in actions(board):   #seraching every possible move
            score = getmin(result(board, move))
            if score > bestscore:  
                bestscore = score
                bestmove = move

    else:
        # 0 is the min here
        bestscore = math.inf
        for move in actions(board):
            score = getmax(result(board, move))
            if score < bestscore:
                bestscore = score
                bestmove = move

    return bestmove