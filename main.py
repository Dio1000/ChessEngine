import argparse
import os
from engine import ChessEngine
from engine_server import ChessEngineServer, StockfishEngineWrapper


def main():
    parser = argparse.ArgumentParser(description='Chess Engine Server')
    parser.add_argument('--mode', choices=['stockfish', 'train', 'pretrained'],
                        default='stockfish', help='Engine mode')
    parser.add_argument('--pgn', default='games.pgn', help='Path to PGN file for training')
    parser.add_argument('--model-path', default='chess_model.joblib', help='Path to save/load the model')
    args = parser.parse_args()

    if args.mode == 'stockfish':
        engine = StockfishEngineWrapper()

    elif args.mode == 'train':
        if not os.path.exists(args.pgn):
            raise FileNotFoundError(f"PGN file not found: {args.pgn}")

        engine = ChessEngine()
        engine.train_model(args.pgn, save_path=args.model_path)
        print("Training complete. Starting server with trained model...")

    elif args.mode == 'pretrained':
        engine = ChessEngine()
        engine.load_model(args.model_path)

    server = ChessEngineServer('localhost', 12345)
    server.engine = engine
    server.start()


if __name__ == "__main__":
    main()
