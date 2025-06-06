# CS-481 AI Project

This is the final project I made with my friend Demetri for my CS-481 AI class at Kettering Univeristy.

## Development Setup

### Prerequisites

- [Python](https://www.python.org/downloads/) 3.12 or later
- [Poetry](https://python-poetry.org/docs/) for Python package management

### Installing Dependencies

To install the project and its dependencies, run:

```bash
poetry install
```

### Running the Games

#### Checkers

To run the Checkers game, use the following command:

```bash
poetry run checkers
```

#### Tic-Tac-Toe

To run the Tic-Tac-Toe game, use the following command:

```bash
poetry run tic-tac-toe
```

#### Usage

```bash
usage: (checkers|tic-tac-toe) [-h] [-d {1,2,3,4,5}] [-r PERCENTAGE] [--debug]

AI Game Agent

options:
  -h, --help            show this help message and exit
  -d {1,2,3,4,5}, --difficulty {1,2,3,4,5}
                        Difficulty level of the AI (1-5) (default: 3)
  -r PERCENTAGE, --randomness PERCENTAGE
                        Randomness percentage for AI moves (0-100) (default: 0.0)
  --debug               Enable debug mode (default: False)

```
