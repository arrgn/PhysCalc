import numpy as np
from PyQt5 import Qt, uic
from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
from choose_plot_type import ChoosePlotWindow
from config import path_to_file
import sympy as sym
from sympy import *


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
        self.s_o = 0
        self.v_o = 0
        self.start = ["0", "0"]

        self.init_ui()

    def init_ui(self):
        uic.loadUi(path_to_file("Calcs.ui"), self.ui)

        self.ui.add_btn.clicked.connect(lambda: self.build_plot())

    def build_plot(self):
        self.ui.Plot_s.clear()
        self.ui.Plot_v.clear()
        self.ui.Plot_a.clear()

        self.functions.clear()

        res = ChoosePlotWindow(self.functions, self.start)

        self.s_o, self.v_o = self.start

        self.s_o = eval(self.s_o.replace("pi", str(np.pi)))
        self.v_o = eval(self.v_o.replace("pi", str(np.pi)))

        y_s = self.s_o
        y_v = self.v_o

        if res == 0:
            return
        elif res == 3:
            for segment in self.functions:

                X = np.linspace(eval(segment[0].replace("pi", str(np.pi))), eval(segment[1].replace("pi", str(np.pi))),
                                1000)

                segment[2] = segment[2].replace("^", "**")

                # Coordinate

                y_s = eval(self.sympy_to_numpy(f"{segment[2]}"))

                if type(y_s) == int or type(y_s) == float:
                    y_s = np.linspace(y_s, y_s, 1000)

                self.ui.Plot_s.plot(x=X, y=y_s)

                x = sym.Symbol('x')

                # Velocity

                expr = eval(segment[2])
                velocity = self.sympy_to_numpy(str(sym.diff(expr)))

                y_v = eval(velocity)

                if type(y_v) == int or type(y_v) == float:
                    y_v = np.linspace(y_v, y_v, 1000)

                self.ui.Plot_v.plot(x=X, y=y_v)

                # Acceleration

                expr = eval(segment[2])
                acceleration = self.sympy_to_numpy(str(sym.diff(expr, x, x)))

                y_a = eval(acceleration)

                if type(y_a) == int or type(y_a) == float:
                    y_a = np.linspace(y_a, y_a, 1000)

                self.ui.Plot_a.plot(x=X, y=y_a)

                self.v_o = y_v[-1]
                self.s_o = y_s[-1]

        elif res == 2:
            for segment in self.functions:

                X = np.linspace(eval(segment[0].replace("pi", str(np.pi))), eval(segment[1].replace("pi", str(np.pi))),
                                1000)

                segment[2] = segment[2].replace("^", "**")

                # Velocity

                y_v = eval(self.sympy_to_numpy(f"{segment[2]}"))

                if type(y_v) == int or type(y_v) == float:
                    y_v = np.linspace(y_v, y_v, 1000)

                self.ui.Plot_v.plot(x=X, y=y_v)

                # Coordinate

                x = sym.Symbol('x')

                expr = eval(segment[2])

                coordinate = self.sympy_to_numpy(str(sym.integrate(expr, x)) + f" + {self.v_o}")

                y_s = eval(coordinate + " + " + str((self.s_o - eval(f"{coordinate}".replace("X", segment[0])))))

                if type(y_s) == int or type(y_s) == float:
                    y_s = np.linspace(y_s, y_s, 1000)

                self.ui.Plot_s.plot(x=X, y=y_s)

                # Acceleration

                expr = eval(segment[2])
                acceleration = self.sympy_to_numpy(str(sym.diff(expr)))

                y_a = eval(acceleration.replace("X", f"(X - {segment[0].replace('pi', str(np.pi))})"))

                if type(y_a) == int or type(y_a) == float:
                    y_a = np.linspace(y_a, y_a, 1000)

                self.ui.Plot_a.plot(x=X, y=y_a)

                self.v_o = y_v[-1]
                self.s_o = y_s[-1]

        elif res == 1:
            for segment in self.functions:

                X = np.linspace(eval(segment[0].replace("pi", str(np.pi))), eval(segment[1].replace("pi", str(np.pi))),
                                1000)

                segment[2] = segment[2].replace("^", "**")

                # Acceleration

                y_a = eval(self.sympy_to_numpy(f"{segment[2]}"))

                if type(y_a) == int or type(y_a) == float:
                    y_a = np.linspace(y_a, y_a, 1000)

                self.ui.Plot_a.plot(x=X, y=y_a)

                # Velocity

                x = sym.Symbol('x')

                expr = eval(segment[2])

                velocity = self.sympy_to_numpy(str(sym.integrate(expr, x)))

                func = velocity + " + " + str(
                    (self.v_o - eval(f"{velocity}".replace("X", str(eval(segment[0].replace("pi", str(np.pi))))))))

                y_v = eval(func)

                if type(y_v) == int or type(y_v) == float:
                    y_v = np.linspace(y_v, y_v, 1000)

                self.ui.Plot_v.plot(x=X, y=y_v)

                # Coordinate

                expr = eval(func.replace("X", "x"))

                coordinate = self.sympy_to_numpy(str(sym.integrate(expr, x)) + f" + {self.v_o}")

                y_s = eval(coordinate + " + " + str(
                    (self.s_o - eval(f"{coordinate}".replace("X", str(eval(segment[0].replace("pi", str(np.pi)))))))))
                if type(y_s) == int or type(y_s) == float:
                    y_s = np.linspace(y_s, y_s, 1000)

                self.ui.Plot_s.plot(x=X, y=y_s)

                self.v_o = y_v[-1]
                self.s_o = y_s[-1]

    def sympy_to_numpy(self, expr: str):
        return expr.replace("asin", "np.ASIN") \
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

    def show(self):
        self.ui.show()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = CalcsWindow()
    w.show()
    app.exec()
