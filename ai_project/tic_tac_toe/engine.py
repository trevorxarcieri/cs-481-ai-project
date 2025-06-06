"""Tic-tac-toe AI engine using Negamax and Alpha-Beta Pruning."""

from ai_project.engine import AbstractEngine
from ai_project.tic_tac_toe.board import WINNING_LINES, TttBoard, TttMark, TttMove

NUM_MARKS_VALUES = [
    0,
    10,
    100,
]  # Values for no marks, one mark, and two marks in a line
POS_VALUES = [
    3,
    2,
    3,
    2,
    1,
    2,
    3,
    2,
    3,
]  # Values for for each position in the board, corners > edges > center


class TttEngine(AbstractEngine[TttBoard, TttMove]):
    """Class for the Tic-tac-toe AI engine using Negamax and Alpha-Beta Pruning."""

    def evaluate(self, board: TttBoard) -> int:
        """Evaluate the board state."""
        score = 0

        # Add to score based on number of marks in winning lines
        for line in WINNING_LINES:
            line_str = "".join(board[i] for i in line)
            num_o = line_str.count(TttMark.o)
            score += NUM_MARKS_VALUES[num_o]
            num_x = line_str.count(TttMark.x)
            score -= NUM_MARKS_VALUES[num_x]

        # Add positional values
        for i, mark in enumerate(board):
            if mark == TttMark.o:
                score += POS_VALUES[i]
            elif mark == TttMark.x:
                score -= POS_VALUES[i]

        return score

    def get_ordered_moves(
        self, board: TttBoard, *, negate: bool = False
    ) -> list[TttMove]:
        """Get legal moves ordered by their potential effectiveness."""
        return sorted(
            board.legal_moves,
            key=lambda move: -POS_VALUES[move],
        )
