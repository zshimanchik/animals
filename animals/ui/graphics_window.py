from collections import deque

import numpy as np
import pyqtgraph
from PyQt5 import QtWidgets

from engine.world import World

SYMBOL_PEN = (255, 255, 255, 100)
SYMBOL_BRUSH = (0, 0, 255, 100)


def history_to_points(history):
    x, y = [], []
    for tick, values in enumerate(history):
        for value in values:
            x.append(tick)
            y.append(value)
    return x, y

class GraphicsWindow(QtWidgets.QMainWindow):
    def __init__(self, world, parent=None):
        super().__init__(parent=parent)
        assert isinstance(world, World)
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

        self.animals_lifetimes_plot = pyqtgraph.PlotWidget()
        self.animals_lifetimes_plot.enableAutoRange('y')
        self.animals_lifetimes_plot.setXRange(0, self.parent().animal_lifetime_analyzer.analysis_interval)

        self.new_animals_energy_plot = pyqtgraph.PlotWidget()
        self.new_animals_energy_plot.enableAutoRange('y')
        self.new_animals_energy_plot.setXRange(0, self.parent().new_animal_energy_analyzer.analysis_interval)

        self.energy_for_birth_plot = pyqtgraph.PlotWidget()
        self.energy_for_birth_plot.setXRange(
            self.world.constants.ENERGY_FOR_BIRTH_MIN,
            self.world.constants.ENERGY_FOR_BIRTH_MAX
        )
        self.energy_for_birth_plot.enableAutoRange('y')

        self.useless_param_plot = pyqtgraph.PlotWidget()
        self.useless_param_plot.setXRange(
            self.world.constants.ENERGY_FOR_BIRTH_MIN,
            self.world.constants.ENERGY_FOR_BIRTH_MAX
        )
        self.useless_param_plot.enableAutoRange('y')

        self.centralwidget_layout.addWidget(self.food_plot)
        self.centralwidget_layout.addWidget(self.animals_plot)
        self.centralwidget_layout.addWidget(self.animals_lifetimes_plot)
        self.centralwidget_layout.addWidget(self.new_animals_energy_plot)
        self.centralwidget_layout.addWidget(self.energy_for_birth_plot)
        self.centralwidget_layout.addWidget(self.useless_param_plot)
        self.setCentralWidget(self.centralwidget)

    def showEvent(self, QShowEvent):
        pass

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, value):
        self._world = value

    def update(self):
        self.food_history.append(len(self.world.food))
        self.animals_history.append(len(self.world.animals))

    def redraw(self):
        self.food_curve.setData(self.food_history)
        self.animals_curve.setData(self.animals_history)

        x, y = history_to_points(self.parent().animal_lifetime_analyzer.animals_lifetimes_history)
        self.animals_lifetimes_plot.plot(
            x, y, pen=None, symbol='o', symbolSize=5, symbolPen=SYMBOL_PEN, symbolBrush=SYMBOL_BRUSH, clear=True
        )

        x, y = history_to_points(self.parent().new_animal_energy_analyzer.new_animal_energy_history)
        self.new_animals_energy_plot.plot(
            x, y, pen=None, symbol='o', symbolSize=5, symbolPen=SYMBOL_PEN, symbolBrush=SYMBOL_BRUSH, clear=True
        )

        vals = np.array([animal.energy_for_birth for animal in self.world.animals])
        y = pyqtgraph.pseudoScatter(vals, spacing=0.15)
        self.energy_for_birth_plot.plot(
            vals, y, pen=None, symbol='o', symbolSize=5, symbolPen=SYMBOL_PEN, symbolBrush=SYMBOL_BRUSH, clear=True
        )

        vals = np.array([animal.useless_param for animal in self.world.animals])
        y = pyqtgraph.pseudoScatter(vals, spacing=0.15)
        self.useless_param_plot.plot(
            vals, y, pen=None, symbol='o', symbolSize=5, symbolPen=SYMBOL_PEN, symbolBrush=SYMBOL_BRUSH, clear=True
        )
