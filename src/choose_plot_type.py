from PyQt5 import Qt, uic
from PyQt5.QtWidgets import QDialog, QRadioButton, QListWidget, QHBoxLayout
from typing import List

from config import path_to_file


class ChoosePlotWindow:
    class Dialog(QDialog):
        def __init__(self, functions):
            super().__init__()
            self.accel = QRadioButton()
            self.vel = QRadioButton()
            self.space = QRadioButton()
            self.listWidget = QListWidget()

            self.functions: List[List[str, str, str]] = functions

            self.inp_result = 0

            self.init_ui()

        def init_ui(self):
            uic.loadUi(path_to_file("input_plot.ui"), self)

            self.buttonBox.accepted.connect(lambda: self.done(self.inp_result))

            self.accel.clicked.connect(lambda: self.change_plot_type())
            self.vel.clicked.connect(lambda: self.change_plot_type())
            self.space.clicked.connect(lambda: self.change_plot_type())

            self.addButton.clicked.connect(lambda: self.list_add_item())
            self.removeButton.clicked.connect(lambda: self.list_remove_item())

            self.leftBorderInput.textChanged.connect(lambda: self.autosave())
            self.rightBorderInput.textChanged.connect(lambda: self.autosave())
            self.functionInput.textChanged.connect(lambda: self.autosave())

            self.listWidget.currentRowChanged.connect(lambda: self.list_on_row_changed())

            self.accel.click()
            self.list_add_item()

        def change_plot_type(self):
            if self.sender().objectName() == "accel":
                self.change_result(1)
                self.s0_widget.setHidden(False)
                self.v0_widget.setHidden(False)
            elif self.sender().objectName() == "vel":
                self.change_result(2)
                self.s0_widget.setHidden(False)
                self.v0_widget.setHidden(True)
            elif self.sender().objectName() == "space":
                self.change_result(3)
                self.s0_widget.setHidden(True)
                self.v0_widget.setHidden(True)

        def autosave(self):
            if self.sender().objectName() == "leftBorderInput":
                change_index = 0
            elif self.sender().objectName() == "rightBorderInput":
                change_index = 1
            elif self.sender().objectName() == "functionInput":
                change_index = 2

            self.functions[self.listWidget.currentRow()][change_index] = self.sender().text()

        def change_result(self, new_result: int):
            self.inp_result = new_result

        def list_add_item(self):
            self.listWidget.addItem(f"el_{self.listWidget.count()}")
            self.listWidget.setCurrentItem(self.listWidget.item(self.listWidget.count()))
            self.functions.append(["0", "0", ""])

            self.leftBorderInput.setText("0")
            self.rightBorderInput.setText("0")

            self.functionInput.setText("")

        def list_remove_item(self):
            if len(self.functions) <= 1:
                return

            selected_row = self.listWidget.currentRow()

            self.listWidget.takeItem(selected_row)
            self.functions.pop(selected_row)

        def list_on_row_changed(self):
            selected_row = self.listWidget.currentRow()

            self.leftBorderInput.setText(self.functions[selected_row][0])
            self.rightBorderInput.setText(self.functions[selected_row][1])
            self.functionInput.setText(self.functions[selected_row][2])

    def __init__(self, functions):
        super().__init__()
        self.result = self.Dialog(functions).exec()

    def get_result(self):
        return self.result


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = ChoosePlotWindow([])
    app.exec()
