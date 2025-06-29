"""Main entry point for the tic-tac-toe game.

Authors: Trevor Arcieri and Demetri Karras
Course: CS 481 Artificial Intelligence
Term: Spring 2025
Project: DualBoard Negamax AI
"""

import random

from ai_project.tic_tac_toe.board import TttBoard, TttPlayer
from ai_project.tic_tac_toe.engine import TttEngine
from ai_project.utils import parse_args

args = parse_args()

board = TttBoard()
engine = TttEngine(
    depth=args.difficulty * 2, randomness=args.randomness, debug=args.debug
)


def handle_game_over(board: TttBoard) -> None:
    """Handle the end of the game."""
    if board.is_win_loss:
        print(f"Game over. Winner: {TttPlayer(-board.turn.value)}!")
    else:
        print("Game over. It's a draw!")
    board.reset()
    print(board)


def get_user_choice() -> str:
    """Get user choice for the next action."""
    while True:
        choice = input(
            "Type 'm' to make a move, 'e' to make the engine move, 'u' to undo the last move, 'a' for auto play, or 'r' for a random position: "
        )
        if choice in ["m", "e", "u", "a", "r"]:
            return choice
        print("Invalid choice. Please try again.")


def get_move_input() -> int:
    """Get a valid move input from the user."""
    while True:
        try:
            move = int(input("Enter your move (0-8): "))
            if move not in board.legal_moves:
                raise ValueError("Invalid move")
            break
        except ValueError as e:
            print(f"Error: {e}. Please try again.")
    return move


def handle_user_choice(choice: str) -> None:
    """Handle the user choice for the next action."""
    match choice:
        case "m":
            move = get_move_input()
            board.push(move)
        case "e":
            move = engine.get_best_move(board)
            print(f"Engine chose move: {move}")
            board.push(move)
        case "u":
            try:
                board.pop()
                print("Last move undone.")
            except IndexError:
                print("No moves to undo.")
        case "a":
            while not board.game_over:
                print(board)
                print(f"Current turn: {TttPlayer(board.turn.value)}")
                move = engine.get_best_move(board)
                print(f"Engine chose move: {move}")
                board.push(move)
        case "r":
            board.reset()
            num_moves = random.randint(1, 7)
            for _ in range(num_moves):
                if board.game_over:
                    break
                move = random.choice(list(board.legal_moves))
                board.push(move)


def main():
    """Main function to run the tic-tac-toe server."""
    while True:
        print(board)

        if board.game_over:
            handle_game_over(board)

        print(f"Current turn: {TttPlayer(board.turn.value)}")
        try:
            handle_user_choice(get_user_choice())
        except KeyboardInterrupt:
            print("\nGame interrupted. Exiting...")
            break
