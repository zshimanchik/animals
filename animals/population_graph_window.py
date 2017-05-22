import colorsys

from PySide import QtGui
from PySide.QtCore import QRect, Qt
from PySide.QtGui import QPen, QBrush, QColor

CHILDREN_TO_BE_RED = 10


def get_color(children_count):
    ratio = min(1.0, float(children_count) / CHILDREN_TO_BE_RED)
    hue = 0.34 - 0.34 * ratio
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return QColor(int(r*255), int(g*255), int(b*255))


def qcircle(x, y, r):
    return QRect(x-r, y-r, r*2, r*2)


class PopulationGraphWindow(QtGui.QMainWindow):
    agent_size = 10
    padding = 10
    connection_pen = QPen(QColor(0,0,0), 1)
    agent_brush = QBrush(QColor(120, 120, 120))

    def __init__(self, world, selected_animal=None, parent=None):
        super().__init__(parent=parent)
        self.world = world
        self.selected_animal = selected_animal

        self.central_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle("Population Graph")
        self.resize(700, 300)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
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

                if not self.selected_animal:
                    for parent in animal.parents:
                        if hasattr(parent, '_drawing_position'):
                            qp.drawLine(x, y, *parent._drawing_position)

        if self.selected_animal:
            qp.setBrush(QBrush(QColor(100, 100, 250)))
            qp.drawEllipse(qcircle(*self.selected_animal._drawing_position, 2))
            self.draw_ancestors_connections(qp, self.selected_animal)
            # self.draw_successors_connections(qp, self.selected_animal)
        qp.end()

    def draw_ancestors_connections(self, qp, animal):
        for parent in animal.parents:
            if hasattr(animal, '_drawing_position') and hasattr(parent, '_drawing_position'):
                qp.drawLine(*animal._drawing_position, *parent._drawing_position)
                qp.drawEllipse(qcircle(*parent._drawing_position, 2))
                self.draw_ancestors_connections(qp, parent)

    def draw_successors_connections(self, qp, animal):
        for child in animal.children:
            if hasattr(animal, '_drawing_position') and hasattr(child, '_drawing_position'):
                qp.drawLine(*animal._drawing_position, *child._drawing_position)
                qp.drawEllipse(qcircle(*child._drawing_position, 2))
                self.draw_successors_connections(qp, child)


    def generation_iterator(self, world):
        current = set(world.first_generation)
        drawed = set()
        while current:
            yield current.copy()
            drawed.update(current)

            prev, current = current, set()
            for animal in prev:
                for child in animal.children:
                    if not set(child.parents).difference(drawed):
                        current.add(child)