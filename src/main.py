from PyQt5 import Qt, QtCore, uic
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QStackedWidget, QPushButton, QWidget, QFrame, QGridLayout
from ballistic import BallisticWindow
from calcs import CalcsWindow
from path_module import path_to_file


class Window(QWidget):
    class SideMenu():
        def __init__(self, widget: QWidget, path: str, width: int, duration: int, left: bool) -> None:
            self.menu = QFrame()
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
            if self.widget.menu_btn.isChecked():
                self.widget.menu_btn.hide()
                self.animation.setDirection(QtCore.QAbstractAnimation.Forward)
                self.animation.start()
            else:
                self.animation.setDirection(QtCore.QAbstractAnimation.Backward)
                self.animation.start()
                self.widget.menu_btn.show()

        def resizeEvent(self):
            if self.widget.menu_btn.isChecked():
                self.menu.resize(QtCore.QSize(self.width, self.widget.height()))
            self.update_animation()

        def update_animation(self):
            if self.left:
                self.animation.setStartValue(QtCore.QSize(0, self.widget.height()))
                self.animation.setEndValue(QtCore.QSize(self.width, self.widget.height()))
            else:
                self.animation.setStartValue(QtCore.QSize(self.widget.width(), self.widget.height()))
                self.animation.setEndValue(QtCore.QSize(self.widget.width() - self.width, self.widget.height()))

    def __init__(self):
        super().__init__()
        self.ui = QStackedWidget()
        self.layout_ = QGridLayout()
        self.drop_menu = None
        self.menu_btn = QPushButton()
        self.animation = QPropertyAnimation()
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.layout_)
        self.layout_.addWidget(self.ui)

        self.setGeometry(0, 0, 640, 640)
        self.ui.setGeometry(0, 0, 640, 640)
        self.ui.addWidget(BallisticWindow().ui)
        self.ui.addWidget(CalcsWindow().ui)

        self.drop_menu = self.SideMenu(self, "drop_menu.ui", 121, 200, True)

        self.drop_menu.menu.w1_btn.clicked.connect(self.switch_window)
        self.drop_menu.menu.w2_btn.clicked.connect(self.switch_window)

        self.menu_btn = QPushButton(self)
        self.menu_btn.setCheckable(True)
        self.menu_btn.setGeometry(Qt.QRect(5, 5, 25, 25))
        self.menu_btn.setStyleSheet("background: blue")
        self.menu_btn.clicked.connect(self.drop_menu.show_hide_menu)

        self.drop_menu.show_hide_menu()

    def switch_window(self):
        if self.ui.sender().objectName() == self.drop_menu.menu.w1_btn.objectName():
            self.ui.setCurrentIndex(0)
        elif self.ui.sender().objectName() == self.drop_menu.menu.w2_btn.objectName():
            self.ui.setCurrentIndex(1)
        self.menu_btn.setChecked(False)
        self.drop_menu.show_hide_menu()

    def resizeEvent(self, event):
        self.drop_menu.resizeEvent()

    def show(self):
        self.ui.show()
        super().show()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()
