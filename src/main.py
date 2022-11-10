from PyQt5 import Qt
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QStackedWidget, QPushButton, QWidget, QGridLayout
from ballistic import BallisticWindow
from calcs import CalcsWindow
from side_menu import SideMenu
from auth_window import AuthWindow
from profile_window import ProfileWindow
from path_module import path_to_file, create_dir
import logging.config
import logging


class Window(QWidget):
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

        self.drop_menu = SideMenu(self, self.drop_btn, "drop_menu.ui", 121, 200, True)
        self.auth_menu = SideMenu(self, self.auth_btn, "auth_menu.ui", 121, 200, False)
        self.drop_menu.menu.w1_btn.clicked.connect(self.switch_window)
        self.drop_menu.menu.w2_btn.clicked.connect(self.switch_window)
        self.auth_menu.menu.sign_in.clicked.connect(lambda: AuthWindow(True).exec())
        self.auth_menu.menu.sign_up.clicked.connect(lambda: AuthWindow(False).exec())
        self.auth_menu.menu.profile.clicked.connect(lambda: ProfileWindow().exec())

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
        self.drop_menu.resize_event()
        self.auth_menu.resize_event()
        self.auth_btn.move(self.width() - 30, 5)

    def show(self):
        self.ui.show()
        super().show()


if __name__ == "__main__":
    create_dir("logs")
    logging.config.fileConfig(fname=path_to_file("logging.conf"), disable_existing_loggers=False)
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()
