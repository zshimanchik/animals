from random import randint
import colorsys

from PySide import QtGui
from PySide.QtCore import QRect, Qt
from PySide.QtGui import QBrush, QColor


def set_color(qp, color):
    qp.setPen(Qt.NoPen)
    color = max(0, min(255, color))
    r, g, b = colorsys.hsv_to_rgb(0.333333 * color, 1.0, 1.0)
    qp.setBrush(QBrush(QColor(r*255, g*255, b*255)))


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
        cell_height = height*0.7
        cell_width = width / len(layer)
        y += height * 0.15

        for i, out in enumerate(layer):
            rect = QRect(x+i*cell_width, y, cell_width, cell_height)
            set_color(qp, (out + 1) / 2.0)
            qp.drawEllipse(rect)


if __name__ == "__main__":
    pass
