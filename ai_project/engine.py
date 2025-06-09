"""Abstract base class for an AI engine using Negamax and Alpha-Beta Pruning.

Authors: Trevor Arcieri and Demetri Karras
Course: CS 481 Artificial Intelligence
Term: Spring 2025
Project: DualBoard Negamax AI
"""

import random
from abc import ABC, abstractmethod
from math import inf
from typing import Generic, TypeVar

from ai_project.board import AbstractBoard, AbstractPlayer, MoveT

BoardT = TypeVar("BoardT", bound="AbstractBoard")


class AbstractEngine(ABC, Generic[BoardT, MoveT]):
    """Abstract base class for an AI engine using Negamax and Alpha-Beta Pruning."""

    def __init__(
        self, depth: int, *, randomness: float = 0.0, debug: bool = False
    ) -> None:
        """Initialize the engine with a search depth."""
        if not 0 <= randomness <= 100:
            raise ValueError("randomness must be in 0...100")

        self.depth = depth
        self._p_random = randomness / 100
        self._rng = random.Random()
        self._dbg = debug

    def terminal_score(self, board: BoardT) -> float:
        """Return a terminal score for the board state.

        Args:
            board (AbstractBoard): The current board state.

        Returns:
            float: Terminal score for the board.
        """
        if board.is_draw:
            return 0
        return -inf  # side to move has lost since it has no legal moves

    @abstractmethod
    def evaluate(self, board: BoardT) -> int:
        """Evaluate the board state.

        Args:
            board (AbstractBoard): The current board state.

        Returns:
            int: Evaluation score for the board.
        """
        pass

    @abstractmethod
    def get_ordered_moves(
        self, board: BoardT, *, is_min_turn: bool = False
    ) -> list[MoveT]:
        """Get legal moves ordered by their potential effectiveness.

        Args:
            board (AbstractBoard): The current board state.
            is_min_turn (bool): Whether it is the minimizing player's turn.

        Returns:
            list[Any]: List of legal moves ordered by effectiveness.
        """
        pass

    def alpha_beta(
        self,
        board: BoardT,
        depth: int,
        alpha: float,
        beta: float,
        *,
        is_min_turn: bool = False,
    ) -> float:
        """Perform Alpha-Beta pruning to find the best move.

        Args:
            board (AbstractBoard): The current board state.
            depth (int): The current search depth.
            alpha (float): The best score for the maximizing player.
            beta (float): The best score for the minimizing player.
            is_min_turn (bool): Whether it is the minimizing player's turn.

        Returns:
            float: The evaluation score for the board.
        """
        if board.game_over:
            return self.terminal_score(board)

        if depth == 0:
            return (1 if is_min_turn else -1) * self.evaluate(board)

        best = -inf
        for move in self.get_ordered_moves(board, is_min_turn=is_min_turn):
            board.push(move)  # make move
            val = -self.alpha_beta(
                board, depth - 1, -beta, -alpha, is_min_turn=not is_min_turn
            )  # recurse and negate
            board.pop()  # undo move

            best = max(best, val)
            alpha = max(alpha, val)
            if alpha >= beta:  # beta cutoff
                break

        return best

    def _maybe_random_root_move(self, board: BoardT) -> MoveT | None:
        """With probability p_random, return a random legal move, else None."""
        if self._p_random and self._rng.random() < self._p_random:
            return self._rng.choice(list(board.legal_moves))
        return None

    def get_best_move(self, board: BoardT) -> MoveT:
        """Get the best move for the current board state using **Negamax**.

        Args:
            board (AbstractBoard[Move]): The current board state.

        Returns:
            Move: The best move for the current player.
        """
        # Probabilistically return a random move, similar to epsilon-greedy strategy used in reinforcement learning.
        rnd = self._maybe_random_root_move(board)
        if rnd is not None:
            return rnd

        best_move = None
        alpha = -inf

        is_min_turn = board.turn.value == AbstractPlayer.MIN

        for move in self.get_ordered_moves(board, is_min_turn=is_min_turn):
            board.push(move)  # make move
            move_value = -self.alpha_beta(
                board,
                self.depth - 1,
                -inf,
                -alpha,
                is_min_turn=not is_min_turn,
            )  # recurse and negate
            board.pop()  # undo move

            if move_value > alpha:
                alpha = move_value
                best_move = move

            if self._dbg:
                print(f"Evaluated move: {move}, Value: {move_value}")

        if best_move is None:
            if list(board.legal_moves):
                return self.get_ordered_moves(board)[
                    0
                ]  # fallback to the first legal move
            raise ValueError("No valid moves found")

        if self._dbg:
            print(f"Turn: {board.turn}, Best move: {best_move}, Alpha: {alpha}")
        return best_move
