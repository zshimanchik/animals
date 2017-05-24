import collections

from PySide import QtGui
from PySide.QtCore import QRect, Qt
from PySide.QtGui import QPen, QBrush, QColor

from graphics_window_ui import Ui_graphics_window


def get_color(color):
    r, g, b = max(0, -color), max(0, color), 0
    return QColor(r * 255, g * 255, b * 255)


class GraphicsWindow(Ui_graphics_window, QtGui.QMainWindow):
    def __init__(self, world, parent=None):
        super().__init__(parent=parent)
        self.world = world

        self.setupUi(self)
        self.population_widget.paintEvent = self.on_population_widget_paintEvent
        self.food_widget.paintEvent = self.on_food_widget_paintEvent
        self.population_widget.resizeEvent = self.population_widget_resizeEvent

    def population_widget_resizeEvent(self, event):
        # I know that this method evoke too often...
        self.population.scale = self.population_widget.height() / 100.0
        self.food.scale = self.food_widget.height() / 250.0

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, value):
        self._world = value
        self.population = Graphic(freq=50, scale=2, maxlen=None)
        self.food = Graphic(freq=50, scale=1, maxlen=None)

    def update(self):
        self.population.update(len(self.world.animals))
        self.food.update(len(self.world.food))

        width = max(len(self.population), self.scrollArea.width()-10)
        self.scrollAreaWidgetContents.setFixedWidth(width)

        bar= self.scrollArea.horizontalScrollBar()
        if bar.maximum() - bar.value() < 100:
            bar.setValue(bar.maximum())

        self.population_widget.repaint()
        self.food_widget.repaint()

    def on_population_widget_paintEvent(self, event):
        self.draw_graphic(self.population_widget, self.population, text='population')

    def on_food_widget_paintEvent(self, event):
        self.draw_graphic(self.food_widget, self.food, text='food')

    def draw_graphic(self, widget, graphic, text=None):
        qp = QtGui.QPainter()
        height = widget.height()
        qp.begin(widget)

        if text:
            qp.drawText(QRect(0, 0, 100, 100), Qt.AlignLeft, text)

        igraph = enumerate(graphic)
        i, prev = next(igraph)
        for i, cur in igraph:
            qp.drawLine(i-1, height - prev, i, height - cur)
            prev = cur

        qp.end()


class Graphic:
    def __init__(self, freq=1, scale=1.0, maxlen=None):
        self.freq = freq
        self.curi = 0
        self.scale = scale
        self.deque = collections.deque(maxlen=maxlen)

    def update(self, value):
        if self.curi == 0:
            self.deque.append(value)
            self.curi = self.freq

        self.curi -= 1

    def __iter__(self):
        return iter(x*self.scale for x in self.deque)

    def __len__(self):
        return len(self.deque)
