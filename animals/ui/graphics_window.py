import collections

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPen, QColor

from ui.graphics_window_ui import Ui_graphics_window


def get_color(color):
    r, g, b = max(0, -color), max(0, color), 0
    return QColor(r * 255, g * 255, b * 255)


class GraphicsWindow(Ui_graphics_window, QtWidgets.QMainWindow):
    def __init__(self, world, parent=None):
        super().__init__(parent=parent)
        self.world = world

        self.setupUi(self)
        self.widget_1.paintEvent = self.on_widget_1_paintEvent
        self.widget_1.resizeEvent = self.widget_1_resizeEvent
        self.widget_1.wheelEvent = self.on_widget_1_wheelEvent

    def widget_1_resizeEvent(self, event):
        # I know that this method evoke too often...
        self.population.scale = self.widget_1.height() / 100.0
        self.food.scale = self.widget_1.height() / 250.0

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, value):
        self._world = value
        self.population = Graphic(freq=10, scale=2, maxlen=None)
        self.food = Graphic(freq=10, scale=1, maxlen=None)

    def update(self):
        self.population.update(len(self.world.animals))
        self.food.update(len(self.world.food))

    def redraw(self):
        width = max(len(self.population), self.scrollArea.width()-10)
        self.scrollAreaWidgetContents.setFixedWidth(width)

        bar= self.scrollArea.horizontalScrollBar()
        if bar.maximum() - bar.value() < 100:
            bar.setValue(bar.maximum())

        self.widget_1.repaint()

    def on_widget_1_paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self.widget_1)
        width = painter.device().width()
        scroll_pos = self.scrollArea.horizontalScrollBar().value()

        painter.setPen(QPen(Qt.green))
        painter.drawText(QRect(scroll_pos, 0, 100, 20), Qt.AlignLeft, 'population')
        self.draw_graphic(painter, self.population)

        painter.setPen(QPen(Qt.blue))
        painter.drawText(QRect(scroll_pos, 20, width, 20), Qt.AlignLeft, 'food')
        self.draw_graphic(painter, self.food)

        painter.end()

    def draw_graphic(self, painter, graphic):
        height = painter.device().height()
        igraph = enumerate(graphic)
        i, prev = next(igraph)
        for i, cur in igraph:
            painter.drawLine(i - 1, height - prev, i, height - cur)
            prev = cur

    def on_widget_1_wheelEvent(self, event):
        d = - event.delta() / 120
        self.food.freq += d
        self.population.freq += d


class Graphic:
    def __init__(self, freq=1, scale=1.0, maxlen=None):
        self._freq = freq
        self.curi = 0
        self.scale = scale
        self.deque = collections.deque(maxlen=maxlen)

    def update(self, value):
        self.deque.append(value)

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, value):
        self._freq = max(1, int(value))

    def __iter__(self):
        return self._iterator()

    def _iterator(self):
        freq = self.freq
        idata = iter(self.deque)
        while True:
            yield next(idata) * self.scale

            # skipping data
            for _ in range(freq - 1):
                next(idata)

    def __len__(self):
        return len(self.deque) // self.freq
