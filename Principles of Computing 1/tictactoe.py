"""
Monte Carlo Tic-Tac-Toe Player
"""

import random

# import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100  # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0  # Score for squares played by the other player


# Add your functions here.

def mc_trial(board, player):
    """
    :param board: The current board state
    :param player: The next player to move
    :return: Does not return any value but instead plays out the game and changes the state of the board
    """
    while board.check_win() == None:
        next_move = board.get_empty_squares()
        random_cell = random.choice(next_move)
        board.move(random_cell[0], random_cell[1], player)
        player = provided.switch_player(player)


def mc_update_scores(scores, board, player):
    """
    :param scores: A 2D array which we will edit with the updated scores
    :param board: The completed board
    :param player: Which player is the machine
    :return: Updates the scores parameter
    """

    other_player = provided.switch_player(player)

    for index_i in range(board.get_dim()):
        for index_j in range(board.get_dim()):
            if board.square(index_i, index_j) == player:
                if board.check_win() == player:
                    scores[index_i][index_j] += SCORE_CURRENT
                if board.check_win() == other_player:
                    scores[index_i][index_j] += -SCORE_CURRENT
            if board.square(index_i, index_j) == other_player:
                if board.check_win() == player:
                    scores[index_i][index_j] += -SCORE_OTHER
                if board.check_win() == other_player:
                    scores[index_i][index_j] += SCORE_OTHER


def get_best_move(board, scores):
    """
    :param board: Current board state
    :param scores: Grid of scores
    :return: Finds all of the empty squares and returns the one with the max score
    """
    max_val = -10000000
    empty_square = ()
    arr = board.get_empty_squares()
    for (index_row, index_col) in arr:
        if scores[index_row][index_col] > max_val:
            max_val = scores[index_row][index_col]
            empty_square = (index_row, index_col)
    return empty_square


def mc_move(board, player, trials):
    """
    :param board: The current state of the board
    :param player: The machine player id
    :param trials: The number of trials to run
    :return: Should return a square tuple to go to next
    """
    score = [[0 for dummy_i in range(board.get_dim())] for dummy_j in range(board.get_dim())]

    machine_player = 0 + player # Is this still a reference?
    for dummy_trial in range(trials):
        new_board = board.clone()
        mc_trial(new_board, player)
        mc_update_scores(score, new_board, machine_player)
    return get_best_move(board, score)

provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
