# Chess Engine

## About the Project
This project provides a chess engine that integrates with the [ChessEd](https://github.com/Dio1000/ChessEd) application. It allows users to play against Stockfish, train a custom engine using PGN game files, or load a pretrained model for AI gameplay.

## Features

### ChessEd Interoperability
- **Java-Python Communication**: Implements a TCP socket interface for real-time data exchange between the ChessEd GUI and the Python engine.
- **FEN Parsing**: Decodes Forsyth-Edwards Notation to interpret board positions from ChessEd.

### AI Gameplay Options
- **Stockfish Integration**: Run Stockfish, one of the strongest chess engines, out of the box.
- **Trainable AI**: Train your own model using PGN game datasets and play against it.
- **Pretrained Model Support**: Load an existing trained model for customized AI performance.

## Prerequisites

Ensure you have the following installed:

1. **[ChessEd](https://github.com/Dio1000/ChessEd)**: Required for the GUI interface.
2. **Python 3.8+**: Core engine and model logic.
3. **Stockfish Binary**: Download from [stockfishchess.org](https://stockfishchess.org/download/). Set its path in `stockfish_helper.py`.

Install required packages:
```bash
pip install python-chess stockfish joblib scikit-learn
```

## Usage

### 1. Clone the Repository
```bash
git clone https://github.com/Dio1000/ChessEngine.git
cd ChessEngine
```

### 2. Configure Stockfish Path
Ensure `stockfish_helper.py` correctly points to your Stockfish binary.

### 3. Start the Server

#### A. Run with Stockfish
```bash
python main.py --mode stockfish
```

#### B. Train a New Model
```bash
python main.py --mode train --pgn path/to/games.pgn
```

#### C. Use a Pretrained Model
```bash
python main.py --mode pretrained --model-path path/to/chess_model.joblib
```

The server listens on `localhost:12345` and awaits connections from the ChessEd client.

### 4. Run ChessEd
Start the ChessEd client as described in its [README](https://github.com/Dio1000/ChessEd). It connects to this engine using TCP and sends FEN positions.

### 5. Play or Train
- Play against a strong AI (Stockfish or trained model).
- Analyze moves using the engine backend.

## Troubleshooting

- **Model Not Found**: Ensure paths are correct for `.pgn` or `.joblib` files.
- **Stockfish Not Found**: Check `stockfish_helper.py` and binary permissions.
- **Socket Issues**: Make sure no other app is using port `12345`.

## Contact

Email: [sandru.darian@gmail.com](mailto:sandru.darian@gmail.com)  

ChessEd: [https://github.com/Dio1000/ChessEd](https://github.com/Dio1000/ChessEd)  
Chess Engine: [https://github.com/Dio1000/ChessEngine](https://github.com/Dio1000/ChessEngine)
