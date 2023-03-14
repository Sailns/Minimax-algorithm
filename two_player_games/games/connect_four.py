from dataclasses import fields
from two_player_games.move import Move
from typing import Iterable, List, Optional, Tuple
from two_player_games.game import Game
from two_player_games.player import Player
from two_player_games.state import State

#Klasa reprezentująca grę szesnastkową
class ConnectFour(Game):

    FIRST_PLAYER_DEFAULT_CHAR = '1'
    SECOND_PLAYER_DEFAULT_CHAR = '2'

#Inicjuje grę
    def __init__(self, size: Tuple[int, int] = (7, 6), first_player: Player = None, second_player: Player = None):
        """
            size: rozmiar gry jako liczba kolumn i wierszy
            first_player: gracz, który pójdzie pierwszy (jeśli żaden nie zostanie przekazany, zostanie utworzony gracz)
            second_player: gracz, który zajmie drugie miejsce (jeśli żaden nie zostanie przekazany, zostanie utworzony gracz)
        """
        self.first_player = first_player or Player(self.FIRST_PLAYER_DEFAULT_CHAR)
        self.second_player = second_player or Player(self.SECOND_PLAYER_DEFAULT_CHAR)

        state = ConnectFourState(size, self.first_player, self.second_player)
        super().__init__(state)

#Klasa reprezentująca ruch w grze w kropki i kwadraty
class ConnectFourMove(Move):

    def __init__(self, column) -> None: #indeks kolumny, w której ma zostać umieszczony token
        self.column = column
        super().__init__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConnectFourMove):
            return False
        return self.column == other.column


#Klasa reprezentująca stan gry szesnastkowej
class ConnectFourState(State): 

    def __init__(
            self, size: Tuple[int, int] = None, current_player: Player = None, other_player: Player = None,
            fields: List[List[Player]] = None
    ):
        if fields is not None:
            self.fields = fields
        else:
            cols, rows = size
            self.fields = [[None for _ in range(rows)] for _ in range(cols)]

        super().__init__(current_player, other_player)

    def get_moves(self) -> Iterable[ConnectFourMove]:
        return [ConnectFourMove(i) for i, column in enumerate(self.fields) if column[-1] is None]

    def get_current_player(self) -> Player:
        return self._current_player

    def make_move(self, move: ConnectFourMove) -> 'ConnectFourState':
        new_fields = [list(column) for column in self.fields]
        self._put(new_fields, move)
        return ConnectFourState(current_player=self._other_player, other_player=self._current_player, fields=new_fields)

    def is_finished(self) -> bool:
        return self.get_winner() is not None or len(self.get_moves()) == 0

    def get_winner(self) -> Optional[Player]:
        for column_id in range(len(self.fields)):  # verticals
            for start_row_id in range(len(self.fields[column_id]) - 3):
                winner = self._check_four((column_id, start_row_id), (0, 1))
                if winner:
                    return winner

        for start_column_id in range(len(self.fields) - 3):  # horizontals
            for row_id in range(len(self.fields[start_column_id])):
                winner = self._check_four((start_column_id, row_id), (1, 0))
                if winner:
                    return winner

        for start_column_id in range(len(self.fields) - 3):  # diagonals
            for start_row_id in range(len(self.fields[start_column_id]) - 3):
                winner = \
                    self._check_four((start_column_id, start_row_id), (1, 1)) \
                    or self._check_four((start_column_id, start_row_id + 3), (1, -1))
                if winner:
                    return winner

        return None

    def get_heuristic(self) -> int:
        v1 = v2 = v3 = 0
        for column_id in range(len(self.fields)):  # verticals
            for start_row_id in range(len(self.fields[column_id]) - 3):
                v1 += self._heuristic((column_id, start_row_id), (0, 1))

        for start_column_id in range(len(self.fields) - 3):  # horizontals
            for row_id in range(len(self.fields[start_column_id])):
                v2 += self._heuristic((start_column_id, row_id), (1, 0))

        for start_column_id in range(len(self.fields) - 3):  # diagonals
            for start_row_id in range(len(self.fields[start_column_id]) - 3):
                v3 += \
                    self._heuristic((start_column_id, start_row_id), (1, 1)) \
                    or self._heuristic((start_column_id, start_row_id + 3), (1, -1))
        return v1 + v2 + v3

    def __str__(self) -> str:
        transposed = zip(*self.fields)
        text = '\n'.join(
            reversed([''.join(f'[{" " if field is None else field.char}]' for field in row) for row in transposed])
        )

        return f'Current player: {self._current_player.char}\n{text}'

    # metody pomocnicze dla interfejsu
    def _put(self, fields: List[List[Player]], move: ConnectFourMove) -> None:
        for i, field in enumerate(fields[move.column]):
            if field is None:
                fields[move.column][i] = self._current_player
                break

    def _check_four(self, start_coords: Tuple[int, int], move_coords: Tuple[int, int]) -> Optional[Player]:
        fields = {
            self.fields[start_coords[0] + move_coords[0] * i][start_coords[1] + move_coords[1] * i] for i in range(4)
        }

        if len(fields) != 1:
            return None

        return next(iter(fields))
    
    #heuristics value stanu gry
    def _heuristic(self, start_coords: Tuple[int, int], move_coords: Tuple[int, int]) -> int:
        fields = [
            self.fields[start_coords[0] + move_coords[0] * i][start_coords[1] + move_coords[1] * i] for i in range(4)
        ]
        cp = self._current_player
        count_none = count_cp = count_op = h_sum = 0
        for i in range(len(fields)):
            if fields[i] == cp:
                count_cp += 1
            elif fields[i] is None:
                count_none += 1
            else:
                count_op += 1
        if count_cp == 4:
            h_sum += 100
        elif count_cp == 3 and count_none == 1:
            h_sum += 5
        elif count_cp == 2 and count_none == 2:
            h_sum += 2
        if count_op == 3 and count_none == 1:
            h_sum -= 10
        return h_sum
