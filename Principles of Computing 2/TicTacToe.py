"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor

codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}


def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """

    if board.check_win() is not None:
        return SCORES[board.check_win()], (-1, -1)

    all_empty = board.get_empty_squares()

    optimize = None
    board_pos = None

    for (x_pos, y_pos) in all_empty:
        new_board = board.clone()
        new_board.move(x_pos, y_pos, player)
        val = mm_move(new_board, provided.PLAYERO if player == provided.PLAYERX else provided.PLAYERX)[0]
        if player == provided.PLAYERX:
            if optimize is None:
                optimize = val
            optimize = max(optimize, val)
            if optimize == val:
                board_pos = (x_pos, y_pos)
            if optimize == 1:
                break
        else:
            if optimize is None:
                optimize = val
            optimize = min(optimize, val)
            if optimize == val:
                board_pos = (x_pos, y_pos)
            if optimize == -1:
                break

    return optimize, board_pos


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]
