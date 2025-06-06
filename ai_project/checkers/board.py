"""Checkers board representation."""

from draughts.boards.american import Board
from draughts.boards.standard import Move

from ai_project.engine import AbstractBoard


class CheckersBoard(Board, AbstractBoard[Move]):
    """Class representing the Checkers board, inheriting from `py-draught`'s `Board` and `AbstractBoard`."""
