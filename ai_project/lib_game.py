from draughts import Server, get_board
import numpy as np

get_best_mv = lambda board: np.random.choice(list(board.legal_moves))
server = Server(board=get_board("american"), get_best_move_method=get_best_mv)
server.run()
