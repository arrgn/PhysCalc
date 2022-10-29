from PyQt5 import Qt, QtCore, uic
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QStackedWidget, QPushButton, QWidget, QFrame
from ballistic import BallisticWindow
from calcs import CalcsWindow


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = QStackedWidget()
        self.drop_menu = QWidget()
        self.menu_btn = QPushButton()
        self.animation = QPropertyAnimation()
        self.frame2 = QFrame()
        self.w1_btn = QPushButton()
        self.w2_btn = QPushButton()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 640, 640)
        self.ui = QStackedWidget(self)
        self.ui.setGeometry(0, 0, 640, 640)

        self.ui.addWidget(BallisticWindow().ui)
        self.ui.addWidget(CalcsWindow().ui)

        uic.loadUi("Drop_menu.ui", self.drop_menu)

        # Here is example
        self.frame2 = QFrame(self)
        self.frame2.setGeometry(QtCore.QRect(0, 0, 0, 480))
        self.frame2.setStyleSheet("background:red;")
        self.frame2.setFrameShape(QFrame.StyledPanel)
        self.frame2.setFrameShadow(QFrame.Raised)
        self.frame2.setObjectName("frame2")

        self.w1_btn = QPushButton(self.frame2)
        self.w1_btn.setText("Ballistics window")
        self.w1_btn.setGeometry(QtCore.QRect(0, 0, 121, 20))
        self.w1_btn.setStyleSheet("background: green;")
        self.w1_btn.setObjectName("w1_btn")
        self.w1_btn.clicked.connect(self.switch_window)

        self.w2_btn = QPushButton(self.frame2)
        self.w2_btn.setText("Calcs window")
        self.w2_btn.setGeometry(QtCore.QRect(0, 20, 121, 20))
        self.w2_btn.setStyleSheet("background: cyan;")
        self.w2_btn.setObjectName("w2_btn")
        self.w2_btn.clicked.connect(self.switch_window)

        self.animation = QPropertyAnimation(self.frame2, b"size", self.ui)
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
