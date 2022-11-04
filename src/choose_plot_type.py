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

            self.inp_result = 0

            self.init_ui()

        def init_ui(self):
            uic.loadUi(path_to_file("Input_plot.ui"), self)

            self.buttonBox.accepted.connect(lambda: self.done(self.inp_result))

            self.accel.clicked.connect(lambda: self.change_result(1))
            self.vel.clicked.connect(lambda: self.change_result(2))
            self.space.clicked.connect(lambda: self.change_result(3))

            self.accel.click()

        def change_result(self, new_result: int):
            self.inp_result = new_result


    def __init__(self):
        super().__init__()
        self.result = self.Dialog().exec()

    def get_result(self):
        return self.result


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = ChoosePlotWindow()
    app.exec()
