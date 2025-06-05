"""Main entry point for the checkers game."""

import numpy as np
from draughts import Server, get_board


def main():
    """Main function to run the checkers server."""

    def get_best_mv(board):
        return np.random.choice(list(board.legal_moves))

    server = Server(board=get_board("american"), get_best_move_method=get_best_mv)
    # engine = AlphaBetaEngine(depth=3)
    # board = get_board("american")
    # server = Server(board=board, get_best_move_method=engine.get_best_move)
    server.run()
