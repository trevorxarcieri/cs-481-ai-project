"""Tic-tac-toe AI engine using Negamax and Alpha-Beta Pruning."""

from ai_project.engine import AbstractEngine
from ai_project.tic_tac_toe.board import WINNING_LINES, TttBoard, TttMark, TttMove

NUM_MARKS_VALUES = [
    0,
    10,
    100,
]  # Values for no marks, one mark, and two marks in a line
POS_PRI = [
    3,
    2,
    3,
    2,
    1,
    2,
    3,
    2,
    3,
]  # Priority for each position in the board, corners > edges > center


class TttEngine(AbstractEngine[TttBoard, TttMove]):
    """Class for the Tic-tac-toe AI engine using Negamax and Alpha-Beta Pruning."""

    def evaluate(self, board: TttBoard) -> int:
        """Evaluate the board state."""
        score = 0

        # Add to score based on number of marks in winning lines
        for line in WINNING_LINES:
            line_str = "".join(board[i] for i in line)
            num_o = line_str.count(TttMark.o)
            num_x = line_str.count(TttMark.x)
            if num_x == 0:
                score += NUM_MARKS_VALUES[num_o]
            if num_o == 0:
                score -= NUM_MARKS_VALUES[num_x]

        return score

    def get_ordered_moves(
        self, board: TttBoard, *, is_min_turn: bool = False
    ) -> list[TttMove]:
        """Get legal moves ordered by their potential effectiveness."""
        return sorted(
            board.legal_moves,
            key=lambda move: -POS_PRI[move],
        )
