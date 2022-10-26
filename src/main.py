from PyQt5 import Qt, QtCore, uic
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QStackedWidget, QPushButton, QWidget, QFrame
from ballistic import BallisticWindow
from calcs import CalcsWindow


class Window:
    def __init__(self):
        super().__init__()

        self.ui = QStackedWidget()
        self.drop_menu = QWidget()
        self.menu_btn = QPushButton()
        self.animation = QPropertyAnimation()

        self.init_ui()

    def init_ui(self):
        self.ui.setGeometry(250, 250, 640, 640)

        self.ui.addWidget(BallisticWindow().ui)
        self.ui.addWidget(CalcsWindow().ui)

        uic.loadUi("Drop_menu.ui", self.drop_menu)

        # Here is example
        frame2 = QFrame(self.ui)
        frame2.setGeometry(QtCore.QRect(0, 0, 0, 480))
        frame2.setStyleSheet("background:red;")
        frame2.setFrameShape(QFrame.StyledPanel)
        frame2.setFrameShadow(QFrame.Raised)
        frame2.setObjectName("frame2")

        self.animation = QPropertyAnimation(frame2, b"size", self.ui)
        self.animation.setStartValue(QtCore.QSize(0, self.ui.height()))
        self.animation.setEndValue(QtCore.QSize(121, self.ui.height()))
        self.animation.setDuration(200)

        self.menu_btn = QPushButton(self.ui)
        self.menu_btn.setCheckable(True)
        self.menu_btn.setGeometry(Qt.QRect(5, 5, 25, 25))
        self.menu_btn.setStyleSheet("background: transparent")
        self.menu_btn.clicked.connect(self.show_hide_menu)

    def show_hide_menu(self):
        print(self.menu_btn.isChecked())
        if self.menu_btn.isChecked():
            self.animation.setDirection(QtCore.QAbstractAnimation.Forward)
            self.animation.start()
        else:
            self.animation.setDirection(QtCore.QAbstractAnimation.Backward)
            self.animation.start()

    def show(self):
        self.ui.show()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()
