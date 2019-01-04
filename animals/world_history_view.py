import os
import sys

import numpy as np
import pyqtgraph
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from pyqtgraph.Qt import QtCore

from engine import serializer


def main():
    DIR = 'snapshots/rem_2019-01-04T01:14:04--62948fd/snapshots/2019-01-04T01:14:04--62948fd--world_n03'
    win = GraphicsWindow()
    win.resize(600,16000)
    win.setWindowTitle('world history')

    files = [x for x in os.listdir(DIR) if x.endswith('.wrld')]
    print(len(files))
    sorted_files = sorted(files, key=lambda x: int(x.partition('.')[0]))
    for i, filename in enumerate(sorted_files):
        full_filename = os.path.join(DIR, filename)
        print(full_filename)
        world = serializer.load(full_filename)
        win.plot_world(world)
    return win


class GraphicsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setWindowTitle("Plots")
        self.central_widget_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.central_widget_layout.setObjectName("centralwidget_layout")

        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scrollArea")
        self.scroll_area_widget_contents = QtWidgets.QWidget()
        self.scroll_area_widget_contents.setGeometry(QtCore.QRect(0, 0, 929, 339))
        self.scroll_area_widget_contents.setObjectName("scrollAreaWidgetContents")
        self.grid_layout = QtWidgets.QGridLayout(self.scroll_area_widget_contents)
        self.grid_layout.setObjectName("horizontalLayout")

        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.central_widget_layout.addWidget(self.scroll_area)

        self.setCentralWidget(self.centralwidget)
        self.row = 0

    def plot_world(self, world):
        self.plot_energy_for_birth(world, 1)
        # self.plot_new_animal_energy(world, 2)
        self.row += 1

    def plot_energy_for_birth(self, world, column):
        energy_for_birth_plot = pyqtgraph.PlotWidget()
        energy_for_birth_plot.setXRange(
            world.constants.ENERGY_FOR_BIRTH_MIN,
            world.constants.ENERGY_FOR_BIRTH_MAX
        )
        energy_for_birth_plot.enableAutoRange('y')

        self.grid_layout.addWidget(energy_for_birth_plot, self.row, column)

        vals = np.array([animal.energy_for_birth for animal in world.animals])
        y = pyqtgraph.pseudoScatter(vals, spacing=0.15)
        energy_for_birth_plot.plot(
            vals, y, pen=None, symbol='o', symbolSize=5, symbolPen=(255, 255, 255, 200), symbolBrush=(0, 0, 255, 150),
            clear=True
        )

    def plot_new_animal_energy(self, world, column):
        plot_widget = pyqtgraph.PlotWidget()
        plot_widget.enableAutoRange('y')
        self.grid_layout.addWidget(plot_widget, self.row, column)
        plot_widget.plot([x[1] for x in world.new_animal_avg_energy], clear=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mySW = main()
    mySW.show()
    sys.exit(app.exec_())
