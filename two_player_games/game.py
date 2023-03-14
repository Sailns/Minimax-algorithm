from typing import Iterable, Optional
from two_player_games.move import Move
from two_player_games.player import Player
from two_player_games.state import State

# Klas Interfejs gry
class Game:
    def __init__(self, state: State):
        self.state = state

    def get_moves(self) -> Iterable[Move]:
        return self.state.get_moves()

    def get_current_player(self) -> Player:
        return self.state.get_current_player()

    def make_move(self, move: Move):
        self.state = self.state.make_move(move)

    def is_finished(self) -> bool:
        return self.state.is_finished()

    def get_winner(self) -> Optional[Player]:
        return self.state.get_winner()

    def get_heuristic(self) -> int:
        return self.state.get_heuristic()

    def get_players(self) -> Iterable[Player]:
        return self.state.get_players()

    def __str__(self) -> str:
        return str(self.state)
