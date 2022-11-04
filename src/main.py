from PyQt5 import Qt, QtCore, uic
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QStackedWidget, QPushButton, QWidget, QFrame
from ballistic import BallisticWindow
from calcs import CalcsWindow


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.menu_btn = QPushButton()
        self.animation = QPropertyAnimation()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 640, 640)
        self.ui = QStackedWidget(self)
        self.ui.setGeometry(0, 0, 640, 640)
        self.ui.addWidget(BallisticWindow().ui)
        self.ui.addWidget(CalcsWindow().ui)
        self.drop_menu = QFrame(self)
        uic.loadUi("Drop_menu.ui", self.drop_menu)

        self.drop_menu.w1_btn.clicked.connect(self.switch_window)
        self.drop_menu.w2_btn.clicked.connect(self.switch_window)

        self.animation = QPropertyAnimation(self.drop_menu, b"size", self.ui)
        self.animation.setStartValue(QtCore.QSize(0, self.ui.height()))
        self.animation.setEndValue(QtCore.QSize(121, self.ui.height()))
        self.animation.setDuration(200)

        self.menu_btn = QPushButton(self)
        self.menu_btn.setCheckable(True)
        self.menu_btn.setGeometry(Qt.QRect(5, 5, 25, 25))
        self.menu_btn.setStyleSheet("background: blue")
        self.menu_btn.clicked.connect(self.show_hide_menu)

    def switch_window(self):
        if self.ui.sender().objectName() == self.w1_btn.objectName():
            self.ui.setCurrentIndex(0)
        elif self.ui.sender().objectName() == self.w2_btn.objectName():
            self.ui.setCurrentIndex(1)
        self.menu_btn.setChecked(False)
        self.show_hide_menu()

    def show_hide_menu(self):
        if self.menu_btn.isChecked():
            self.animation.setDirection(QtCore.QAbstractAnimation.Forward)
            self.animation.start()
        else:
            self.animation.setDirection(QtCore.QAbstractAnimation.Backward)
            self.animation.start()

    def show(self):
        self.ui.show()
        super().show()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()
