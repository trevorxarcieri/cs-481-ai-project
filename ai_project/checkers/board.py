"""Checkers board representation.

Authors: Trevor Arcieri and Demetri Karras
Course: CS 481 Artificial Intelligence
Term: Spring 2025
Project: DualBoard Negamax AI
"""

from __future__ import annotations

import math

from draughts.boards.base import BaseBoard
from draughts.move import Move

from ai_project.engine import AbstractBoard


class CheckersBoard(BaseBoard, AbstractBoard[Move]):
    """Class representing the Checkers board, inheriting from `py-draught`'s `Board` and `AbstractBoard`."""

    @staticmethod
    def size(board: CheckersBoard) -> int:
        """Return the size of the board."""
        return int(math.sqrt(len(board.STARTING_POSITION) * 2))
