from pathlib import Path
from os import path


def path_to_file(filename: str) -> str:
    return path.join(Path(__file__).parent.resolve(), filename)
