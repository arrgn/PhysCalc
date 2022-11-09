from pathlib import Path
from os import path


def path_to_file(filename: str) -> str:
    return path.join(Path(__file__).parent.resolve(), filename)


def path_to_userdata(filename: str, username: str) -> str:
    return path.join(Path(__file__).parent.resolve(), "userdata", username, filename)
