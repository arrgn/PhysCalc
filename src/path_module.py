import shutil
from pathlib import Path
from os import path, makedirs
from os.path import basename


def path_to_file(filename: str) -> str:
    return path.join(Path(__file__).parent.resolve(), filename)


def path_to_userdata(filename: str, username: str) -> str:
    return path.join(Path(__file__).parent.resolve(), "userdata", username, filename)


def copy_file(src, username):
    try:
        shutil.copy(src, path_to_userdata(basename(src), username))
    except shutil.SameFileError as e:
        print(e)


def create_dir(username):
    try:
        makedirs(path_to_userdata("", username))
    except FileExistsError as e:
        print(e)
