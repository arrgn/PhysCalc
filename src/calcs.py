import numpy as np
from PyQt5 import Qt, uic, QtCore
from PyQt5.QtWidgets import QWidget, QLabel
import pyqtgraph as pg


class CalcsWindow:
    def __init__(self):
        super().__init__()
        self.ui = QWidget()

        self.deg2rad = 0.01745329251

        self.init_ui()

    def init_ui(self):
        uic.loadUi("Calcs.ui", self.ui)
        label = QLabel(self.ui)
        label.setGeometry(0, 0, 480, 480)
        label.setText("WTF")

    def show(self):
        self.ui.show()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = CalcsWindow()
    w.show()
    app.exec()