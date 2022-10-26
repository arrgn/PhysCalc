from PyQt5 import Qt
from PyQt5.QtWidgets import QStackedWidget
from ballistic import BallisticWindow
from calcs import CalcsWindow


class Window:
    def __init__(self):
        super().__init__()
        self.ui = QStackedWidget()

        self.init_ui()

    def init_ui(self):
        self.ui.addWidget(BallisticWindow().ui)
        self.ui.addWidget(CalcsWindow().ui)

    def show(self):
        self.ui.show()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()
