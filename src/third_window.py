import json
import random
import sys
from copy import deepcopy
from math import radians, cos, sin

from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import Qt as Qt2
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit, QWidget, QComboBox

from config import user
from path_module import path_to_file, path_to_userdata
from loggers import logger


class ExceptionHandler(QtCore.QObject):
    errorSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(ExceptionHandler, self).__init__()

    def handler(self, exctype, value, traceback):
        self.errorSignal.emit()
        sys._excepthook(exctype, value, traceback)


class ThirdWindow:
    '''
    Classs of Third Window
    '''

    class DrawWindow(QWidget):
        '''
        Create QDialog with title, text and ok/cancel buttons
        return number of pressed button
        '''

        class Dialog(QDialog):
            '''
            Create QDialog with title, text and ok/cancel buttons
            return number of pressed button
            '''

            def __init__(self, text, title, mode="Ask", shared=None, out=None, show_button_ok=False):
                super().__init__()
                self.text = text
                self.show_button_ok = show_button_ok
                self.title = title
                self.mode = mode
                self.shared = shared
                self.out = out

                self.init_ui()

            def init_ui(self):
                if self.show_button_ok:
                    QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
                else:
                    QBtn = QDialogButtonBox.Cancel

                self.buttonBox = QDialogButtonBox(QBtn)
                self.buttonBox.accepted.connect(self.accept)
                self.buttonBox.rejected.connect(self.reject)

                self.layout = QVBoxLayout()
                message = QLabel(self.text)
                self.layout.addWidget(message)
                self.layout.addWidget(self.buttonBox)

                if self.mode == "Save ws":
                    self.ask_for_name = QLabel(self)
                    self.ask_for_name.setText("Enter workspace name:")
                    self.name = QLineEdit(self)
                    self.name.textChanged.connect(self.get_save_data)

                    self.ask_for_description = QLabel(self)
                    self.ask_for_description.setText("Enter workspace description:")
                    self.description = QLineEdit(self)
                    self.description.textChanged.connect(self.get_save_data)

                    self.layout.addWidget(self.ask_for_name)
                    self.layout.addWidget(self.name)
                    self.layout.addWidget(self.ask_for_description)
                    self.layout.addWidget(self.description)
                elif self.mode == "Get ws":
                    self.ws_list = QComboBox(self)

                    for el in self.shared:
                        self.ws_list.addItem(el["title"])
                    self.choose_ws()

                    self.ws_list.activated.connect(lambda: self.choose_ws())

                    self.layout.addWidget(self.ws_list)

                self.setLayout(self.layout)
                self.setWindowTitle(self.title)

                # Load stylesheet from DevSec Studio (protected by MIT LICENSE)
                ssh_file = path_to_file("themes", "SpyBot.qss")
                with open(ssh_file, "r") as fh:
                    self.setStyleSheet(fh.read())

            def get_save_data(self):
                self.out["title"] = self.name.text()
                self.out["description"] = self.description.text()

            def choose_ws(self):
                self.out["title"] = self.ws_list.currentText()

        def __init__(self, parentwindow=None):
            super().__init__()
            self.parentwindow = parentwindow
            self.setMouseTracking(True)
            self.btn1_drawcoards = []
            self.btn1_wait_to_click = -1
            self.btn2_drawcoards = []
            self.btn2_wait_to_click = -1
            self.btn5_wait_to_click = -1
            self.btn7_wait_to_click = -1
            self.render_objects = [[], [], []]
            self.object_history = []
            self.selected = None
            self.patterns = [Qt2.Dense1Pattern, Qt2.Dense2Pattern, Qt2.Dense3Pattern, Qt2.Dense4Pattern,
                             Qt2.Dense5Pattern, Qt2.Dense6Pattern, Qt2.Dense7Pattern]
            self.btn7_drawcoards = []
            self.current_patt = random.choice(self.patterns)
            self.angle = 1
            self.ignore_rotate = False
            self.mouse_btn = 0
            self.keys = []
            self.mouse_tracking = False
            self.moving = None
            self.hidden = None
            self.colors = {"red": Qt2.darkRed, "green": Qt2.darkGreen, "blue": Qt2.darkBlue, "cyan": Qt2.darkCyan,
                           "white": Qt2.white, "grey": Qt2.darkGray, "transparent": Qt2.transparent}
            self.colorsback1 = [Qt2.darkRed, Qt2.darkGreen, Qt2.darkBlue, Qt2.darkCyan, Qt2.white, Qt2.darkGray,
                                Qt2.transparent]
            self.colorsback2 = ["red", "green", "blue", "cyan", "white", "grey",
                                "transparent"]
            self.initUI()

        def initUI(self):
            uic.loadUi(path_to_file("uis", "third_window.ui"), self)
            self.mousepos.setText("Координаты: None, None")
            self.mousebtn.setText("")
            self.btn1.setText("Линия")
            self.btn2.setText("Прямоугольник")
            # self.btn3.setText("Отмена")
            self.btn4.setText("Очистка")
            self.btn5.setText("Сохранить")
            self.btn6.setText("Загрузить")
            self.btn7.setText("Удалить")
            self.sandbox.setText("")
            self.btn1.clicked.connect(lambda: self.btn1_click())
            self.btn2.clicked.connect(lambda: self.btn2_click())
            # self.btn3.clicked.connect(lambda: self.btn3_click())
            self.btn4.clicked.connect(lambda: self.btn4_click())
            self.btn5.clicked.connect(lambda: self.btn5_click())
            self.btn6.clicked.connect(lambda: self.btn6_click())
            self.btn7.clicked.connect(lambda: self.btn7_click())
            self.dial.setMinimum(0)
            self.dial.setMaximum(359)
            self.dial.setValue(0)
            self.spinBox.setMinimum(0)
            self.spinBox.setMaximum(359)
            self.spinBox.setValue(0)
            self.dial.valueChanged.connect(lambda: self.rotate_changed())
            self.spinBox.valueChanged.connect(self.rotate2_changed)
            self.colorbox.activated.connect(self.colorchange2)
            for i in self.colors:
                self.colorbox.addItem(i)
            self.colorbox.setCurrentIndex(5)
            self.dial.hide()
            self.colorbox.hide()
            self.spinBox.hide()
            self.btn3.hide()

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
                qp.setBrush(QBrush(Qt2.darkGray, Qt2.SolidPattern))
                qp.setPen(QPen(Qt2.black, 3, Qt2.SolidLine))
                if i == self.selected and i != self.hide:
                    qp.setPen(QPen(Qt2.black, 5, Qt2.DotLine))
                    qp.setBrush(QBrush(Qt2.lightGray, Qt2.DiagCrossPattern))
                    if len(i) == 3:
                        if i[2] == -1:
                            qp.setBrush(QBrush(Qt2.transparent, Qt2.DiagCrossPattern))
                        else:
                            qp.setBrush(QBrush(QColor(i[2]), Qt2.DiagCrossPattern))
                    self.drawRect(i[0], i[1], qp)
                elif i != self.hide:
                    if len(i) == 3:
                        if i[2] == -1:
                            qp.setBrush(QBrush(Qt2.transparent, Qt2.SolidPattern))
                        else:
                            qp.setBrush(QBrush(QColor(i[2]), Qt2.SolidPattern))
                    qp.setPen(QPen(Qt2.black, 3, Qt2.SolidLine))
                    self.drawRect(i[0], i[1], qp)
                    self.update()

            qp.setPen(QPen(Qt2.black, 3, Qt2.DashDotLine))

            if len(self.btn1_drawcoards) == 2:
                qp.drawLine(*self.transform_coards_for_line(self.btn1_drawcoards))

            qp.setBrush(QBrush(Qt2.darkGray, self.current_patt))

            if len(self.btn2_drawcoards) == 2:
                qp.drawRect(*self.transform_coards_for_rect(self.btn2_drawcoards))

            qp.setBrush(QBrush())
            qp.setPen(QPen(Qt2.red, 2, Qt2.DashLine))

            if len(self.btn7_drawcoards) == 2:
                qp.drawRect(*self.transform_coards_for_rect(self.btn7_drawcoards))

            qp.setBrush(QBrush())
            qp.setPen(QPen(Qt2.black, 3, Qt2.DashDotLine))
            if self.moving is not None:
                qp.setPen(QPen(Qt2.black, 5, Qt2.DotLine))
                qp.setBrush(QBrush(Qt2.lightGray, Qt2.DiagCrossPattern))
                if len(self.moving) == 3:
                    if self.moving[2] == -1:
                        qp.setBrush(QBrush(Qt2.transparent, Qt2.DiagCrossPattern))
                    else:
                        qp.setBrush(QBrush(QColor(self.moving[2]), Qt2.DiagCrossPattern))
                self.drawRect(self.moving[0], self.moving[1], qp)

        def rotate_rect_coards(self, center, w, h, angle):
            ans = [[], [], [], []]
            a = radians(angle)
            ans[0] = [(cos(a) * w - sin(a) * h) / 2 + center[0], (sin(a) * w + cos(a) * h) / 2 + center[1]]
            ans[1] = [(cos(a) * (-w) - sin(a) * h) / 2 + center[0], (sin(a) * (-w) + cos(a) * h) / 2 + center[1]]
            ans[2] = [(cos(a) * (-w) - sin(a) * (-h)) / 2 + center[0], (sin(a) * (-w) + cos(a) * (-h)) / 2 + center[1]]
            ans[3] = [(cos(a) * w - sin(a) * (-h)) / 2 + center[0], (sin(a) * w + cos(a) * (-h)) / 2 + center[1]]
            return ans

        def rotate_rect(self, rect, angle):
            '''
            :param rect: 4 points of not rotated rect
            :param angle: angle of rotation
            :return: 4 points of rotated rect
            '''
            j = [[(rect[1][0] + rect[0][0]) / 2, (rect[1][1] + rect[2][1]) / 2], rect[1][0] - rect[0][0],
                 rect[1][1] - rect[2][1], angle]
            j = self.rotate_rect_coards(*j)
            for h in range(len(j)):
                j[h] = [int(j[h][0]), int(j[h][1])]
            return j

        def drawRect(self, rect, angle, painter):
            '''

            :param rect: 4 points of rect
            :param angle: rotation angle of rect
            :param painter: qpainter
            :return:
            '''
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
            '''
            :param rect: 2 points of rect
            :return: sorted 4 points of rect
            '''
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
            self.btn7_wait_to_click = -1
            self.selected = None
            self.dial.hide()
            self.colorbox.hide()
            self.spinBox.hide()

        def btn1_click(self):
            # print("mode: LINE")
            self.flag_down()
            if self.btn1_wait_to_click == -1:
                self.btn1_wait_to_click = 0
            self.update()

        def btn2_click(self):
            # print("mode: RECT")
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
                        # print(f"{'LINE' if self.object_history[-1][0] == 1 else 'RECT'} deleted")
                        self.object_history.pop()

                    elif self.object_history[-1][0] == "rotated":
                        self.render_objects[2][self.render_objects[2].index(self.object_history[-1][2])][1] = 0
                        self.object_history.pop()
                        self.ignore_rotate = True
                        self.dial.setValue(0)
                        self.ignore_rotate = False

                    elif self.object_history[-1][0] == "moved":
                        self.render_objects[2][self.render_objects[2].index(self.object_history[-1][0][2])] = \
                            self.object_history[-1][0][1]
                        self.object_history.pop()

            except:
                logger.exception("Tracked exception occurred!")
            finally:
                if co == len(self.object_history) and co != 0:
                    self.object_history.pop()

            self.update()

        def colorchange(self, value):
            mapped_value = int(value / 100 * 5)
            colors = [Qt2.black, Qt2.darkGray, Qt2.gray, Qt2.lightGray, Qt2.white]
            if len(self.render_objects[2][self.render_objects[2].index(self.selected)]) == 2:
                self.render_objects[2][self.render_objects[2].index(self.selected)].append(colors[mapped_value])
            elif len(self.render_objects[2][self.render_objects[2].index(self.selected)]) == 3:
                self.render_objects[2][self.render_objects[2].index(self.selected)][2] = colors[mapped_value]

        def colorchange2(self):
            color = self.colors[self.colorbox.currentText()]
            if len(self.render_objects[2][self.render_objects[2].index(self.selected)]) == 2:
                self.render_objects[2][self.render_objects[2].index(self.selected)].append(color)
            elif len(self.render_objects[2][self.render_objects[2].index(self.selected)]) == 3:
                self.render_objects[2][self.render_objects[2].index(self.selected)][2] = color

        def btn4_click(self):
            rs = self.Dialog("Вы уверены, что хотите очистить экран?", "Очистка", show_button_ok=True).exec()
            if rs:
                self.btn1_drawcoards = []
                self.render_objects = [[self.transform_coards_for_rect(self.mouse_in_widget([0, 0], self.sandbox)[:2]),
                                        [220, 220, 220]], [], []]
                self.btn1_wait_to_click = -1
                self.object_history = []
                self.update()
                # print("cleaned")

        def btn5_click(self):
            shared = {}
            rs = self.Dialog("Вы уверены, что хотите сохранить холст?", "Сохранение", mode="Save ws", out=shared,
                             show_button_ok=True).exec()
            buf = deepcopy(self.render_objects)
            if rs:
                for i in range(len(buf[2])):
                    if len(buf[2][i]) == 2:
                        buf[2][i].append("grey")
                    elif len(buf[2][i]) == 3:
                        buf[2][i][2] = self.colorsback2[self.colorsback1.index(buf[2][i][2])]

                data = {
                    "render_objects": buf,
                    "object_history": self.object_history
                }
                try:
                    shared["filename"] = shared["title"] + ".json"
                    with open(path_to_userdata(shared["filename"], str(user.get_user_id())), "w") as file:
                        json.dump(data, file)
                        user.add_workspace(shared["title"], shared["filename"], shared["description"])
                except NameError:
                    logger.exception("Tracked exception occurred!")

        def btn6_click(self):
            shared = user.get_workspaces()
            out = {}
            rs = self.Dialog("Вы уверены, что хотите загрузить сохранение?", "Сохранение", mode="Get ws", shared=shared,
                             out=out, show_button_ok=True).exec()
            if rs:
                try:
                    self.flag_down()
                    ws = user.get_workspace(out["title"])
                    with open(path_to_userdata(ws["file"], str(user.get_user_id())), "r") as file:
                        data = json.load(file)
                        buf = data["render_objects"]
                        for i in range(len(buf[2])):
                            buf[2][i] = buf[2][i][:2] + [self.colors[buf[2][i][2]]]
                        self.object_history = data["object_history"]
                        self.render_objects = deepcopy(buf)
                except (FileNotFoundError, AttributeError):
                    logger.exception("Tracked exception occurred!")
                    self.Dialog("Не найдено сохранение или оно некорректно", "Сохранение").exec()

        def btn7_click(self):
            self.flag_down()
            if self.btn7_wait_to_click == -1:
                self.btn7_wait_to_click = 0
            self.update()

        def delete_selected(self):
            # print("mode: DELETE")

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
                    while self.RectAndWidgetCollision(self.rotate_rect(self.selected[0], val),
                                                      self.sandbox) or self.RectAnfRenderObjCollision(
                        self.rotate_rect(self.selected[0], val), self.render_objects):
                        val -= 1
                    if val < 0:
                        val = 360 - val
                    self.render_objects[2][self.render_objects[2].index(self.selected)][1] = val
                    self.selected[1] = val
                    self.spinBox.setValue(val)
                    self.dial.setValue(val)
                    if self.object_history[-1][0] == "rotated" and self.object_history[-1][2][0] == self.selected[0]:
                        self.object_history.pop()
                    self.object_history.append(["rotated", self.dial.value(), self.selected])
                else:
                    self.spinBox.setValue(0)
                    self.dial.setValue(0)
            except:
                logger.exception("Tracked exception occurred!")
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
            '''
            :param rect: 4 points of rect
            :return: sorted 4 points
            '''
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
            '''
            :param rect: 4 points of rect
            :param coards: point
            :return: True if point in rect else False
            '''
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

        def ProjectVertices(self, rect, o):
            mi = 10 ** 9
            ma = -10 ** 9
            for i in rect:
                proj = self.dot(i, o)
                mi = min(mi, proj)
                ma = max(ma, proj)
            return [mi, ma]

        def RectAndRectCollision(self, rect1, rect2):
            '''
            :param rect1: 4 points of rect
            :param rect2: 4 points of rect
            :return: True if rects have a collision else False
            '''
            for i in [3, 1]:
                o = [rect1[0][0] - rect1[i][0], rect1[0][1] - rect1[i][1]]
                proj1 = self.ProjectVertices(rect1, o)
                proj2 = self.ProjectVertices(rect2, o)
                if proj1[0] >= proj2[1] or proj2[0] >= proj1[1]:
                    return False
            for i in [3, 1]:
                o = [rect2[0][0] - rect2[i][0], rect2[0][1] - rect2[i][1]]
                proj1 = self.ProjectVertices(rect1, o)
                proj2 = self.ProjectVertices(rect2, o)
                if proj1[0] >= proj2[1] or proj2[0] >= proj1[1]:
                    return False
            return True

        def RectAndLineCollision(self, rect, line):
            '''
            :param rect: 4 points of rect
            :param line: 2 points of line
            :return: True if rect and line have a collision else False
            '''
            for i in [3, 1]:
                o = [rect[0][0] - rect[i][0], rect[0][1] - rect[i][1]]
                proj1 = self.ProjectVertices(rect, o)
                proj2 = self.ProjectVertices(line, o)
                if proj1[0] >= proj2[1] or proj2[0] >= proj1[1]:
                    return False
            o = [-(line[1][1] - line[0][1]), line[1][0] - line[0][0]]
            proj1 = self.ProjectVertices(line, o)
            proj2 = self.ProjectVertices(rect, o)
            if proj1[0] >= proj2[1] or proj2[0] >= proj1[1]:
                return False
            return True

        def RectAnfRenderObjCollision(self, rect, renderobjects):
            '''
            :param rect: 4 points of ret
            :param renderobjects: list of objects
            :return: True if rect and some objects have a collision else False
            '''
            for i in renderobjects[2]:
                if len(i) >= 2 and i != self.hide and i != self.selected:
                    i = self.rotate_rect(i[0], i[1])
                    if self.RectAndRectCollision(rect, i):
                        return True
            for i in renderobjects[1]:
                if len(i) == 4:
                    i = [[i[0], i[1]], [i[2], i[3]]]
                    if self.RectAndLineCollision(rect, i):
                        return True

            return False

        def RectAndWidgetCollision(self, rect, widget):
            '''
            :param rect: 4 points of ret
            :param renderobjects: Qtwidget
            :return: True if rect and widger have a collision else False
            '''
            t = []
            window_metrix = self.get_widget_metrix(widget)
            for i in range(len(rect)):
                t.append(window_metrix[0][0] <= rect[i][0] <= window_metrix[1][0])
                t.append(window_metrix[0][1] <= rect[i][1] <= window_metrix[1][1])
            return not all(t)

        def select_rect(self, rects, mouse_coards):
            '''
            :param rects: list of rects
            :param mouse_coards: mousecoards
            :return: rect which has a collision with mousecoards
            '''
            for i in rects[::-1]:
                if self.inRect(self.rotate_rect(i[0], i[1]), mouse_coards):
                    return i

        def moose_set_in_widget(self, mouse_coards, qwidget):
            gp = qwidget.mapToGlobal(QtCore.QPoint(0, 0))
            widget = gp.x(), gp.y()
            window = (self.x(), self.y()) if not self.parentwindow else (self.parentwindow.x(), self.parentwindow.y())
            widget_coards = (widget[0] - window[0], widget[1] - window[1])
            widget_size = (qwidget.geometry().width(), qwidget.geometry().height())
            widget_coards2 = (widget_coards[0] + widget_size[0], widget_coards[1] + widget_size[1])
            mouse_in_widget = self.setInRange(widget_coards, widget_coards2, mouse_coards)
            return mouse_in_widget

        def mouse_in_widget(self, mouse_coards, qwidget):
            '''
            :param mouse_coards: mousecoards
            :param qwidget: Qwidget
            :return: True if mouse in widget
            '''
            gp = qwidget.mapToGlobal(QtCore.QPoint(0, 0))
            widget = gp.x(), gp.y()
            window = (self.x(), self.y()) if not self.parentwindow else (self.parentwindow.x(), self.parentwindow.y())
            widget_coards = (widget[0] - window[0], widget[1] - window[1])
            widget_size = (qwidget.geometry().width(), qwidget.geometry().height())
            widget_coards2 = (widget_coards[0] + widget_size[0], widget_coards[1] + widget_size[1])
            return [widget_coards, widget_coards2, widget_size, mouse_coards,
                    self.inRange(widget_coards, widget_coards2, mouse_coards)]

        def get_widget_metrix(self, qwidget):
            '''
            :param qwidget: Qwidget
            :return: widget params
            '''
            gp = qwidget.mapToGlobal(QtCore.QPoint(0, 0))
            widget = gp.x(), gp.y()
            window = (self.x(), self.y()) if not self.parentwindow else (self.parentwindow.x(), self.parentwindow.y())
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

        def area(self, rect):
            '''
            :param rect: 4 points of not rotated rect
            :return: area of rect
            '''
            return abs(rect[0][0] - rect[1][0]) * abs(rect[0][1] - rect[3][1])

        def line_len(self, line):
            '''
            :param line: 2 points of line
            :return: len of line
            '''
            return ((line[0] - line[2]) ** 2 + (line[1] - line[3]) ** 2) ** 0.5

        def keyPressEvent(self, event):
            if event.key() in [Qt2.Key_Delete, Qt2.Key_Backspace]:
                self.delete_selected()
            # if event.key() == Qt2.Key_Z and Qt2.Key_Control in self.keys:
            #     self.btn3_click()
            if event.key() == Qt2.Key_Escape:
                self.flag_down()
                self.selected = None
                self.hide = None
                self.moving = None
                self.mouse_tracking = False
                self.btn2_drawcoards = []
                self.btn1_drawcoards = []
                self.btn1_wait_to_click = -1
                self.btn2_wait_to_click = -1
                self.btn7_wait_to_click = -1
                self.btn7_drawcoards = []

            self.keys.append(event.key())
            if self.selected is None:
                self.dial.hide()
                self.colorbox.hide()
                self.spinBox.hide()
            else:
                self.dial.show()
                self.colorbox.show()
                self.spinBox.show()
            self.update()

        def keyReleaseEvent(self, event):
            try:
                del self.keys[self.keys.index(event.key())]
            except:
                logger.exception("Tracked exception occurred!")

        def mouseMoveEvent(self, event):
            mouse_coards = (event.x(), event.y())
            mouse_btn = event.button()
            self.render_objects[0] = [self.transform_coards_for_rect(self.mouse_in_widget([0, 0], self.sandbox)[:2]),
                                      [220, 220, 220]]
            if len(self.btn1_drawcoards) == 2:
                self.btn1_drawcoards[1] = self.moose_set_in_widget(mouse_coards, self.sandbox)

            if len(self.btn2_drawcoards) == 2:
                self.btn2_drawcoards[1] = self.moose_set_in_widget(mouse_coards, self.sandbox)

            if len(self.btn7_drawcoards) == 2:
                self.btn7_drawcoards[1] = self.moose_set_in_widget(mouse_coards, self.sandbox)

            if self.selected is not None and self.mouse_btn == 2 and self.mouse_tracking:
                buf = deepcopy(self.render_objects[2][self.render_objects[2].index(self.selected)])
                dx, dy = mouse_coards[0] - self.start_coards[0], mouse_coards[1] - self.start_coards[1]
                buf[0] = [[buf[0][0][0] + dx, buf[0][0][1] + dy], [buf[0][1][0] + dx, buf[0][1][1] + dy],
                          [buf[0][2][0] + dx, buf[0][2][1] + dy], [buf[0][3][0] + dx, buf[0][3][1] + dy]]
                self.hide = deepcopy(self.render_objects[2][self.render_objects[2].index(self.selected)])
                if not self.RectAndWidgetCollision(self.rotate_rect(buf[0], buf[1]),
                                                   self.sandbox) and not self.RectAnfRenderObjCollision(
                    self.rotate_rect(buf[0], buf[1]), self.render_objects):
                    self.moving = buf
                else:
                    pass

            self.mousepos.setText(f"Координаты: {event.x()}, {event.y()}")
            self.update()

        def mousePressEvent(self, event):
            self.ignore_rotate = True
            self.dial.setValue(0)
            self.ignore_rotate = False
            mouse_coards = [event.x(), event.y()]
            self.mouse_btn = event.button()
            mouse_in_sandbox = self.mouse_in_widget(mouse_coards, self.sandbox)[-1]
            self.render_objects[0] = [self.transform_coards_for_rect(self.mouse_in_widget([0, 0], self.sandbox)[:2]),
                                      [220, 220, 220]]
            if self.btn1_wait_to_click in [0] and mouse_in_sandbox and self.mouse_btn == 1:
                self.selected = None
                if self.btn1_wait_to_click == 0:
                    self.btn1_drawcoards = [mouse_coards, mouse_coards]
                    self.btn1_wait_to_click = 1
                    # print(f"starting drawing LINE from ({mouse_coards[0]}, {mouse_coards[1]})")

            if self.btn2_wait_to_click in [0] and mouse_in_sandbox and self.mouse_btn == 1:
                if self.btn2_wait_to_click == 0:
                    self.selected = None
                    self.current_patt = random.choice(self.patterns)
                    self.btn2_drawcoards = [mouse_coards, mouse_coards]
                    self.btn2_wait_to_click = 1
                    # print(f"starting drawing RECT from ({mouse_coards[0]}, {mouse_coards[1]})")

            if self.btn7_wait_to_click in [0] and mouse_in_sandbox and self.mouse_btn == 1:
                if self.btn7_wait_to_click == 0:
                    self.selected = None
                    self.btn7_drawcoards = [mouse_coards, mouse_coards]
                    self.btn7_wait_to_click = 1
                    # print(f"starting drawing DELETERECT from ({mouse_coards[0]}, {mouse_coards[1]})")

            if self.mouse_btn == 2 and mouse_in_sandbox and [self.btn1_drawcoards, self.btn2_drawcoards,
                                                             self.btn7_drawcoards] == [[], [], []]:

                buf = self.select_rect(self.render_objects[2], mouse_coards)

                if buf == self.selected:
                    self.mouse_tracking = True
                    self.start_coards = mouse_coards
                else:
                    self.mouse_tracking = False

                self.selected = self.select_rect(self.render_objects[2], mouse_coards)

                if self.selected is not None and len(self.selected) == 3:
                    self.colorbox.setCurrentIndex(list(self.colors.values()).index(self.selected[2]))
                else:
                    self.colorbox.setCurrentIndex(list(self.colors.values()).index(Qt2.darkGray))

                if self.selected is not None:
                    self.update()
                    self.dial.show()
                    self.colorbox.show()
                    self.spinBox.show()
                    self.dial.setValue(self.selected[1])
                    self.update()
                    # print(f"selected RECT {self.selected} with number {self.render_objects[2].index(self.selected)}")
                else:
                    # print("nothing selected")
                    pass
            if self.selected is None:
                self.dial.hide()
                self.colorbox.hide()
                self.spinBox.hide()
            else:
                self.dial.show()
                self.colorbox.show()
                self.spinBox.show()

            self.update()

            self.mousepos.setText(f"Координаты:{event.x()}, {event.y()}")
            # if (event.button() == Qt2.LeftButton):
            #     self.mousebtn.setText("Левая")
            # elif (event.button() == Qt2.RightButton):
            #     self.mousebtn.setText("Правая")

        def mouseReleaseEvent(self, event):
            mouse_coards = [event.x(), event.y()]
            mouse_btn = event.button()
            self.mouse_btn = 0

            if mouse_btn == 1 and len(self.btn1_drawcoards) == 2:
                flag = True
                line = self.transform_coards_for_line(self.btn1_drawcoards)
                # print(self.line_len(line))
                if self.line_len(line) > 100:
                    line = [[line[0], line[1]], [line[2], line[3]]]
                    for i in self.render_objects[2]:
                        if self.RectAndLineCollision(self.rotate_rect(i[0], i[1]), line):
                            flag = False
                    if flag:
                        self.render_objects[1].append(self.transform_coards_for_line(self.btn1_drawcoards))
                        # print(
                        #     f"drawn LINE from ({self.render_objects[1][-1][0]}, {self.render_objects[1][-1][1]}) to ({self.render_objects[1][-1][2]}, {self.render_objects[1][-1][3]})")
                        self.object_history.append([1, self.transform_coards_for_line(self.btn1_drawcoards)])
                self.btn1_drawcoards = []
                self.btn1_wait_to_click = 0

            if mouse_btn == 1 and len(self.btn2_drawcoards) == 2:
                rect = [self.get_all_points(self.btn2_drawcoards), 0]
                if self.area(rect[0]) > 500:
                    if not self.RectAnfRenderObjCollision(rect[0], self.render_objects):
                        self.render_objects[2].append([self.get_all_points(self.btn2_drawcoards), 0, Qt2.darkGray])
                        # print(
                        #     f"drawn RECT ({self.render_objects[2][-1][0][0]}, {self.render_objects[2][-1][0][1]}, {self.render_objects[2][-1][0][2]}, {self.render_objects[2][-1][0][3]})")
                        self.object_history.append([2, [self.get_all_points(self.btn2_drawcoards), 0]])
                self.btn2_drawcoards = []
                self.btn2_wait_to_click = 0

            if mouse_btn == 1 and len(self.btn7_drawcoards) == 2:
                rect = [self.get_all_points(self.btn7_drawcoards), 0]
                buf = [[], [], []]
                buf[0] = deepcopy(self.render_objects[0])
                for i in self.render_objects[2]:
                    if len(i) >= 2 and i != self.hide and i != self.selected:
                        j = self.rotate_rect(i[0], i[1])
                        if not self.RectAndRectCollision(rect[0], j):
                            buf[2].append(self.render_objects[2][self.render_objects[2].index(i)])

                for i in self.render_objects[1]:
                    if len(i) == 4:
                        j = [[i[0], i[1]], [i[2], i[3]]]
                        if not self.RectAndLineCollision(rect[0], j):
                            buf[1].append(self.render_objects[1][self.render_objects[1].index(i)])

                self.render_objects = deepcopy(buf)
                self.btn7_drawcoards = []
                self.btn7_wait_to_click = -1

            if self.moving and self.mouse_tracking:
                self.mouse_tracking = False
                self.object_history.append(
                    ["moved", self.render_objects[2][self.render_objects[2].index(self.selected)], self.moving])
                self.render_objects[2][self.render_objects[2].index(self.selected)] = self.moving
                self.moving = None
                self.hide = None
                self.selected = None

            if self.selected is None:
                self.dial.hide()
                self.colorbox.hide()
                self.spinBox.hide()
            else:
                self.dial.show()
                self.colorbox.show()
                self.spinBox.show()

            # self.mousebtn.setText("Никакая")
            self.update()

    def __init__(self, parentwindow=None):
        super().__init__()
        self.ui = self.DrawWindow(parentwindow)

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
