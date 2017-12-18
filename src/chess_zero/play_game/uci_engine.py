import chess
import chess.uci
import chess.variant

class UciEngine:
    def __init__(self):
        self.engine = chess.uci.popen_engine("/Users/alexanderlenhardt/src/github.com/chess-alpha-zero/stockfish")
        self.engine.uci()
        self.engine.setoption({"UCI_Variant": "horde"})
        self.board = chess.variant.HordeBoard()
        self.info_handler = chess.uci.InfoHandler()
        self.engine.info_handlers.append(self.info_handler)

    def start_game(self, human_is_black):
        self.human_color = chess.BLACK if human_is_black else chess.WHITE
        self.engine.ucinewgame()
        self.engine.position(chess.variant.HordeBoard())

    def update_position(self, board):
        self.board = board
        self.engine.position(board)

    def best_move(self, thinking_time_ms=400):
        move = self.engine.go(movetime=thinking_time_ms)
        return move[0].uci()

    def score(self):
        return self.info_handler.info["score"][1]