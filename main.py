import numpy as np
from PyQt5 import Qt
import pyqtgraph as pg


class Window(Qt.QWidget):

    def __init__(self):
        super().__init__()

        layout = Qt.QVBoxLayout(self)

        x = np.linspace(-10, 10, 1000)
        y = x ** 3 - np.sin(x)
        p = pg.PlotItem(x=x, y=y)
        self.view = pg.PlotWidget(plotItem=p)

        layout.addWidget(self.view)


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()
