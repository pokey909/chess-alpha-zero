from logging import getLogger

from chess_zero.agent.player_chess import HistoryItem
from chess_zero.agent.player_chess import ChessPlayer
from chess_zero.config import Config
from chess_zero.lib.model_helper import load_best_model_weight
from chess_zero.play_game.uci_engine import UciEngine
import chess
import sys

logger = getLogger(__name__)


class PlayWithHuman:
    def __init__(self, config: Config):
        self.config = config
        self.human_color = None
        self.observers = []
        self.model = self._load_model()
        self.ai = None  # type: ChessPlayer
        self.last_evaluation = None
        self.last_history = None  # type: HistoryItem

    def start_game(self, human_is_black):
        self.human_color = chess.BLACK if human_is_black else chess.WHITE
        self.ai = ChessPlayer(self.config, self.model)

    def _load_model(self):
        from chess_zero.agent.model_chess import ChessModel
        model = ChessModel(self.config)
        if not load_best_model_weight(model):
            raise RuntimeError("Best model not found!")
        return model

    def move_by_ai(self, env):
        if self.ai is None:
            self.ai = ChessPlayer(self.config, self.model)
        action = self.ai.action(env.observation)

        self.last_history = self.ai.ask_thought_about(env.observation)
        self.last_evaluation = self.last_history.values[self.last_history.action]
        logger.debug(f"Evaluation history by AI = {self.last_history}")
        logger.debug(f"Evaluation by AI = {self.last_evaluation}")

        return action

    def move_by_opponent(self, env):
        while True:
            try:
                move = input('\nEnter your move in UCI format (a1a2, b2b6, ...): ')
                if chess.Move.from_uci(move) in env.board.legal_moves:
                    return move
                else:
                    print("That is NOT a valid move :(.")
            except:
                print("Shutdown")
                sys.exit(0)

class PlayWithEngine:
    def __init__(self, config: Config):
        self.config = config
        self.engine_color = None
        self.engine = UciEngine()
        self.observers = []
        self.model = self._load_model()
        self.ai = None  # type: ChessPlayer
        self.last_evaluation = None
        self.last_history = None  # type: HistoryItem

    def start_game(self, engine_is_black):
        self.engine_color = chess.BLACK if engine_is_black else chess.WHITE
        self.engine.start_game(engine_is_black)
        self.ai = ChessPlayer(self.config, self.model)

    def _load_model(self):
        from chess_zero.agent.model_chess import ChessModel
        model = ChessModel(self.config)
        if not load_best_model_weight(model):
            raise RuntimeError("Best model not found!")
        return model

    def move_by_ai(self, env):
        if self.ai is None:
            self.ai = ChessPlayer(self.config, self.model)
        action = self.ai.action(env.observation)

        self.last_history = self.ai.ask_thought_about(env.observation)
        self.last_evaluation = self.last_history.values[self.last_history.action]
        logger.debug(f"Evaluation history by AI = {self.last_history}")
        logger.debug(f"Evaluation by AI = {self.last_evaluation}")

        return action

    def move_by_opponent(self, env):
        self.engine.update_position(env.board)
        action = self.engine.best_move()
        last_evaluation = self.engine.score()
        logger.debug(f"Evaluation by Stockfish = {last_evaluation}")

        return action
