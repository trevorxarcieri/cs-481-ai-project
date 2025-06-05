"""Utilities for the AI project."""

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedArgs:
    """Class to hold parsed command line arguments.

    Attributes:
        difficulty (int): Difficulty level of the AI (1-5).
        randomness (float): Randomness percentage for AI moves (0-100).
        debug (bool): Enable debug mode.
    """

    difficulty: int
    randomness: float
    debug: bool


def parse_args() -> ParsedArgs:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AI Game Agent",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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
    return ParsedArgs(
        difficulty=args.difficulty,
        randomness=args.randomness,
        debug=args.debug,
    )
