import numpy as np
from PyQt5 import Qt, uic, QtCore  # type: ignore
from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
from config import path_to_file


class BallisticWindow:
    def __init__(self):
        super().__init__()
        self.ui = QWidget()

        self.deg2rad = 0.01745329251

        self.init_ui()

    def init_ui(self):
        uic.loadUi(path_to_file("Ballistics.ui"), self.ui)

        self.ui.AngleInput.setText("30")
        self.ui.VelocityInput.setText("10")
        self.ui.GInput.setText("9.81")

        self.ui.AngleInput.textChanged.connect(self.build_plot)
        self.ui.VelocityInput.textChanged.connect(self.build_plot)
        self.ui.GInput.textChanged.connect(self.build_plot)

        self.ui.Plot.setAspectLocked()
        self.ui.Plot.setLimits(xMin=0, yMin=0)

        self.build_plot()

    def build_plot(self):
        try:
            angle = float(self.ui.AngleInput.text()) * self.deg2rad
            velocity = float(self.ui.VelocityInput.text())
            g = float(self.ui.GInput.text())
        except ValueError as e:
            print(e)
            return

        x = np.linspace(0, velocity ** 2 * np.sin(2 * angle) / g, 1000)
        y = self.f(x, angle, velocity, g)

        self.ui.Plot.clear()
        self.ui.Plot.plot(x=x, y=y, pen=pg.mkPen('w', width=5, style=QtCore.Qt.DashLine))

        try:
            self.ui.Plot.setYRange(0, np.max(y) * 1.5)
            self.ui.Plot.setXRange(0, np.max(y) * 1.5)
        except:
            pass

    def f(self, x, angle, velocity, g):
        t = x / (velocity * np.cos(angle))
        return velocity * np.sin(angle) * t - g * (t ** 2) / 2

    def show(self):
        self.ui.show()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = BallisticWindow()
    w.show()
    app.exec()
