import colorsys
import math

from PySide import QtGui
from PySide.QtCore import QRect
from PySide.QtGui import QPen, QBrush, QColor

from population_graph_window_ui import Ui_PopulationGraphWidget

CHILDREN_TO_BE_RED = 10


def get_color(children_count):
    ratio = min(1.0, float(children_count) / CHILDREN_TO_BE_RED)
    hue = 0.34 - 0.34 * ratio
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return QColor(int(r*255), int(g*255), int(b*255))


def qcircle(x, y, r):
    return QRect(x-r, y-r, r*2, r*2)


class PopulationGraphWindow(Ui_PopulationGraphWidget, QtGui.QMainWindow):
    agent_size = 10
    padding = 10
    connection_pen = QPen(QColor(0,0,0), 1)
    agent_brush = QBrush(QColor(120, 120, 120))

    def __init__(self, world, selected_animal=None, parent=None):
        super().__init__(parent=parent)
        self.world = world
        self._selected_animal = selected_animal
        self.info = []
        self._cols = 1
        self._rows = 1

        self.setupUi(self)
        self.draw_widget.paintEvent = self.on_draw_widget_paintEvent
        self.draw_widget.mousePressEvent = self.on_draw_widget_mousePressEvent

    def redraw(self):
        self.draw_widget.repaint()

        self.info.append("generations: {}".format(self._rows))
        children = len(self.selected_animal.children) if self.selected_animal else 0
        self.info.append("children: {}".format(children))
        self.info_label.setText('\n'.join(self.info))
        self.info.clear()

        self.set_new_draw_widget_size(self._rows, self._cols)

    def on_draw_widget_paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self.draw_widget)
        qp.setPen(self.connection_pen)
        qp.setBrush(self.agent_brush)
        for i, generation in enumerate(self.generation_iterator(self.world)):
            for j, animal in enumerate(generation):
                x = (self.agent_size + self.padding) * j
                y = (self.agent_size + self.padding) * i

                qp.setBrush(QBrush(get_color(len(animal.children))))
                qp.drawEllipse(QRect(x, y, self.agent_size, self.agent_size))
                x += self.agent_size // 2
                y += self.agent_size // 2
                animal._drawing_position = (x, y)

                if self.all_radio_button.isChecked():
                    for parent in animal.parents:
                        if hasattr(parent, '_drawing_position'):
                            qp.drawLine(x, y, *parent._drawing_position)
                self._cols = max(self._cols, j)

        if self.selected_animal:
            qp.setPen(QPen(QColor(255, 180, 0), 3))
            qp.setBrush(QBrush(get_color(len(self.selected_animal.children))))
            qp.drawEllipse(qcircle(*self.selected_animal._drawing_position, self.agent_size))

            qp.setPen(QPen(QColor(0, 0, 0), 1))
            qp.setBrush(QBrush(QColor(100, 100, 250)))
            qp.drawEllipse(qcircle(*self.selected_animal._drawing_position, 2))
            depth = self.depth_spinbox.value() or -1
            if self.ancestors_radio_button.isChecked():
                self.draw_ancestors_connections(qp, self.selected_animal, depth)
            elif self.successors_radio_button.isChecked():
                self.draw_successors_connections(qp, self.selected_animal, depth)

        qp.end()

        self._rows = i

    def set_new_draw_widget_size(self, rows, cols):
        self.draw_widget.setFixedWidth((cols + 1) * (self.agent_size + self.padding))
        self.draw_widget.setFixedHeight((rows+1) * (self.agent_size + self.padding))

    def draw_ancestors_connections(self, qp, animal, depth, drawn=None):
        """Draw all ancestors with given depth. If depth is negative - draw without depth limit"""
        if depth == 0:
            return
        drawn = drawn or dict()
        drawn[animal] = depth
        for parent in animal.parents:
            if hasattr(animal, '_drawing_position') and hasattr(parent, '_drawing_position'):
                qp.drawLine(*animal._drawing_position, *parent._drawing_position)
                qp.drawEllipse(qcircle(*parent._drawing_position, 2))
                if depth < 0 and parent in drawn:
                    continue
                if parent not in drawn or drawn[parent] < depth - 1:
                    self.draw_ancestors_connections(qp, parent, depth-1, drawn)

    def draw_successors_connections(self, qp, animal, depth, drawn=None):
        """Draw all successors with given depth. If depth is negative - draw without depth limit"""
        if depth == 0:
            return
        drawn = drawn or dict()
        drawn[animal] = depth
        for child in animal.children:
            if hasattr(animal, '_drawing_position') and hasattr(child, '_drawing_position'):
                if self.draw_lines_checkbox.isChecked():
                    qp.drawLine(*animal._drawing_position, *child._drawing_position)
                qp.drawEllipse(qcircle(*child._drawing_position, 2))
                if depth < 0 and child in drawn:
                    continue
                if child not in drawn or drawn[child] < depth - 1:
                    self.draw_successors_connections(qp, child, depth-1, drawn)

    def generation_iterator(self, world):
        current = set(world.first_generation)
        drawn = set()
        while current:
            yield current.copy()
            drawn.update(current)

            prev, current = current, set()
            for animal in prev:
                for child in animal.children:
                    if not set(child.parents).difference(drawn):
                        current.add(child)

    def on_draw_widget_mousePressEvent(self, event):
        for generation in self.generation_iterator(self.world):
            for animal in generation:
                if hasattr(animal, '_drawing_position') and self._close_enogh(event.x(), event.y(), *animal._drawing_position, self.agent_size):
                    self.selected_animal = animal
                    return
        self.selected_animal = None

    def _close_enogh(self, x1, y1, x2, y2, radius):
        return math.hypot(x1 - x2, y1 - y2) < radius

    @property
    def selected_animal(self):
        return self._selected_animal

    @selected_animal.setter
    def selected_animal(self, value):
        self._selected_animal = value
        self.repaint()
