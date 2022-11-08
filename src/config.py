from pathlib import Path
from os import path


def path_to_file(filename: str) -> str:
    return path.join(Path(__file__).parent.resolve(), filename)


path_to_db = "db.db"


class User:
    class UserOrPassIsIncorrectError(Exception):
        pass

    def __init__(self, data=None, dao=None) -> None:
        self._id = None
        self.name = None
        self.dao = None
        if data is not None:
            self._id = data[0]
            self.name = data[1]
            self.dao = dao

    def set_user(self, data: tuple[int, str, str]) -> None:
        if self.dao.get_checked_user(data[1], data[2]):
            self._id = data[0]
            self.name = data[1]
        else:
            raise self.UserOrPassIsIncorrectError(f"Cannt authorize under user {data[1]}")

    def get_username(self) -> str:
        return self.name

    def get_user(self) -> str:
        return self._id, self.name


user = User()
