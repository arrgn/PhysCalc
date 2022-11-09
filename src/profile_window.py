from PyQt5 import Qt, uic
from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QLabel

from path_module import path_to_file
from config import user


class ProfileWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.username = QLineEdit()
        self.change_btn = QPushButton()
        self.error = QLabel()

        self.init_ui()

    def init_ui(self):
        uic.loadUi(path_to_file("profile.ui"), self)

        self.username.setText(user.get_user())

        self.change_btn.clicked.connect(self.change_username)

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
