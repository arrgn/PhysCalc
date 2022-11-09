from PyQt5 import Qt, uic
from PyQt5.QtCore import Qt as Qt2
from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap
from path_module import path_to_file
from config import user


class ProfileWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.username = QLineEdit()
        self.change_btn = QPushButton()
        self.error = QLabel()
        self.avatar = QLabel()

        self.init_ui()

    def init_ui(self):
        uic.loadUi(path_to_file("profile.ui"), self)

        self.username.setText(user.get_user())

        self.change_btn.clicked.connect(self.change_username)

        path_to_avatar = user.get_avatar()
        if path_to_avatar:
            smaller_pixmap = QPixmap(path_to_avatar).scaled(64, 64, Qt2.KeepAspectRatio, Qt2.FastTransformation)
            self.avatar.setPixmap(smaller_pixmap)

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


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = ProfileWindow()
    app.exec()
