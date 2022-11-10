from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame
from PyQt5 import QtCore, uic
from src.path_module import path_to_file


class SideMenu:
    def __init__(self, widget: QWidget, btn: QPushButton, path: str, width: int, duration: int, left: bool) -> None:
        self.menu = QFrame()
        self.btn = btn
        self.path = path
        self.duration = duration
        self.widget = widget
        self.width = width
        self.left = left
        self.animation = QPropertyAnimation()

        self.init_ui()

    def init_ui(self):
        self.menu = QFrame(self.widget)
        uic.loadUi(path_to_file(self.path), self.menu)

        self.menu.closer.clicked.connect(self.close)
        self.animation = QPropertyAnimation(self.menu, b"size", self.widget.ui)
        self.update_animation()
        self.animation.setDuration(self.duration)

    def show_hide_menu(self):
        if self.btn.isChecked():
            self.btn.hide()
            self.animation.setDirection(QtCore.QAbstractAnimation.Forward)
        else:

            self.animation.setDirection(QtCore.QAbstractAnimation.Backward)
            self.btn.show()
        self.animation.start()

    def resize_event(self):
        self.update_animation()

    def update_animation(self):
        if self.left:
            self.menu.setGeometry(QtCore.QRect(0, 0, self.width, self.widget.height()))
        else:
            self.menu.setGeometry(QtCore.QRect(self.widget.width() - self.width,
                                               0, self.width, self.widget.height()))
        if not self.btn.isChecked():
            self.menu.resize(QtCore.QSize(0, 0))
        self.animation.setStartValue(QtCore.QSize(self.width, 0))
        self.animation.setEndValue(QtCore.QSize(self.width, self.widget.height()))

    def close(self):
        self.btn.setChecked(False)
        self.show_hide_menu()
