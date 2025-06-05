"""Abstract board representation."""

from abc import ABC, abstractmethod
from collections.abc import Generator
from enum import Enum
from typing import Generic, TypeVar

MoveT = TypeVar("MoveT")


class AbstractPlayer(Enum):
    """Enum for players."""

    MAX = 1
    MIN = -1


class AbstractBoard(ABC, Generic[MoveT]):
    """Abstract base class for a board."""

    turn: AbstractPlayer

    @property
    @abstractmethod
    def legal_moves(self) -> Generator[MoveT, None, None]:
        """All legal moves for the current player."""
        pass

    @property
    @abstractmethod
    def is_draw(self) -> bool:
        """Check if the game is a draw."""
        pass

    @property
    def game_over(self) -> bool:
        """Returns ``True`` if the game is over."""
        return self.is_draw or not bool(list(self.legal_moves))

    @abstractmethod
    def push(self, move: MoveT) -> None:
        """Apply a move to the board."""
        pass

    @abstractmethod
    def pop(self) -> None:
        """Undo the last move applied to the board."""
        pass
