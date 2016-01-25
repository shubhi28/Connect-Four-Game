from util import memoize, run_search_function
from util import INFINITY, NEG_INFINITY

# Global Variable used to count the number of Expanded Nodes
numExpandNodes = 0

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified.
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3 - col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3 - col)

    return score

def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    global numExpandNodes
    from connectfour import InvalidMoveException
    for i in xrange(board.board_width):
        # Incrementing value of Expanded nodes
        numExpandNodes += 1
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass


def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()


# Function to Return Minimum value at a node for Minmax Search
def min_value(depth, board, eval_fn, col):
    if is_terminal(depth, board):
        return -eval_fn(board), col
    v = INFINITY
    successor = get_all_next_moves(board)
    for i, move in successor:
        maxv, c = max_value(depth - 1, move, eval_fn, col)
        if maxv < v:
            v = maxv
            col = i
    return v, col

#Function to Return Maximum value at a node for Minmax Search
def max_value(depth, board, eval_fn, col):
    if is_terminal(depth, board):
        return (eval_fn(board), col)
    v = NEG_INFINITY
    successor = get_all_next_moves(board)
    for i, move in successor:
        minv,c = min_value(depth - 1, move, eval_fn, col)
        if minv > v:
            v = minv
            col = i
    return v, col


def minimax(board, depth, eval_fn,
            get_next_moves_fn=get_all_next_moves,
            is_terminal_fn=is_terminal,
            verbose=True):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """
    col = -1
    v, col = max_value(depth, board, eval_fn, col)
    return col


def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]

# New Heuristic function to calculate the value at terminal node
def new_evaluate(board):
    currId=board.get_current_player_id()
    otherId=board.get_other_player_id()
    other_numFour=0

    numFour=getLongestChain(currId,board,4)
    numThree=getLongestChain(currId,board,3)
    numTwo=getLongestChain(currId,board,2)
    other_numFour=getLongestChain(otherId,board,4)

    score=numFour*100000+numThree*100+numTwo

    if other_numFour > 0:
        return -100000
    else:
        return score

def getLongestChain(id,board,len):
    count=0
    for row in range(6):
        for col in range(7):
            if board.get_cell(row,col) == id:
                count+=verticalChain(row,col,board,len,id)
                count+=horizontalChain(row,col,board,len,id)
                count+=posDiagonalChain(row,col,board,len,id)
                count+=negDiagonalChain(row,col,board,len,id)
    return count

def verticalChain(row,col,board,len,id):
    vLongest=0
    for i in range(row,6):
        if board.get_cell(i,col)==id:
            vLongest+=1
        else:
            break
    if vLongest >= len:
        return 1
    else:
        return 0

def horizontalChain(row, col, board,len,id):
    hLongest = 0
    for i in range(col, 7):
        if board.get_cell(row,i)==id:
            hLongest += 1
        else:
            break
    if hLongest >=len:
        return 1
    else:
        return 0


def posDiagonalChain(row,col,board,len,id):
    pdLongest = 0
    n = col
    for m in range(row, 6):
        if n >= 7 or board.get_cell(m,n)!= id:
            break
        elif board.get_cell(m,n)== id:
            pdLongest += 1
        n += 1

    if pdLongest >= len:
        return 1
    else:
        return 0

def negDiagonalChain(row,col,board,len,id):
    ndLongest = 0
    n = col
    for m in range(row, -1, -1):
        if n >= 7 or board.get_cell(m,n)!=id :
            break
        elif board.get_cell(m,n)== id:
            ndLongest += 1
        n += 1

    if ndLongest >= len:
        return 1
    else:
        return 0

#random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)
