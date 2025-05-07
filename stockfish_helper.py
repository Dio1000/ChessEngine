from stockfish import Stockfish
import platform
import subprocess


def get_stockfish_path():
    system = platform.system()

    # Windows
    if system == "Windows":
        try:
            from stockfish import Stockfish as SF
            return SF().path  # Auto-detects if installed via pip
        except:
            raise Exception("Stockfish not installed. Run: pip install stockfish")

    # MacOS/Linux - Check common paths
    common_paths = [
        "/usr/local/bin/stockfish",  # MacOS Homebrew
        "/usr/games/stockfish",  # Linux apt
        "/usr/bin/stockfish",  # Some Linux
        "stockfish"  # If in PATH
    ]

    for path in common_paths:
        try:
            # Verify the binary works
            subprocess.run([path, "--version"],
                           check=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
            return path
        except:
            continue

    raise FileNotFoundError(
        "Stockfish not found. Install it:\n"
        "MacOS: brew install stockfish\n"
        "Linux: sudo apt install stockfish\n"
        "Windows: pip install stockfish"
    )


