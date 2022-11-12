import logging.config
import sys
import traceback

from PyQt5 import Qt
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QStackedWidget, QPushButton, QWidget, QGridLayout

from auth_window import AuthWindow
from ballistic import BallisticWindow
from calcs import CalcsWindow
from path_module import path_to_file, create_dir
from profile_window import ProfileWindow
from side_menu import SideMenu
from third_window import ThirdWindow
from loggers import logger


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = QStackedWidget()
        self.layout_ = QGridLayout()
        self.drop_menu = None
        self.auth_menu = None
        # Initialize some widgets for convenience
        self.drop_btn = QPushButton()
        self.auth_btn = QPushButton()
        self.animation = QPropertyAnimation()

        self.init_ui()

    def init_ui(self):
        # Initialize ui
        self.setLayout(self.layout_)
        self.layout_.addWidget(self.ui)

        self.setGeometry(0, 0, 640, 640)
        self.ui.setGeometry(0, 0, 640, 640)
        self.ui.addWidget(BallisticWindow().ui)
        self.ui.addWidget(CalcsWindow().ui)
        self.ui.addWidget(ThirdWindow(self).ui)

        self.drop_btn = QPushButton(self)
        self.auth_btn = QPushButton(self)

        # Add and configure drop menus
        self.drop_menu = SideMenu(self, self.drop_btn, path_to_file("uis", "drop_menu.ui"), 121, 200, True)
        self.auth_menu = SideMenu(self, self.auth_btn, path_to_file("uis", "auth_menu.ui"), 121, 200, False)
        self.drop_menu.menu.w1_btn.clicked.connect(self.switch_window)
        self.drop_menu.menu.w2_btn.clicked.connect(self.switch_window)
        self.drop_menu.menu.w3_btn.clicked.connect(self.switch_window)
        self.auth_menu.menu.sign_in.clicked.connect(lambda: AuthWindow(True).exec())
        self.auth_menu.menu.sign_up.clicked.connect(lambda: AuthWindow(False).exec())
        self.auth_menu.menu.profile.clicked.connect(lambda: ProfileWindow().exec())

        # Connect buttons to drop menus (show/hide)
        self.drop_btn.setCheckable(True)
        self.drop_btn.setGeometry(Qt.QRect(5, 5, 25, 25))
        self.drop_btn.clicked.connect(self.drop_menu.show_hide_menu)

        self.auth_btn.setCheckable(True)
        self.auth_btn.setGeometry(Qt.QRect(self.width() - 30, 5, 25, 25))
        self.auth_btn.clicked.connect(self.auth_menu.show_hide_menu)

        self.drop_menu.show_hide_menu()
        self.auth_menu.show_hide_menu()

        self.setWindowTitle("Ballistics")

        # Load stylesheet from DevSec Studio (protected by MIT LICENSE)
        ssh_file = path_to_file("themes", "SpyBot.qss")
        with open(ssh_file, "r") as fh:
            self.setStyleSheet(fh.read())

    def switch_window(self):
        """
        Switch window using QStackedWidget.
        All menus will be hidden
        """
        # Switch window
        if self.ui.sender().objectName() == self.drop_menu.menu.w1_btn.objectName():
            self.setWindowTitle("Ballistics")
            self.ui.setCurrentIndex(0)
        elif self.ui.sender().objectName() == self.drop_menu.menu.w2_btn.objectName():
            self.setWindowTitle("Calcs")
            self.ui.setCurrentIndex(1)
        elif self.ui.sender().objectName() == self.drop_menu.menu.w3_btn.objectName():
            self.setWindowTitle("Drawing")
            self.ui.setCurrentIndex(2)
        # Uncheck buttons and hide menus
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


def log_handler(exctype, value, tb):
    logger.exception(''.join(traceback.format_exception(exctype, value, tb)))


if __name__ == "__main__":
    # Create folder for log and load log configuration
    create_dir("logs")
    logging.config.fileConfig(fname=path_to_file("logging.conf"), disable_existing_loggers=False)
    sys.excepthook = log_handler
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()
