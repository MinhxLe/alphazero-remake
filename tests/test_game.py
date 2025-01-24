from a0.game import Connect4, ConnectN
import numpy as np
import pytest


def test_reset():
    game = Connect4()
    game.board[0][0] = 1
    game.current_player = 2
    game.reset()
    assert np.all(game.board == 0)
    assert game.current_player == 1


def test_get_valid_moves_empty():
    game = Connect4()
    assert np.all(game.get_valid_moves() == np.arange(game.n_cols))


def test_get_valid_moves_column_filled():
    game = Connect4()
    game.board[:, :] = 1
    game.board[:, 0] = 0
    assert game.get_valid_moves() == np.array([0])


def test_make_move():
    game = Connect4()
    game.make_move(0)
    assert game.board[0, 0] == 1
    assert game.current_player == 2

    game.make_move(0)
    assert game.board[1, 0] == 2
    assert game.current_player == 1


def test_is_terminal_filled():
    game = Connect4()
    assert not game.is_terminal()
    game.board[:, :] = 1
    assert game.is_terminal()


@pytest.mark.parametrize(
    "coordinates",
    [
        ([0, 0], [0, 1]),
        ([0, 1], [0, 0]),
        ([0, 1], [0, 1]),
        ([0, 1], [1, 0]),  # diagonal
    ],
)
def test_is_terminal_win(coordinates):
    game = ConnectN(n=2, n_rows=2, n_cols=2)
    game.board[coordinates] = 1
    assert game.is_terminal()
    assert np.any(game.board == 0)


@pytest.mark.parametrize(
    "coordinates",
    [
        ([0, 0], [0, 1]),
        ([0, 1], [0, 0]),
        ([0, 1], [0, 1]),
        ([0, 1], [1, 0]),  # diagonal
    ],
)
def test_check_win(coordinates):
    game = ConnectN(n=2, n_rows=2, n_cols=2)
    game.board[coordinates] = 1
    assert game.check_win() == 1
