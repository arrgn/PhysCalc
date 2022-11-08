from pathlib import Path
from os import path


def path_to_file(filename: str) -> str:
    return path.join(Path(__file__).parent.resolve(), filename)


class User:
    def __init__(self, data=None):
        self._id = None
        self.name = None
        if data is not None:
            self._id = data[0]
            self.name = data[1]

    def set_user(self, data):
        self._id = data[0]
        self.name = data[1]

    def get_username(self):
        return self.name

    def get_user(self):
        return self._id, self.name


user = User()
