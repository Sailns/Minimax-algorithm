import math

import numpy as np


def evaluate_position(game_state):
    return game_state.get_heuristic()


def get_winner(game_state):
    return game_state.get_winner()


def current_player(game_state):
    return game_state.get_current_player()


def is_finished(game_state):
    return game_state.is_finished()



def alphabeta(game_state, players, alpha, beta, maximising_player):
    if players == 0 or is_finished(game_state):
        if is_finished(game_state):
            winner = get_winner(game_state)
            if winner is current_player(game_state):
                return 10e6, None
            elif winner is not (current_player(game_state) or None):
                return -10e6, None
            else:
                return 0, None
        else:
            return evaluate_position(game_state), None
    if maximising_player:
        max_eval = -math.inf
        possible_moves = game_state.get_moves()
        rng = np.random.default_rng()
        rng.shuffle(possible_moves)
        best_move = rng.choice(possible_moves)
        for move in possible_moves:
            state = game_state.make_move(move)
            eval = alphabeta(state, players - 1, alpha, beta, False)[0]
            if eval > max_eval:
                max_eval = eval
                best_move = move
            elif max_eval == eval:
                rng = np.random.default_rng()
                best_move = rng.choice([best_move, move])
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break

        return max_eval, best_move
    else:
        min_eval = math.inf
        possible_moves = game_state.get_moves()
        rng = np.random.default_rng()
        rng.shuffle(possible_moves)
        best_move = rng.choice(possible_moves)
        for move in possible_moves:
            state = game_state.make_move(move)
            eval = alphabeta(state, players - 1, alpha, beta, True)[0]
            if eval < min_eval:
                min_eval = eval
                best_move = move
            elif min_eval == eval:
                rng = np.random.default_rng()
                best_move = rng.choice([best_move, move])
            min_eval = min(min_eval, eval)
            beta = min(beta, min_eval)
            if alpha >= beta:
                break
        return min_eval, best_move
