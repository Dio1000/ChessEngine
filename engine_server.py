import socket
import threading
import chess


class ChessEngineServer:

    def __init__(self, host, port):
        HOST = 'localhost'
        PORT = 12345  # Change to whatever you would like

        self.host = HOST
        self.port = PORT
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
                data = client_socket.recv(1024).decode().strip()
                if not data:
                    break

                if data.startswith("FEN "):
                    fen = data[4:]

                    try:
                        move = self.get_best_move(fen)
                        client_socket.sendall(f"MOVE {move}\n".encode())
                    except Exception as e:
                        client_socket.sendall(f"ERROR {str(e)}\n".encode())
        finally:
            client_socket.close()

    def get_best_move(self, fen):
        board = chess.Board(fen)
        if board.is_game_over():
            raise ValueError("Game is already over")

        # TODO: Replace with actual ML model
        return str(list(board.legal_moves)[0])


if __name__ == "__main__":
    server = ChessEngineServer()
    server.start()
