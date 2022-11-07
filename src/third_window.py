import random
import sys
from math import radians, cos, sin

from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import Qt as Qt2
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from time import sleep


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

            self.setMouseTracking(True)

            self.btn1_drawcoards = []
            self.btn1_wait_to_click = -1
            self.btn2_drawcoards = []
            self.btn2_wait_to_click = -1
            self.btn5_wait_to_click = -1
            self.render_objects = [[], [], []]
            self.object_history = []
            self.selected = None
            self.patterns = [Qt2.Dense1Pattern, Qt2.Dense2Pattern, Qt2.Dense3Pattern, Qt2.Dense4Pattern,
                             Qt2.Dense5Pattern, Qt2.Dense6Pattern, Qt2.Dense7Pattern]
            self.current_patt = random.choice(self.patterns)
            self.angle = 1
            self.ignore_rotate = False

            self.initUI()
            self.render_objects[0] = [self.transform_coards_for_rect(self.mouse_in_widget([0, 0], self.sandbox)[:2]),
                                      [220, 220, 220]]
            self.repaint()


        def initUI(self):
            uic.loadUi("third_window.ui", self)
            self.mousepos.setText("Координаты: None, None")
            self.mousebtn.setText("Никакая")
            self.btn1.setText("Линия")
            self.btn2.setText("Прямоугольник")
            self.btn3.setText("Отмена")
            self.btn4.setText("Очистка")
            self.btn5.setText("Удалить")
            self.sandbox.setText("")
            self.btn1.clicked.connect(lambda: self.btn1_click())
            self.btn2.clicked.connect(lambda: self.btn2_click())
            self.btn3.clicked.connect(lambda: self.btn3_click())
            self.btn4.clicked.connect(lambda: self.btn4_click())
            self.btn5.clicked.connect(lambda: self.btn5_click())
            self.dial.setMinimum(0)
            self.dial.setMaximum(359)
            self.dial.setValue(0)
            self.spinBox.setMinimum(0)
            self.spinBox.setMaximum(359)
            self.spinBox.setValue(0)
            self.dial.valueChanged.connect(lambda: self.rotate_changed())
            self.spinBox.valueChanged.connect(self.rotate2_changed)
            # self.dial.hide()
            # self.spinBox.hide()

        def renderf(self, qp):

            qp.setPen(QPen(Qt2.lightGray, 2, Qt2.SolidLine))

            if self.render_objects[0]:
                qp.setBrush(QColor(*self.render_objects[0][1]))
                qp.drawRect(*self.render_objects[0][0])

            qp.setPen(QPen(Qt2.black, 3, Qt2.SolidLine))

            for i in self.render_objects[1]:
                qp.drawLine(*i)

            qp.setBrush(QBrush(Qt2.darkGray, Qt2.SolidPattern))
            for i in self.render_objects[2]:
                if i == self.selected:
                    qp.setPen(QPen(Qt2.black, 5, Qt2.DotLine))
                    qp.setBrush(QBrush(Qt2.lightGray, Qt2.DiagCrossPattern))
                    self.drawRect(i[0], i[1], qp)
                    qp.setBrush(QBrush(Qt2.darkGray, Qt2.SolidPattern))
                    qp.setPen(QPen(Qt2.black, 3, Qt2.SolidLine))
                else:
                    self.drawRect(i[0], i[1], qp)
                    self.update()

            qp.setPen(QPen(Qt2.black, 3, Qt2.DashDotLine))

            if len(self.btn1_drawcoards) == 2:
                qp.drawLine(*self.transform_coards_for_line(self.btn1_drawcoards))

            qp.setBrush(QBrush(Qt2.darkGray, self.current_patt))

            if len(self.btn2_drawcoards) == 2:
                qp.drawRect(*self.transform_coards_for_rect(self.btn2_drawcoards))

        def rotate_rect_coards(self, center, w, h, angle):
            ans = [[], [], [], []]
            a = radians(angle)
            ans[0] = [(cos(a) * w - sin(a) * h) / 2 + center[0], (sin(a) * w + cos(a) * h) / 2 + center[1]]
            ans[1] = [(cos(a) * (-w) - sin(a) * h) / 2 + center[0], (sin(a) * (-w) + cos(a) * h) / 2 + center[1]]
            ans[2] = [(cos(a) * (-w) - sin(a) * (-h)) / 2 + center[0], (sin(a) * (-w) + cos(a) * (-h)) / 2 + center[1]]
            ans[3] = [(cos(a) * w - sin(a) * (-h)) / 2 + center[0], (sin(a) * w + cos(a) * (-h)) / 2 + center[1]]
            return ans

        def rotate_rect(self, rect, angle):
            j = [[(rect[1][0] + rect[0][0]) / 2, (rect[1][1] + rect[2][1]) / 2], rect[1][0] - rect[0][0],
                 rect[1][1] - rect[2][1], angle]
            j = self.rotate_rect_coards(*j)
            for h in range(len(j)):
                j[h] = int(j[h][0]), int(j[h][1])
            return j

        def drawRect(self, rect, angle, painter):
            r = self.rotate_rect(rect, angle)
            for h in range(len(r)):
                r[h] = QtCore.QPoint(*r[h])
            painter.drawConvexPolygon(*r)

        def paintEvent(self, event):
            qp = QPainter()
            qp.begin(self)
            self.renderf(qp)
            qp.end()

        def transform_coards_for_rect(self, coards):
            return [coards[0][0], coards[0][1], coards[1][0] - coards[0][0], coards[1][1] - coards[0][1]]

        def get_all_points(self, rect):
            p = [[], [], [], []]
            p[0] = [rect[0][0], rect[0][1]]
            p[1] = [rect[1][0], rect[1][1]]
            p[2] = [rect[0][0], rect[1][1]]
            p[3] = [rect[1][0], rect[0][1]]
            return self.sort_rect_points(p)

        def transform_coards_for_line(self, coards):
            return [coards[0][0], coards[0][1], coards[1][0], coards[1][1]]

        def flag_down(self):
            self.btn1_wait_to_click = -1
            self.btn2_wait_to_click = -1
            self.btn5_wait_to_click = -1
            self.selected = None

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
            co = len(self.object_history)
            try:
                if self.object_history:
                    while self.object_history[-1][0] == "rotated" and self.object_history[-1][1] == 0:
                        self.object_history.pop()
                    if type(self.object_history[-1][0]) is int:
                        delindex = self.render_objects[self.object_history[-1][0]].index(self.object_history[-1][1])
                        del self.render_objects[self.object_history[-1][0]][delindex]
                        print(f"{'LINE' if self.object_history[-1][0] == 1 else 'RECT'} deleted")
                        self.object_history.pop()

                    elif self.object_history[-1][0] == "rotated":
                        self.render_objects[2][self.render_objects[2].index(self.object_history[-1][2])][1] = 0
                        self.object_history.pop()
                        self.ignore_rotate = True
                        self.dial.setValue(0)
                        self.ignore_rotate = False
            except:
                pass
            finally:
                if co == len(self.object_history) and co != 0:
                    self.object_history.pop()

            self.update()

        def btn4_click(self):
            self.btn1_drawcoards = []
            self.render_objects = [[self.transform_coards_for_rect(self.mouse_in_widget([0, 0], self.sandbox)[:2]),
                                    [220, 220, 220]], [], []]
            self.btn1_wait_to_click = -1
            self.object_history = []
            self.update()
            print("cleaned")

        def btn5_click(self):
            print("mode: DELETE")

            if self.selected is not None:
                del self.render_objects[2][self.render_objects[2].index(self.selected)]
                self.selected = None

            self.flag_down()
            self.update()

        def rotate2_changed(self, value):
            self.rotate_changed(value)

        def rotate_changed(self, val=None):
            if val is None:
                val = self.dial.value()
            try:
                if not self.ignore_rotate:
                    while self.RectAndWidgetCollision(self.rotate_rect(self.selected[0], val), self.sandbox):
                        val -= 1
                    self.render_objects[2][self.render_objects[2].index(self.selected)][1] = val
                    self.selected[1] = val
                    self.spinBox.setValue(val)
                    self.dial.setValue(val)
                    if self.object_history[-1][0] == "rotated" and self.object_history[-1][2][0] == self.selected[0]:
                        self.object_history.pop()
                    self.object_history.append(["rotated", self.dial.value(), self.selected])
                    print(f"rotated at {self.dial.value()} degrees")
                else:
                    self.spinBox.setValue(0)
                    self.dial.setValue(0)
            except:
                pass
            self.update()

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

        def sort_rect_points(self, rect):
            ans = [[], [], [], []]
            ans[0] = min(rect, key=lambda x: (x[1], x[0]))
            del rect[rect.index(ans[0])]
            ans[1] = min(rect, key=lambda x: (x[1], x[0]))
            del rect[rect.index(ans[1])]
            ans[2] = min(rect, key=lambda x: (x[1], -x[0]))
            del rect[rect.index(ans[2])]
            ans[3] = rect[0]
            return ans

        def dot(self, x, y):
            return x[0] * y[0] + x[1] * y[1]

        def inRect(self, rect, coards):
            o1 = [rect[0][0] - rect[1][0], rect[0][1] - rect[1][1]]
            o2 = [rect[1][0] - rect[2][0], rect[1][1] - rect[2][1]]
            coards_o1 = self.dot(o1, coards)
            coards_o2 = self.dot(o2, coards)
            dotso1 = []
            dotso2 = []
            for i in rect:
                dotso1.append(self.dot(o1, i))
                dotso2.append(self.dot(o2, i))
            dotso1 = min(dotso1), max(dotso1)
            dotso2 = min(dotso2), max(dotso2)
            return dotso1[0] <= coards_o1 <= dotso1[1] and dotso2[0] <= coards_o2 <= dotso2[1]

        def RectAndWidgetCollision(self, rect, widget):
            t = []
            window_metrix = self.get_widget_metrix(widget)
            for i in range(len(rect)):
                t.append(window_metrix[0][0] <= rect[i][0] <= window_metrix[1][0])
                t.append(window_metrix[0][1] <= rect[i][1] <= window_metrix[1][1])
            return not all(t)

        def select_rect(self, rects, mouse_coards):
            for i in rects[::-1]:
                if self.inRect(self.rotate_rect(i[0], i[1]), mouse_coards):
                    return i

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

        def get_widget_metrix(self, qwidget):
            gp = qwidget.mapToGlobal(QtCore.QPoint(0, 0))
            widget = gp.x(), gp.y()
            window = (self.geometry().x(), self.geometry().y())
            widget_coards = (widget[0] - window[0], widget[1] - window[1])
            widget_size = (qwidget.geometry().width(), qwidget.geometry().height())
            widget_coards2 = (widget_coards[0] + widget_size[0], widget_coards[1] + widget_size[1])
            return [widget_coards, widget_coards2, widget_size]

        def left_top_corner_rect(self, rect):
            a1 = [rect[0], rect[1]]
            if rect[2] < 0:
                a1[0] += rect[2]
            if rect[3] < 0:
                a1[1] += rect[3]
            return [a1[0], a1[1], abs(rect[2]), abs(rect[3])]

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
                self.selected = None
                if self.btn1_wait_to_click == 0:
                    self.btn1_drawcoards = [mouse_coards, mouse_coards]
                    self.btn1_wait_to_click = 1
                    print(f"starting drawing LINE from ({mouse_coards[0]}, {mouse_coards[1]})")

            if self.btn2_wait_to_click in [0] and mouse_in_sandbox and mouse_btn == 1:
                if self.btn2_wait_to_click == 0:
                    self.selected = None
                    self.current_patt = random.choice(self.patterns)
                    self.btn2_drawcoards = [mouse_coards, mouse_coards]
                    self.btn2_wait_to_click = 1
                    print(f"starting drawing RECT from ({mouse_coards[0]}, {mouse_coards[1]})")

            if mouse_btn == 2 and mouse_in_sandbox:
                self.selected = self.select_rect(self.render_objects[2], mouse_coards)
                if self.selected is not None:
                    print(f"selected RECT {self.selected} with number {self.render_objects[2].index(self.selected)}")
                else:
                    print("nothing selected", self.render_objects[2], mouse_coards)

            if self.selected is None:
                self.dial.hide()
                self.spinBox.hide()
            else:
                self.dial.show()
                self.spinBox.show()

            self.update()

            self.mousepos.setText(f"Координаты:{event.x()}, {event.y()}")
            if (event.button() == Qt2.LeftButton):
                self.mousebtn.setText("Левая")
            elif (event.button() == Qt2.RightButton):
                self.mousebtn.setText("Правая")

        def mouseReleaseEvent(self, event):
            mouse_coards = (event.x(), event.y())
            mouse_btn = event.button()
            self.ignore_rotate = True
            self.dial.setValue(0)
            self.ignore_rotate = False
            if mouse_btn == 1 and len(self.btn1_drawcoards) == 2:
                self.render_objects[1].append(self.transform_coards_for_line(self.btn1_drawcoards))
                print(
                    f"drawn LINE from ({self.render_objects[1][-1][0]}, {self.render_objects[1][-1][1]}) to ({self.render_objects[1][-1][2]}, {self.render_objects[1][-1][3]})")
                self.object_history.append([1, self.transform_coards_for_line(self.btn1_drawcoards)])
                self.btn1_drawcoards = []
                self.btn1_wait_to_click = 0

            if mouse_btn == 1 and len(self.btn2_drawcoards) == 2:
                self.render_objects[2].append([self.get_all_points(self.btn2_drawcoards), 0])
                print(
                    f"drawn RECT ({self.render_objects[2][-1][0][0]}, {self.render_objects[2][-1][0][1]}, {self.render_objects[2][-1][0][2]}, {self.render_objects[2][-1][0][3]})")
                self.object_history.append([2, [self.get_all_points(self.btn2_drawcoards), 0]])
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
