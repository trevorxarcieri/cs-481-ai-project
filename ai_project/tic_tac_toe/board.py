"""Tic-tac-toe board representation."""

from collections.abc import Generator
from enum import Enum, IntEnum

from ai_project.engine import AbstractBoard, AbstractPlayer

type TttMove = int


class TttMark(str, Enum):
    """Enum for tic-tac-toe marks."""

    x = "X"
    o = "O"
    blank = " "


class TttPlayer(IntEnum):
    """Enum for tic-tac-toe players."""

    x = 1
    o = -1

    def __str__(self):
        """Return the string representation of the player."""
        return self.name.upper()


WINNING_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


class TttBoard(AbstractBoard[TttMove]):
    """Class for tic-tac-toe board representation."""

    def __init__(self):
        """Initialize the tic-tac-toe board."""
        self._stack = []
        self._board = [
            TttMark.blank for _ in range(9)
        ]  # 3x3 board represented as a flat list
        self.turn = AbstractPlayer(TttPlayer.x)

    def __str__(self):
        """Return a string representation of the board."""
        return "\n".join([
            " | ".join(self._board[i : i + 3])
            + "   "
            + " | ".join(map(str, range(i, i + 3)))
            for i in range(0, 9, 3)
        ])

    def __getitem__(self, item: TttMove) -> TttMark:
        """Get the mark at the specified position."""
        return self._board[item]

    def __setitem__(self, key: TttMove, value: TttMark) -> None:
        """Set the mark at the specified position."""
        self._board[key] = value

    def __iter__(self):
        """Iterate over the board marks."""
        return iter(self._board)

    def reset(self) -> None:
        """Reset the board to its initial state."""
        self.__init__()

    @property
    def legal_moves(self) -> Generator[TttMove, None, None]:
        """All legal moves for the current player."""
        for i, s in enumerate(self._board):
            if s == TttMark.blank:
                yield i

    @property
    def is_draw(self) -> bool:
        """Check if the game is a draw."""
        return not list(self.legal_moves) and not self.is_win_loss

    @property
    def is_win_loss(self) -> bool:
        """Check if the game is a win or loss."""
        for line in WINNING_LINES:
            if (
                self._board[line[0]]
                == self._board[line[1]]
                == self._board[line[2]]
                != TttMark.blank
            ):
                return True
        return False

    @property
    def game_over(self) -> bool:
        """Returns `True` if the game is over."""
        return self.is_draw or self.is_win_loss

    def push(self, move: TttMove) -> None:
        """Apply a move to the board."""
        self._board[move] = TttMark.x if self.turn == TttPlayer.x else TttMark.o
        self.turn = AbstractPlayer(-self.turn.value)
        self._stack.append(move)

    def pop(self) -> None:
        """Undo the last move applied to the board."""
        move = self._stack.pop()
        self.turn = AbstractPlayer(-self.turn.value)
        self._board[move] = TttMark.blank
