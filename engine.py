import chess
import chess.pgn
import joblib
from sklearn.ensemble import RandomForestClassifier
import os


class ChessEngine:
    def __init__(self):
        self.model = None

    def load_model(self, model_path="chess_model.joblib"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        self.model = joblib.load(model_path)

    def train_model(self, pgn_path, save_path="chess_model.joblib", max_games=1000):
        games = []
        with open(pgn_path, encoding="utf-8") as pgn:
            while len(games) < max_games:
                try:
                    game = chess.pgn.read_game(pgn)
                    if not game:
                        break
                    if ("Result" in game.headers and
                            "WhiteElo" in game.headers and
                            "BlackElo" in game.headers):
                        games.append(game)
                except Exception as e:
                    print(f"Skipping corrupt game: {e}")
                    continue

        if not games:
            raise ValueError("No valid games found in PGN file")

        X, y = [], []
        for game in games:
            try:
                board = game.board()
                result = game.headers["Result"]

                if result == "1-0":
                    label = 1
                elif result == "0-1":
                    label = 0
                else:
                    continue

                for ply, move in enumerate(game.mainline_moves()):
                    board.push(move)
                    if ply < 10:
                        continue

                    X.append(self._extract_features(board))
                    y.append(label)

            except Exception as e:
                print(f"Skipping corrupt game segment: {e}")
                continue

        if not X:
            raise ValueError("No valid training positions found")

        print(f"Training on {len(X)} positions...")
        self.model = RandomForestClassifier(n_estimators=100, max_depth=5)
        self.model.fit(X, y)
        joblib.dump(self.model, save_path)
        print(f"Model saved to {save_path}")

    def _extract_features(self, board):
        material = self._calculate_material(board)
        return [
            material,
            int(board.has_kingside_castling_rights(chess.WHITE)),
            int(board.has_queenside_castling_rights(chess.WHITE)),
            int(board.has_kingside_castling_rights(chess.BLACK)),
            int(board.has_queenside_castling_rights(chess.BLACK)),
            int(board.is_check()),
            len(list(board.legal_moves))
        ]

    def _calculate_material(self, board):
        piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9}
        material_white = sum(piece_values.get(p.symbol().upper(), 0)
                             for p in board.piece_map().values() if p.color)
        material_black = sum(piece_values.get(p.symbol().upper(), 0)
                             for p in board.piece_map().values() if not p.color)
        return material_white - material_black

    def get_best_move(self, fen):
        if self.model is None:
            self.load_model()

        board = chess.Board(fen)
        best_move = None
        best_score = -float("inf")

        for move in board.legal_moves:
            board.push(move)
            features = [self._extract_features(board)]
            probes = self.model.predict_proba(features)[0]
            score = probes[1] if len(probes) > 1 else probes[0]
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

        if best_move is None:
            best_move = next(iter(board.legal_moves))

        is_check = board.is_check()
        board.push(best_move)
        is_checkmate = board.is_checkmate()
        board.pop()

        return {
            'move': best_move.uci(),
            'is_check': is_check,
            'is_checkmate': is_checkmate
        }
