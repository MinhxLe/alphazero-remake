import numpy as np
from typing import Literal, Optional
import attrs

Player = Literal[1, 2]
EMPTY_SPACE = 0


@attrs.define
class ConnectN:
    n: int
    n_rows: int
    n_cols: int
    board: np.ndarray = attrs.field(init=False)
    current_player: Player = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.board = np.zeros((self.n_rows, self.n_cols), dtype=np.int8)
        self.current_player = 1

    def reset(self):
        self.board = np.zeros((self.n_rows, self.n_cols), dtype=np.int8)
        self.current_player = 1

    def get_valid_moves(self) -> np.ndarray:
        return np.where(np.any(self.board == EMPTY_SPACE, axis=0))[0]

    def make_move(self, col: int) -> None:
        """Makes a move in the specified column"""
        assert col in self.get_valid_moves()

        row = np.where(self.board[:, col] == EMPTY_SPACE)[0][0]
        self.board[row, col] = self.current_player
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def is_terminal(self):
        return len(self.get_valid_moves()) == 0 or self.check_win() is not None

    def check_win(self) -> Player | None:
        for player in [1, 2]:
            for r in range(self.n_rows):
                for c in range(self.n_cols):
                    # we don't need to check all 8 directions due to symmetries
                    for dr, dc in [
                        (0, 1),  # horizonal
                        (1, 0),  # vertical
                        (1, 1),  # diagnonal right
                        (1, -1),  # diagonal left
                    ]:
                        if self._is_n_in_a_row(player, r, c, dr, dc):
                            return player
        return None

    def _is_n_in_a_row(self, player: Player, r: int, c: int, dr: int, dc: int):
        for _ in range(self.n):
            if self._is_inbound(r, c) and self.board[r][c] == player:
                r += dr
                c += dc
            else:
                return False
        return True

    def _is_inbound(self, r: int, c: int):
        return 0 <= r < self.n_rows and 0 <= c < self.n_cols


class Connect4(ConnectN):
    def __init__(self):
        super().__init__(4, 6, 7)
