from os.path import basename
from PyQt5 import Qt, uic
from PyQt5.QtCore import Qt as Qt2
from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from path_module import path_to_file, path_to_userdata, copy_file
from config import user
from loggers import logger


class ProfileWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.username = QLineEdit()
        self.change_btn = QPushButton()
        self.browse = QPushButton()
        self.restore = QPushButton()
        self.error = QLabel()
        self.avatar = QLabel()

        self.init_ui()

    def init_ui(self):
        uic.loadUi(path_to_file("uis", "profile.ui"), self)

        self.username.setText(user.get_user())

        self.change_btn.clicked.connect(self.change_username)
        self.browse.clicked.connect(self.browse_files)
        self.restore.clicked.connect(self.restore_avatar)

        self.load_avatar()

        ssh_file = path_to_file("themes", "SpyBot.qss")
        with open(ssh_file, "r") as fh:
            self.setStyleSheet(fh.read())
        self.show()

    def change_username(self):
        new_name = self.username.text()
        if new_name == user.get_user():
            return
        res = user.change_username(new_name)
        if not res:
            self.error.setText(f"Can't change name to {new_name}.")
            return
        self.error.setText(f"Name was successfully changed to {new_name}.")

    def browse_files(self):
        file_name = QFileDialog.getOpenFileName(self, "Open file", path_to_userdata("", str(user.get_user_id())),
                                                "Image (*.png *.jpg)")[0]
        if file_name == "":
            logger.warning("Got null filename")
            return
        copy_file(file_name, str(user.get_user_id()))
        user.change_avatar(basename(file_name))
        self.load_avatar()

    def restore_avatar(self):
        user.change_avatar()
        self.load_avatar()

    def load_avatar(self):
        path_to_avatar = user.get_avatar()
        if path_to_avatar:
            smaller_pixmap = QPixmap(path_to_avatar).scaled(64, 64, Qt2.KeepAspectRatio, Qt2.FastTransformation)
            self.avatar.setPixmap(smaller_pixmap)
        else:
            logger.warning("Path doesnt exist!")


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = ProfileWindow()
    app.exec()
