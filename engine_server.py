import socket
import threading
import chess
from stockfish import Stockfish
import stockfish_helper


HOST = 'localhost'
PORT = 12345


class StockfishEngineWrapper:
    def __init__(self):
        self.stockfish = Stockfish(path=stockfish_helper.get_stockfish_path())
        self.board = chess.Board()

    def get_best_move(self, fen):
        self.board.set_fen(fen)
        self.stockfish.set_fen_position(fen)

        move = self.stockfish.get_best_move()
        if move is None:
            raise ValueError("Stockfish did not return a move.")

        is_current_check = self.board.is_check()
        self.board.push(chess.Move.from_uci(move))
        will_be_checkmate = self.board.is_checkmate()
        self.board.pop()

        return {
            'move': move,
            'is_check': is_current_check,
            'is_checkmate': will_be_checkmate
        }


class ChessEngineServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.engine = None

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, _ = self.server_socket.accept()
            print(f"Client connected from: {client_socket}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
                if not data:
                    break

                if data.startswith("FEN "):
                    fen = data[4:]
                    print(f"[Server] Received FEN: {fen}")

                    board = chess.Board(fen)
                    # The engine assumes the player is playing as white.
                    if board.turn == chess.WHITE:
                        continue
                    try:
                        move_data = self.engine.get_best_move(fen)
                        if move_data:
                            response = f"MOVE {move_data['move']} CHECK {int(move_data['is_check'])} MATE {int(move_data['is_checkmate'])}\n"
                            print(f"[Server] Sending response: {response.strip()}")
                            client_socket.sendall(response.encode())
                    except Exception as e:
                        error_msg = f"ERROR {str(e)}\n"
                        print(f"Server Error: {e}")
                        client_socket.sendall(error_msg.encode())
        finally:
            print("Client disconnected.")
            client_socket.close()
