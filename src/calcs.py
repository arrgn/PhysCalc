import numpy as np
from PyQt5 import Qt, uic, QtCore
from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
from choose_plot_type import ChoosePlotWindow
from config import path_to_file
import sympy as sym
from sympy import sin, cos, tan, cot, asin, acos, atan, acot, pi, log, sqrt


def ctg(x):
    return 1 / np.tan(x)


def arcctg(x):
    return -np.arctan(x) + pi / 2


class CalcsWindow:
    def __init__(self):
        super().__init__()
        self.ui = QWidget()

        self.deg2rad = 0.01745329251
        self.functions = []

        self.init_ui()

    def init_ui(self):
        uic.loadUi(path_to_file("Calcs.ui"), self.ui)

        self.ui.add_btn.clicked.connect(lambda: self.build_plot())

    def build_plot(self):
        self.ui.Plot_s.clear()
        self.ui.Plot_v.clear()
        self.ui.Plot_a.clear()

        self.functions.clear()

        res = ChoosePlotWindow(self.functions).get_result()
        if res == 0:
            return
        elif res == 3:
            for segment in self.functions:

                X = np.linspace(eval(segment[0].replace("pi", str(np.pi))), eval(segment[1].replace("pi", str(np.pi))), 1000)

                # Coordinate

                y_s = eval(f"{segment[2]}"
                           .replace("asin", "np.ASIN")
                           .replace("acos", "np.ACOS")
                           .replace("atan", "np.ATAN")
                           .replace("acos", "arcctg")
                           .replace("sin", "np.sin")
                           .replace("cos", "np.cos")
                           .replace("tan", "np.tan")
                           .replace("cot", "ctg")
                           .replace("log", "np.log")
                           .replace("ASIN", "arcsin")
                           .replace("ACOT", "arccot")
                           .replace("ATAN", "arctan")
                           .replace("sqrt", "np.sqrt")
                           .replace("x", "X"))

                if type(y_s) == int or type(y_s) == float:
                    y_s = np.linspace(y_s, y_s, 1000)

                self.ui.Plot_s.plot(x=X, y=y_s)

                x = sym.Symbol('x')

                # Velocity

                expr = eval(segment[2])
                velocity = str(sym.diff(expr)) \
                    .replace("asin", "np.ASIN") \
                    .replace("acos", "np.ACOS") \
                    .replace("atan", "np.ATAN") \
                    .replace("acos", "arcctg") \
                    .replace("sin", "np.sin") \
                    .replace("cos", "np.cos") \
                    .replace("tan", "np.tan") \
                    .replace("cot", "ctg") \
                    .replace("log", "np.log") \
                    .replace("ASIN", "arcsin") \
                    .replace("ACOT", "arccot") \
                    .replace("ATAN", "arctan") \
                    .replace("sqrt", "np.sqrt") \
                    .replace("x", "X")

                y_v = eval(velocity)

                if type(y_v) == int or type(y_v) == float:
                    y_v = np.linspace(y_v, y_v, 1000)

                self.ui.Plot_v.plot(x=X, y=y_v)

                # Acceleration

                expr = eval(segment[2])
                acceleration = str(sym.diff(expr, x, x)) \
                    .replace("asin", "np.ASIN") \
                    .replace("acos", "np.ACOS") \
                    .replace("atan", "np.ATAN") \
                    .replace("acos", "arcctg") \
                    .replace("sin", "np.sin") \
                    .replace("cos", "np.cos") \
                    .replace("tan", "np.tan") \
                    .replace("cot", "ctg") \
                    .replace("log", "np.log") \
                    .replace("ASIN", "arcsin") \
                    .replace("ACOT", "arccot") \
                    .replace("ATAN", "arctan") \
                    .replace("sqrt", "np.sqrt") \
                    .replace("x", "X")

                y_a = eval(acceleration.replace("x", "X"))

                if type(y_a) == int or type(y_a) == float:
                    y_a = np.linspace(y_a, y_a, 1000)

                self.ui.Plot_a.plot(x=X, y=y_a)

                """ 
                TEST INPUT DATA:
                0-1: (x ** 2) + 2 * (x ** 3)
                1-5: -4 * (x ** 2) + 16 * x - 9
                """

    def show(self):
        self.ui.show()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = CalcsWindow()
    w.show()
    app.exec()
