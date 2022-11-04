import sys

from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import Qt as Qt2
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
import random


class ExceptionHandler(QtCore.QObject):
    errorSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(ExceptionHandler, self).__init__()

    def handler(self, exctype, value, traceback):
        self.errorSignal.emit()
        sys._excepthook(exctype, value, traceback)


class ThirdWindow:
    class DrawWindow(QWidget):
        def __init__(self):
            super().__init__()

            # self.pixmap = QPixmap('i2.png')
            # self.sandbox.setPixmap(self.pixmap)
            self.setMouseTracking(True)

            self.btn1_drawcoards = []
            self.btn1_wait_to_click = -1
            self.btn2_drawcoards = []
            self.btn2_wait_to_click = -1
            self.render_objects = [[], [], []]
            self.object_history = []
            self.patterns = [Qt2.Dense1Pattern, Qt2.Dense2Pattern, Qt2.Dense3Pattern, Qt2.Dense4Pattern,
                             Qt2.Dense5Pattern, Qt2.Dense6Pattern, Qt2.Dense7Pattern]
            self.current_patt = random.choice(self.patterns)

            self.initUI()

        def initUI(self):
            uic.loadUi("Third_window.ui", self)
            self.mousepos.setText("Координаты: None, None")
            self.mousebtn.setText("Никакая")
            self.btn1.setText("Линия")
            self.btn2.setText("Прямоугольник")
            self.btn3.setText("Отмена")
            self.btn4.setText("Очистка")
            self.sandbox.setText("")
            self.btn1.clicked.connect(lambda: self.btn1_click())
            self.btn2.clicked.connect(lambda: self.btn2_click())
            self.btn3.clicked.connect(lambda: self.btn3_click())
            self.btn4.clicked.connect(lambda: self.btn4_click())

        def paintEvent(self, event):
            qp = QPainter()
            qp.begin(self)
            self.drawact(qp)
            qp.end()

        def transform_coards_for_rect(self, coards):
            return [coards[0][0], coards[0][1], coards[1][0] - coards[0][0], coards[1][1] - coards[0][1]]

        def transform_coards_for_line(self, coards):
            return [coards[0][0], coards[0][1], coards[1][0], coards[1][1]]

        def drawact(self, qp):

            qp.setPen(QPen(Qt2.lightGray, 2, Qt2.SolidLine))

            if self.render_objects[0]:
                qp.setBrush(QColor(*self.render_objects[0][1]))
                qp.drawRect(*self.render_objects[0][0])

            qp.setPen(QPen(Qt2.black, 3, Qt2.SolidLine))

            for i in self.render_objects[1]:
                qp.drawLine(*i)

            qp.setBrush(QBrush(Qt2.darkGray, Qt2.SolidPattern))
            for i in self.render_objects[2]:
                qp.drawRect(*i)

            qp.setPen(QPen(Qt2.black, 3, Qt2.DashDotLine))

            if len(self.btn1_drawcoards) == 2:
                qp.drawLine(*self.transform_coards_for_line(self.btn1_drawcoards))

            qp.setBrush(QBrush(Qt2.darkGray, self.current_patt))

            if len(self.btn2_drawcoards) == 2:
                qp.drawRect(*self.transform_coards_for_rect(self.btn2_drawcoards))

        def flag_down(self):
            self.btn1_wait_to_click = -1
            self.btn2_wait_to_click = -1

        def btn1_click(self):
            print("mode: LINE")
            self.flag_down()
            if self.btn1_wait_to_click == -1:
                self.btn1_wait_to_click = 0
            self.update()

        def btn2_click(self):
            print("mode: RECT")
            self.flag_down()
            if self.btn2_wait_to_click == -1:
                self.btn2_wait_to_click = 0
            self.update()

        def btn3_click(self):
            if self.object_history:
                self.render_objects[self.object_history[-1]].pop()
                self.object_history.pop()
                print("last action canceled")
            self.update()

        def btn4_click(self):
            self.btn1_drawcoards = []
            self.render_objects = [[self.transform_coards_for_rect(self.mouse_in_widget([0, 0], self.sandbox)[:2]),
                                    [220, 220, 220]], [], []]
            self.btn1_wait_to_click = -1
            self.object_history = []
            self.update()
            print("cleaned")

        def inRange(self, mi, ma, coard):
            t = []
            for i in range(len(coard)):
                t.append(mi[i] <= coard[i] <= ma[i])
            return all(t)

        def setInRange(self, mi, ma, coard):
            t = []
            for i in range(len(coard)):
                t.append(min(max(mi[i], coard[i]), ma[i]))
            return t

        def moose_set_in_widget(self, mouse_coards, qwidget):
            gp = qwidget.mapToGlobal(QtCore.QPoint(0, 0))
            widget = gp.x(), gp.y()
            window = (self.geometry().x(), self.geometry().y())
            widget_coards = (widget[0] - window[0], widget[1] - window[1])
            widget_size = (qwidget.geometry().width(), qwidget.geometry().height())
            widget_coards2 = (widget_coards[0] + widget_size[0], widget_coards[1] + widget_size[1])
            mouse_in_widget = self.setInRange(widget_coards, widget_coards2, mouse_coards)
            return mouse_in_widget

        def mouse_in_widget(self, mouse_coards, qwidget):
            gp = qwidget.mapToGlobal(QtCore.QPoint(0, 0))
            widget = gp.x(), gp.y()
            window = (self.geometry().x(), self.geometry().y())
            widget_coards = (widget[0] - window[0], widget[1] - window[1])
            widget_size = (qwidget.geometry().width(), qwidget.geometry().height())
            widget_coards2 = (widget_coards[0] + widget_size[0], widget_coards[1] + widget_size[1])
            return [widget_coards, widget_coards2, widget_size, mouse_coards,
                    self.inRange(widget_coards, widget_coards2, mouse_coards)]

        def mouseMoveEvent(self, event):
            mouse_coards = (event.x(), event.y())
            self.render_objects[0] = [self.transform_coards_for_rect(self.mouse_in_widget([0, 0], self.sandbox)[:2]),
                                      [220, 220, 220]]
            if len(self.btn1_drawcoards) == 2:
                self.btn1_drawcoards[1] = self.moose_set_in_widget(mouse_coards, self.sandbox)

            if len(self.btn2_drawcoards) == 2:
                self.btn2_drawcoards[1] = self.moose_set_in_widget(mouse_coards, self.sandbox)

            self.mousepos.setText(f"Координаты: {event.x()}, {event.y()}")
            self.update()

        def mousePressEvent(self, event):
            mouse_coards = (event.x(), event.y())
            mouse_btn = event.button()
            mouse_in_sandbox = self.mouse_in_widget(mouse_coards, self.sandbox)[-1]
            self.render_objects[0] = [self.transform_coards_for_rect(self.mouse_in_widget([0, 0], self.sandbox)[:2]),
                                      [220, 220, 220]]
            if self.btn1_wait_to_click in [0] and mouse_in_sandbox and mouse_btn == 1:
                if self.btn1_wait_to_click == 0:
                    self.btn1_drawcoards = [mouse_coards, mouse_coards]
                    self.btn1_wait_to_click = 1
                    print(f"starting drawing LINE from ({mouse_coards[0]}, {mouse_coards[1]})")

            if self.btn2_wait_to_click in [0] and mouse_in_sandbox and mouse_btn == 1:
                if self.btn2_wait_to_click == 0:
                    self.current_patt = random.choice(self.patterns)
                    self.btn2_drawcoards = [mouse_coards, mouse_coards]
                    self.btn2_wait_to_click = 1
                    print(f"starting drawing RECT from ({mouse_coards[0]}, {mouse_coards[1]})")

            self.update()

            self.mousepos.setText(f"Координаты:{event.x()}, {event.y()}")
            if (event.button() == Qt2.LeftButton):
                self.mousebtn.setText("Левая")
            elif (event.button() == Qt2.RightButton):
                self.mousebtn.setText("Правая")

        def mouseReleaseEvent(self, event):
            mouse_coards = (event.x(), event.y())
            mouse_btn = event.button()
            if mouse_btn == 1 and len(self.btn1_drawcoards) == 2:
                self.render_objects[1].append(self.transform_coards_for_line(self.btn1_drawcoards))
                print(
                    f"drawed LINE from ({self.render_objects[1][-1][0]}, {self.render_objects[1][-1][1]}) to ({self.render_objects[1][-1][2]}, {self.render_objects[1][-1][3]})")
                self.object_history.append(1)
                self.btn1_drawcoards = []
                self.btn1_wait_to_click = 0

            if mouse_btn == 1 and len(self.btn2_drawcoards) == 2:
                self.render_objects[2].append(self.transform_coards_for_rect(self.btn2_drawcoards))
                print(
                    f"drawed RECT from ({self.render_objects[2][-1][0]}, {self.render_objects[2][-1][1]}) to ({self.render_objects[2][-1][2]}, {self.render_objects[2][-1][3]})")
                self.object_history.append(2)
                self.btn2_drawcoards = []
                self.btn2_wait_to_click = 0

            self.mousebtn.setText("Никакая")
            self.update()

    def __init__(self):
        super().__init__()
        self.ui = self.DrawWindow()

    def show(self):
        self.ui.show()


if __name__ == "__main__":
    exceptionHandler = ExceptionHandler()
    sys._excepthook = sys.excepthook
    sys.excepthook = exceptionHandler.handler
    app = QApplication(sys.argv)
    ex = ThirdWindow()
    ex.show()
    sys.exit(app.exec())
