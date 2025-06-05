"""Main entry point for the checkers game."""

import argparse

import uvicorn
from draughts import Server, get_board

from ai_project.checkers.engine import CheckersEngine

parser = argparse.ArgumentParser(
    description="Checkers AI", formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "-d",
    "--difficulty",
    type=int,
    choices=range(1, 6),
    default=3,
    help="Difficulty level of the AI (1-5)",
)
parser.add_argument(
    "-r",
    "--randomness",
    type=float,
    default=0.0,
    help="Randomness percentage for AI moves (0-100)",
    metavar="PERCENTAGE",
)
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
args = parser.parse_args()

engine = CheckersEngine(
    depth=args.difficulty, randomness=args.randomness, debug=args.debug
)
board = get_board("american")
server = Server(board=board, get_best_move_method=engine.get_best_move)


def main():
    """Main function to run the checkers server."""
    uvicorn.run("ai_project.checkers.main:server.APP", reload=True)
