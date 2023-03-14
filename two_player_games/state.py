

from typing import Iterable, Optional

from two_player_games.move import Move
from two_player_games.player import Player

#Niezmienny obiekt stanu gry
class State:
    def __init__(self, current_player, other_player) -> None:
        self._current_player = current_player
        self._other_player = other_player

    def get_moves(self) -> Iterable[Move]: #Możliwe ruchy
        raise NotImplementedError

    def get_current_player(self) -> Player: #Obecny gracz
        return self._current_player

    def make_move(self, move: Move) -> 'State': #move: ruch do wykonania -> State: Stan po ruchu
        raise NotImplementedError

    def is_finished(self) -> bool: #Jeśli gra skończona
        raise NotImplementedError

    def get_winner(self) -> Optional[Player]: #Gracz, który wygrał lub None, jeśli remis lub nie skończył
        raise NotImplementedError

    def get_heuristic(self) -> int: #heuristics znaczenie stanu gry
        raise NotImplementedError

    def get_players(self) -> Iterable[Player]: #Iterowalność graczy w grze
        return [self._current_player, self._other_player]

    def __str__(self) -> str: #str reprezentujący stan gry
        raise NotImplementedError
