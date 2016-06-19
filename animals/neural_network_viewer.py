from random import randint

from PySide import QtGui
from PySide.QtCore import QRect
from PySide.QtGui import QBrush, QPen, QColor


def brush(r, g, b, alpha=255):
    return QBrush(QColor(r, g, b, alpha))


def pen(r, g, b, alpha=255):
    return QPen(QColor(r, g, b, alpha))


def set_color(qp, color):
    color = max(0, min(255, color))
    qp.setBrush(brush(100, color, 255-color))
    qp.setPen(pen(100, color, 255-color))


class NeuralNetworkViewer(QtGui.QMainWindow):
    def __init__(self, network=None, parent=None):
        super().__init__(parent=parent)
        self.network = network

        self.central_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle("NeuralNetwork viewer")
        self.resize(400, 400)

    def paintEvent(self, event):
        if self.network:
            qp = QtGui.QPainter()
            qp.begin(self)

            cell_width = self.width()
            cell_height = self.height()/len(self.network)

            for i, layer in enumerate(self.network):
                self.draw_layer(qp, layer, 0, i * cell_height, cell_width, cell_height)

            qp.end()

    def draw_layer(self, qp, layer, x, y, width, height):
        qp.setBrush(brush(randint(0,255), randint(0,255), randint(0,255)))
        cell_height = height*0.7
        cell_width = width / len(layer)
        y += height * 0.15

        for i, out in enumerate(layer):
            rect = QRect(x+i*cell_width, y, cell_width, cell_height)
            set_color(qp, int((out + 1) * 255.0 / 2.0))
            qp.drawEllipse(rect)


if __name__ == "__main__":
    pass
