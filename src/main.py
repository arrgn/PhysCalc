from PyQt5 import Qt, QtCore, uic
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QStackedWidget, QPushButton, QWidget, QFrame, QGridLayout
from ballistic import BallisticWindow
from calcs import CalcsWindow
from path_module import path_to_file


class Window(QWidget):
    class SideMenu():
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

        def resizeEvent(self):
            self.update_animation()

        def update_animation(self):
            if self.left:
                self.menu.setGeometry(QtCore.QRect(0, 0, self.width, self.widget.height()))
            else:
                self.menu.setGeometry(QtCore.QRect(self.widget.width() - self.width,
                                                   0, self.width, self.widget.height()))
            if not self.btn.isChecked():
                self.menu.resize(QtCore.QSize(0, 0))
            self.animation.setStartValue(QtCore.QSize(0, self.widget.height()))
            self.animation.setEndValue(QtCore.QSize(self.width, self.widget.height()))

    def __init__(self):
        super().__init__()
        self.ui = QStackedWidget()
        self.layout_ = QGridLayout()
        self.drop_menu = None
        self.auth_menu = None
        self.drop_btn = QPushButton()
        self.auth_btn = QPushButton()
        self.animation = QPropertyAnimation()
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.layout_)
        self.layout_.addWidget(self.ui)

        self.setGeometry(0, 0, 640, 640)
        self.ui.setGeometry(0, 0, 640, 640)
        self.ui.addWidget(BallisticWindow().ui)
        self.ui.addWidget(CalcsWindow().ui)

        self.drop_btn = QPushButton(self)
        self.auth_btn = QPushButton(self)

        self.drop_menu = self.SideMenu(self, self.drop_btn, "drop_menu.ui", 121, 200, True)
        self.auth_menu = self.SideMenu(self, self.auth_btn, "auth_menu.ui", 121, 200, False)

        self.drop_menu.menu.w1_btn.clicked.connect(self.switch_window)
        self.drop_menu.menu.w2_btn.clicked.connect(self.switch_window)
        self.auth_menu.menu.sign_in.clicked.connect(self.auth_btn.click)
        self.auth_menu.menu.sign_up.clicked.connect(self.auth_btn.click)

        self.drop_btn.setCheckable(True)
        self.drop_btn.setGeometry(Qt.QRect(5, 5, 25, 25))
        self.drop_btn.setStyleSheet("background: blue")
        self.drop_btn.clicked.connect(self.drop_menu.show_hide_menu)

        self.auth_btn.setCheckable(True)
        self.auth_btn.setGeometry(Qt.QRect(self.width() - 30, 5, 25, 25))
        self.auth_btn.setStyleSheet("background: blue")
        self.auth_btn.clicked.connect(self.auth_menu.show_hide_menu)

        self.drop_menu.show_hide_menu()
        self.auth_menu.show_hide_menu()

    def switch_window(self):
        if self.ui.sender().objectName() == self.drop_menu.menu.w1_btn.objectName():
            self.ui.setCurrentIndex(0)
        elif self.ui.sender().objectName() == self.drop_menu.menu.w2_btn.objectName():
            self.ui.setCurrentIndex(1)
        self.drop_btn.setChecked(False)
        self.auth_btn.setChecked(False)
        self.drop_menu.show_hide_menu()
        self.auth_menu.show_hide_menu()

    def resizeEvent(self, event):
        self.drop_menu.resizeEvent()
        self.auth_menu.resizeEvent()
        self.auth_btn.move(self.width() - 30, 5)

    def show(self):
        self.ui.show()
        super().show()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()
