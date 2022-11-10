import shutil
from pathlib import Path
from os import path, makedirs
from os.path import basename
from logging import getLogger


def path_to_file(filename: str) -> str:
    return path.join(Path(__file__).parent.resolve(), filename)


def path_to_userdata(filename: str, username: str) -> str:
    return path.join(Path(__file__).parent.resolve(), "userdata", username, filename)


def copy_file(src, username):
    try:
        shutil.copy(src, path_to_userdata(basename(src), username))
    except shutil.SameFileError:
        getLogger(__name__).exception("Tracked exception occurred!")
    except Exception:
        getLogger(__name__).exception("Abnormal exception occurred!")


def create_user_dir(username):
    try:
        makedirs(path_to_userdata("", username))
    except FileExistsError:
        getLogger(__name__).exception("Tracked exception occurred!")
    except Exception:
        getLogger(__name__).exception("Abnormal exception occurred!")


def create_dir(dirname):
    try:
        makedirs(path_to_file(dirname))
    except FileExistsError:
        getLogger(__name__).exception("Tracked exception occurred!")
    except Exception:
        getLogger(__name__).exception("Abnormal exception occurred!")
