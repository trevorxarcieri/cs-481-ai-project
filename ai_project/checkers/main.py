"""Main entry point for the checkers game."""

import uvicorn
from draughts import Server, get_board

from ai_project.checkers.engine import CheckersEngine

engine = CheckersEngine(depth=3)
board = get_board("american")
server = Server(board=board, get_best_move_method=engine.get_best_move)


def main():
    """Main function to run the checkers server."""
    uvicorn.run("ai_project.checkers.main:server.APP", reload=True)
