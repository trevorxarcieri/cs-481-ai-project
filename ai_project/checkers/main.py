"""Main entry point for the checkers game."""

from draughts import Server, get_board

from ai_project.checkers.engine import CheckersEngine
from ai_project.utils import parse_args

args = parse_args()

engine = CheckersEngine(
    depth=args.difficulty, randomness=args.randomness, debug=args.debug
)
board = get_board("american")
server = Server(board=board, get_best_move_method=engine.get_best_move)


def main():
    """Main function to run the checkers server."""
    server.run()
