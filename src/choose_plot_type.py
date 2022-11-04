from PyQt5 import Qt, uic
from PyQt5.QtWidgets import QDialog, QRadioButton
from config import path_to_file


class ChoosePlotWindow:
    class Dialog(QDialog):
        def __init__(self):
            super().__init__()
            self.accel = QRadioButton()
            self.vel = QRadioButton()
            self.space = QRadioButton()

            self.init_ui()

        def init_ui(self):
            uic.loadUi(path_to_file("Input_plot.ui"), self)

            self.accel.click()
            self.setResult(1)

            self.accel.clicked.connect(lambda: self.setResult(1))
            self.vel.clicked.connect(lambda: self.setResult(2))
            self.space.clicked.connect(lambda: self.setResult(3))

    def __init__(self):
        super().__init__()
        self.result = self.Dialog().exec()

    def get_result(self):
        return self.result


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = ChoosePlotWindow()
    app.exec()
