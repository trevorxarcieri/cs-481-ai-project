"""Checkers AI engine using Negamax and Alpha-Beta Pruning."""

from math import floor

from draughts.boards.american import Board
from draughts.boards.standard import Color, Figure, Move

from ai_project.engine import AbstractBoard, AbstractEngine

BOARD_DIM = 8  # Checkers board is 8x8
BOARD_DIM_MINUS_ONE = BOARD_DIM - 1  # Used for distance calculations
BOARD_DIM_MIN_ONE_HALF = BOARD_DIM_MINUS_ONE / 2  # Half of (board dimension - 1)
MAN_VALUE = 5  # Value of a regular piece
KING_VALUE = 10  # Value of a king piece
WALL_DIST_VALUE = 3  # Distance to the wall value for evaluation
SIDE_DIST_VALUE = 2  # Distance to the side value for evaluation


class CheckersBoard(Board, AbstractBoard[Move]):
    """Class representing the Checkers board, inheriting from `py-draught`'s `Board` and `AbstractBoard`."""


class CheckersEngine(AbstractEngine[CheckersBoard, Move]):
    """Class for the Checkers AI engine using Negamax and Alpha-Beta Pruning."""

    def evaluate(self, board: CheckersBoard) -> int:
        """Evaluate the board state."""
        score = 0

        # Evaluate the board position based on the number of pieces
        for i, square in enumerate(board.friendly_form):
            row = i // BOARD_DIM
            col = i % BOARD_DIM
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
                    WALL_DIST_VALUE * (BOARD_DIM_MINUS_ONE - row) / BOARD_DIM_MINUS_ONE
                )
                score += (
                    SIDE_DIST_VALUE
                    * abs(BOARD_DIM_MIN_ONE_HALF - col)
                    / BOARD_DIM_MIN_ONE_HALF
                )
            else:
                score -= WALL_DIST_VALUE * row / BOARD_DIM_MINUS_ONE
                score -= (
                    SIDE_DIST_VALUE
                    * abs(BOARD_DIM_MIN_ONE_HALF - col)
                    / BOARD_DIM_MIN_ONE_HALF
                )

        return floor(score)

    def get_ordered_moves(
        self, board: CheckersBoard, *, negate: bool = False
    ) -> list[Move]:
        """Get legal moves ordered by their potential effectiveness."""
        return sorted(
            board.legal_moves,
            key=lambda move: (
                -len(move.captured_list),  # prefer moves that capture more pieces
                (1 if negate else -1)
                * (move.square_list[-1] // BOARD_DIM / 2 - BOARD_DIM_MIN_ONE_HALF)
                if len(move.square_list) > 0
                else 0,  # prefer moves that advance to the opposite wall
            ),
        )
