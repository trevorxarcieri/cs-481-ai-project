"""Checkers AI engine using Negamax and Alpha-Beta Pruning.

Authors: Trevor Arcieri and Demetri Karras
Course: CS 481 Artificial Intelligence
Term: Spring 2025
Project: DualBoard Negamax AI
"""

from math import floor

from draughts.models import Color, Figure
from draughts.move import Move

from ai_project.checkers.board import CheckersBoard
from ai_project.engine import AbstractEngine

MAN_VALUE = 5  # Value of a regular piece
KING_VALUE = 10  # Value of a king piece
WALL_DIST_VALUE = 3  # Distance to the wall value for evaluation
SIDE_DIST_VALUE = 2  # Distance to the side value for evaluation


class CheckersEngine(AbstractEngine[CheckersBoard, Move]):
    """Class for the Checkers AI engine using Negamax and Alpha-Beta Pruning."""

    def evaluate(self, board: CheckersBoard) -> int:
        """Evaluate the board state."""
        score = 0

        # Evaluate the board position based on the number of pieces
        for i, square in enumerate(board.friendly_form):
            row = i // CheckersBoard.size(board)
            col = i % CheckersBoard.size(board)
            if square == Figure.EMPTY:
                continue
            if square == Figure.WHITE_MAN:
                score += MAN_VALUE
            elif square == Figure.BLACK_MAN:
                score -= MAN_VALUE
            elif square == Figure.WHITE_KING:
                score += KING_VALUE
            elif square == Figure.BLACK_KING:
                score -= KING_VALUE

            if square / abs(square) == Color.WHITE.value:
                score += (
                    WALL_DIST_VALUE
                    * (CheckersBoard.size(board) - 1 - row)
                    / (CheckersBoard.size(board) - 1)
                )
                score += (
                    SIDE_DIST_VALUE
                    * abs(((CheckersBoard.size(board) - 1) / 2) - col)
                    / ((CheckersBoard.size(board) - 1) / 2)
                )
            else:
                score -= WALL_DIST_VALUE * row / (CheckersBoard.size(board) - 1)
                score -= (
                    SIDE_DIST_VALUE
                    * abs(((CheckersBoard.size(board) - 1) / 2) - col)
                    / ((CheckersBoard.size(board) - 1) / 2)
                )

        return floor(score)

    def get_ordered_moves(
        self, board: CheckersBoard, *, is_min_turn: bool = False
    ) -> list[Move]:
        """Get legal moves ordered by their potential effectiveness."""
        return sorted(
            board.legal_moves,
            key=lambda move: (
                -len(move.captured_list),  # prefer moves that capture more pieces
                (1 if is_min_turn else -1)
                * (
                    (move.square_list[-1] // CheckersBoard.size(board)) / 2
                    - ((CheckersBoard.size(board) - 1) / 2)
                )
                if len(move.square_list) > 0
                else 0,  # prefer moves that advance to the opposite wall
            ),
        )
