"""Checkers game implementation using Tkinter for GUI."""

import tkinter as tk

"""
The code for the Checkers Board GUI was generated entirely by ChatGPT 4.1. This includes both the graphical elements and
the logic of the game.
"""


BOARD_SIZE = 8
SQUARE_SIZE = 60

P1_COLOR = "red"
P2_COLOR = "black"
KING_MARK = "gold"
SELECT_COLOR = "yellow"


class Piece:
    """Class representing a piece in the checkers game."""

    def __init__(self, player, king=False):
        """Initialize a piece with player number and king status."""
        self.player = player  # 1 or 2
        self.king = king


class CheckersGame:
    """Class representing the Checkers game logic and GUI."""

    def __init__(self, root):
        """Initialize the game with a Tkinter root window."""
        self.root = root
        self.root.title("Checkers")
        self.canvas = tk.Canvas(
            root, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE
        )
        self.canvas.pack()
        self.message = tk.Label(root, text="", font=("Arial", 16))
        self.message.pack()
        self.turn = 1
        self.selected = None
        self.valid_moves = {}
        self.board = self.init_board()
        self.update_valid_moves()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.handle_click)

    def init_board(self):
        """Initialize the checkers board with pieces in starting positions."""
        board: list[list[Piece | None]] = [
            [None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]
        for row in range(3):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = Piece(2)
        for row in range(BOARD_SIZE - 3, BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = Piece(1)
        return board

    def draw_board(self):
        """Draw the checkers board and pieces on the canvas."""
        self.canvas.delete("all")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = "grey" if (row + col) % 2 else "lightgrey"
                self.canvas.create_rectangle(
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    (col + 1) * SQUARE_SIZE,
                    (row + 1) * SQUARE_SIZE,
                    fill=color,
                )
                piece = self.board[row][col]
                if self.selected == (row, col):
                    self.canvas.create_rectangle(
                        col * SQUARE_SIZE,
                        row * SQUARE_SIZE,
                        (col + 1) * SQUARE_SIZE,
                        (row + 1) * SQUARE_SIZE,
                        fill=SELECT_COLOR,
                    )
                if piece:
                    self.canvas.create_oval(
                        col * SQUARE_SIZE + 10,
                        row * SQUARE_SIZE + 10,
                        (col + 1) * SQUARE_SIZE - 10,
                        (row + 1) * SQUARE_SIZE - 10,
                        fill=P1_COLOR if piece.player == 1 else P2_COLOR,
                    )
                    if piece.king:
                        self.canvas.create_oval(
                            col * SQUARE_SIZE + 20,
                            row * SQUARE_SIZE + 20,
                            (col + 1) * SQUARE_SIZE - 20,
                            (row + 1) * SQUARE_SIZE - 20,
                            fill=KING_MARK,
                        )

    def handle_click(self, event):
        """Handle mouse click events on the canvas."""
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return

        if self.selected:
            move = (row, col)
            if move in self.valid_moves.get(self.selected, []):
                self.make_move(self.selected, move)
                self.draw_board()
            self.selected = None
            self.update_valid_moves()
            self.draw_board()
        else:
            piece = self.board[row][col]
            if piece and piece.player == self.turn and self.valid_moves.get((row, col)):
                self.selected = (row, col)
                self.draw_board()

        self.show_status()

    def show_status(self):
        """Update the status message and check for game over."""
        if self.is_game_over():
            winner = "Red" if self.turn == 2 else "Black"
            self.message.config(text=f"Game Over! {winner} wins!")
            self.canvas.unbind("<Button-1>")
        else:
            self.message.config(text=f"{'Red' if self.turn == 1 else 'Black'}'s turn")

    def update_valid_moves(self):
        """Update the valid moves for the current player."""
        self.valid_moves = self.get_all_valid_moves(self.turn)

    def get_all_valid_moves(self, player):
        """Get all valid moves for a player."""
        moves = {}
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece.player == player:
                    steps = self.get_moves_for_piece(row, col, piece)
                    if steps:
                        moves[(row, col)] = steps
        return moves

    def get_moves_for_piece(self, row, col, piece):
        """Get all possible moves for a given piece."""
        # Directions for normal pieces (forward only), kings move in all four
        if piece.king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece.player == 1:
            directions = [(-1, -1), (-1, 1)]  # Player 1 moves up
        else:
            directions = [(1, -1), (1, 1)]  # Player 2 moves down

        moves = []
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            jump_row, jump_col = row + 2 * dr, col + 2 * dc
            # Simple move
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                if not self.board[new_row][new_col]:
                    moves.append((new_row, new_col))
            # Capture move
            if (
                0 <= jump_row < BOARD_SIZE
                and 0 <= jump_col < BOARD_SIZE
                and self.board[new_row][new_col]
                and self.board[new_row][new_col].player != piece.player
                and not self.board[jump_row][jump_col]
            ):
                moves.append((jump_row, jump_col))
        return moves

    def make_move(self, from_pos, to_pos):
        """Move a piece on the board."""
        fr, fc = from_pos
        tr, tc = to_pos
        piece = self.board[fr][fc]
        # Move piece
        self.board[tr][tc] = piece
        self.board[fr][fc] = None
        # Kinging
        if (piece.player == 1 and tr == 0) or (
            piece.player == 2 and tr == BOARD_SIZE - 1
        ):
            piece.king = True
        # Capture
        if abs(tr - fr) == 2:
            mid_row = (fr + tr) // 2
            mid_col = (fc + tc) // 2
            self.board[mid_row][mid_col] = None
        # Switch turn
        self.turn = 2 if self.turn == 1 else 1
        self.update_valid_moves()

    def is_game_over(self):
        """Check if the game is over."""
        return not self.valid_moves


if __name__ == "__main__":
    root = tk.Tk()
    game = CheckersGame(root)
    game.show_status()
    root.mainloop()
