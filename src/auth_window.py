from PyQt5 import Qt, uic
from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QLabel

from path_module import path_to_file
from config import user


class AuthWindow(QDialog):
    def __init__(self, is_login: bool):
        super().__init__()
        self.is_login = is_login
        self.auth_btn = QPushButton()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.error = QLabel()

        self.init_ui()

    def init_ui(self):
        uic.loadUi(path_to_file("auth_window.ui"), self)
        if self.is_login:
            self.auth_btn.setText("Sign In")
            self.auth_btn.clicked.connect(self.login)
        else:
            self.auth_btn.clicked.connect(self.register)
        ssh_file = path_to_file("themes", "SpyBot.qss")
        with open(ssh_file, "r") as fh:
            self.setStyleSheet(fh.read())
        self.show()

    def register(self):
        name = self.username.text()
        password = self.password.text()
        res = user.add_user(name, password)
        if not res:
            self.error.setText(f"User with name {name} exists!")
            return
        self.error.setText(f"User {name} created. Successfully sign in via user {name}.")

    def login(self):
        name = self.username.text()
        password = self.password.text()
        res = user.set_user(name, password)
        if not res:
            self.error.setText(f"Can't sig in via {name}!")
            return
        self.error.setText(f"Successfully sign in via user {name}.")


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = AuthWindow(True)
    app.exec()
