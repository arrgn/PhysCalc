import sys

from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import Qt as Qt2
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget


class ExceptionHandler(QtCore.QObject):
    errorSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(ExceptionHandler, self).__init__()

    def handler(self, exctype, value, traceback):
        self.errorSignal.emit()
        sys._excepthook(exctype, value, traceback)


class ThirdWindow:
    class MouseTrack(QWidget):
        def __init__(self):
            super().__init__()
            self.initUI()
            self.pixmap = QPixmap('i2.png')
            self.sandbox.setPixmap(self.pixmap)
            self.setMouseTracking(True)



        def initUI(self):
            uic.loadUi("Third_window.ui", self)
            self.mousepos.setText("Координаты: None, None")
            self.mousebtn.setText("Никакая")



        def mouseMoveEvent(self, event):
            self.mousepos.setText(f"Координаты: {event.x()}, {event.y()}")

        def mousePressEvent(self, event):
            print(self.sandbox.size())
            self.mousepos.setText(f"Координаты:{event.x()}, {event.y()}")
            if (event.button() == Qt2.LeftButton):
                self.mousebtn.setText("Левая")
            elif (event.button() == Qt2.RightButton):
                self.mousebtn.setText("Правая")

        def mouseReleaseEvent(self, event):
            x, y = event.x(), event.y()
            self.mousebtn.setText("Никакая")

    def __init__(self):
        super().__init__()
        self.ui = self.MouseTrack()

    def show(self):
        self.ui.show()


if __name__ == "__main__":
    exceptionHandler = ExceptionHandler()
    sys._excepthook = sys.excepthook
    sys.excepthook = exceptionHandler.handler
    app = QApplication(sys.argv)
    ex = ThirdWindow()
    ex.show()
    sys.exit(app.exec())
