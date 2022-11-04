import numpy as np
from PyQt5 import Qt, uic, QtCore
from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
from choose_plot_type import ChoosePlotWindow
from config import path_to_file


class CalcsWindow:
    def __init__(self):
        super().__init__()
        self.ui = QWidget()

        self.deg2rad = 0.01745329251

        self.init_ui()

    def init_ui(self):
        uic.loadUi(path_to_file("Calcs.ui"), self.ui)

        self.ui.add_btn.clicked.connect(self.build_plot)

    def build_plot(self):
        res = ChoosePlotWindow().get_result()
        if res == 0:
            return

    def show(self):
        self.ui.show()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = CalcsWindow()
    w.show()
    app.exec()
