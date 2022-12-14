import numpy as np
from PyQt5 import Qt, uic, QtCore
from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
from path_module import path_to_file
from loggers import logger


class BallisticWindow:
    def __init__(self):
        super().__init__()
        self.ui = QWidget()

        self.deg2rad = 0.01745329251

        self.init_ui()

    def init_ui(self):
        uic.loadUi(path_to_file("uis", "ballistics.ui"), self.ui)

        # Set default values and configure
        self.ui.AngleInput.setText("30")
        self.ui.VelocityInput.setText("10")
        self.ui.GInput.setText("9.81")

        self.ui.AngleInput.textChanged.connect(lambda: self.build_plot())
        self.ui.VelocityInput.textChanged.connect(lambda: self.build_plot())
        self.ui.GInput.textChanged.connect(lambda: self.build_plot())

        # Lock aspect and set min cords limits
        self.ui.Plot.setAspectLocked()
        self.ui.Plot.setLimits(xMin=0, yMin=0)

        self.build_plot()

    def build_plot(self):
        """
        Build plot from user input.
        If input is incorrect, nothing will be build
        """
        # Check input
        try:
            angle = float(self.ui.AngleInput.text()) * self.deg2rad
            velocity = float(self.ui.VelocityInput.text())
            g = float(self.ui.GInput.text())
        except ValueError:
            logger.exception("Tracked exception occurred!")
            return

        x = np.linspace(0, velocity ** 2 * np.sin(2 * angle) / g, 1000)
        y = self.f(x, angle, velocity, g)

        self.ui.Plot.clear()
        self.ui.Plot.plot(x=x, y=y, pen=pg.mkPen('w', width=5, style=QtCore.Qt.DashLine))

        try:
            self.ui.Plot.setYRange(0, np.max(y) * 1.5)
            self.ui.Plot.setXRange(0, np.max(y) * 1.5)
        except Exception:
            logger.exception("Tracked exception occurred!")
            return

    def f(self, x, angle, velocity, g):
        # Try to scale graph in window
        try:
            self.ui.Plot.setYRange(0, np.max(y) * 1.5)
            self.ui.Plot.setXRange(0, np.max(y) * 1.5)
        except Exception:
            logger.exception("Tracked exception occurred!")

    def f(self, x: float, angle: float, velocity: float, g: float) -> float:
        """
        Simple function to build ballistic plot
        """
        t = x / (velocity * np.cos(angle))
        return velocity * np.sin(angle) * t - g * (t ** 2) / 2

    def show(self):
        self.ui.show()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = BallisticWindow()
    w.show()
    app.exec()
