import random
from collections import deque

import pyqtgraph
from PyQt5 import QtWidgets


class GraphicsWindow(QtWidgets.QMainWindow):
    def __init__(self, world, parent=None):
        super().__init__(parent=parent)
        self._world = world

        self.centralwidget = QtWidgets.QWidget(self)
        self.setWindowTitle("Plots")
        self.centralwidget_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centralwidget_layout.setObjectName("centralwidget_layout")

        self.food_history = deque(maxlen=5000)
        self.food_plot = pyqtgraph.PlotWidget()
        self.food_plot.enableAutoRange()
        self.food_curve = self.food_plot.plot(self.food_history, pen=(0, 255, 0), name="Food")
        self.food_curve.setPos(self.world.time, 0)

        self.animals_history = deque(maxlen=5000)
        self.animals_plot = pyqtgraph.PlotWidget()
        self.animals_plot.enableAutoRange()
        self.animals_curve = self.animals_plot.plot(self.animals_history, pen=(255, 0, 0), name="Animals")
        self.animals_curve.setPos(self.world.time, 0)

        self.guiplot = pyqtgraph.PlotWidget()
        self.guiplot.enableAutoRange()

        self.energy_for_birth_plot = pyqtgraph.PlotWidget()
        self.energy_for_birth_plot.enableAutoRange()

        self.centralwidget_layout.addWidget(self.food_plot)
        self.centralwidget_layout.addWidget(self.animals_plot)
        self.centralwidget_layout.addWidget(self.guiplot)
        self.centralwidget_layout.addWidget(self.energy_for_birth_plot)
        self.setCentralWidget(self.centralwidget)

    def showEvent(self, QShowEvent):
        x = [animal.energy_for_birth for animal in self.world.animals]
        y = [random.normalvariate(0, 0.002) for _ in range(len(self.world.animals))]
        self.energy_for_birth_plot.plot(
            x, y, pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 170), clear=True
        )

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, value):
        self._world = value

    def update(self):
        self.food_history.append(len(self.world.food))
        self.animals_history.append(len(self.world.animals))

        self.food_curve.setData(self.food_history)
        self.animals_curve.setData(self.animals_history)

        self.guiplot.plot([x[1] for x in self.world.animal_deaths], clear=True)

    def redraw(self):
        pass
