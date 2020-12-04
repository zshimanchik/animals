import os
import re

import pyqtgraph
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot as Slot
import tabulate

from engine import serializer
from engine.world_constants import WorldConstants
from ui.loader_window_ui import Ui_LoaderWindow


def sort_key(name):
    if name.endswith('.wrld'):
        name = name[:-len('.wrld')]
    try:
        return (int(name), name)
    except ValueError:
        return (0, name)


class LoaderWindow(Ui_LoaderWindow, QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self._db = {}
        self.init_db(self.parent().snapshot_directory_combobox.currentText())
        self.update_ui_with_new_db()
        self.listWidget.currentItemChanged.connect(self.list_widget_current_item_changed)
        self.listWidget.itemDoubleClicked.connect(self.list_widget_item_double_clicked)
        self.listWidget2.currentItemChanged.connect(self.list_widget2_current_item_changed)
        self.lineEdit.textChanged.connect(self.line_edit_text_changed)
        self.print_latest_button.clicked.connect(self.print_latest_button_click)
        self.refresh_button.clicked.connect(self.refresh_button_click)
        self.analyze_button.clicked.connect(self.analyze_button_click)
        self.analyze_all_button.clicked.connect(self.analyze_all_button_click)

    def init_db(self, snapshot_dir):
        self._db.clear()
        for dirpath, dirnames, filenames in os.walk(snapshot_dir):
            dirnames.sort()
            item = []
            dirpath = dirpath[len(snapshot_dir)+1:]
            self._db[dirpath] = item
            for filename in sorted((f for f in filenames if f.endswith('.wrld')), key=sort_key):
                item.append(filename)

    def update_ui_with_new_db(self):
        self.listWidget.clear()
        self.listWidget2.clear()

        for dirpath in self.filtered_db:
            item = QtWidgets.QListWidgetItem(self.listWidget)
            item.setText(dirpath)

    @property
    def filtered_db(self):
        filter_text = self.lineEdit.text()
        return {dirname: worlds for dirname, worlds in self._db.items() if re.search(filter_text, dirname)}

    @Slot(QtWidgets.QListWidgetItem, QtWidgets.QListWidgetItem)
    def list_widget_current_item_changed(self, cur: QtWidgets.QListWidgetItem, prev: QtWidgets.QListWidgetItem):
        self.listWidget2.clear()

        if cur is None:
            return

        dirpath = cur.text()
        for world_time in self._db[dirpath]:
            item = QtWidgets.QListWidgetItem()
            item.setText(world_time)
            self.listWidget2.addItem(item)

    @Slot(QtWidgets.QListWidgetItem)
    def list_widget_item_double_clicked(self, item: QtWidgets.QListWidgetItem):
        world_name = item.text()
        world_time = self._db[world_name][-1]
        filename = os.path.join(self.parent().snapshot_directory_combobox.currentText(), world_name, world_time)
        print('Loading filename: ', filename)
        self.parent().load_world(filename)

    @Slot(QtWidgets.QListWidgetItem, QtWidgets.QListWidgetItem)
    def list_widget2_current_item_changed(self, cur: QtWidgets.QListWidgetItem, prev: QtWidgets.QListWidgetItem):
        if cur is None:
            return

        world_name = self.listWidget.currentItem().text()
        world_time = cur.text()
        filename = os.path.join(self.parent().snapshot_directory_combobox.currentText(), world_name, world_time)
        print('Loading filename: ', filename)
        self.parent().load_world(filename)

    @Slot(str)
    def line_edit_text_changed(self, text):
        self.update_ui_with_new_db()

    @Slot()
    def print_latest_button_click(self):
        self.print_latest(self.lineEdit.text())

    @Slot()
    def refresh_button_click(self):
        self.init_db(self.parent().snapshot_directory_combobox.currentText())
        self.update_ui_with_new_db()

    @Slot()
    def analyze_button_click(self):
        if self.listWidget.currentItem():
            world_name = self.listWidget.currentItem().text()
            data = self.get_data_for_plot(
                self.parent().snapshot_directory_combobox.currentText(),
                world_name,
                self._db[world_name]
            )
            self.show_graphs([data])

    @Slot()
    def analyze_all_button_click(self):
        data = []
        for world_name, world_times in self.filtered_db.items():
            item = self.get_data_for_plot(
                self.parent().snapshot_directory_combobox.currentText(),
                world_name,
                self._db[world_name]
            )
            data.append(item)
        self.show_graphs(data)

    def print_latest(self, filter_text=''):
        table_header = ('World name', 'Latest tick', 'Generations', 'Constants diff')
        table = []
        for world_name, worlds in self.filtered_db.items():
            latest_tick = worlds[-1][:-len('.wrld')]
            try:
                latest_tick = '{:_}'.format(int(latest_tick))
            except ValueError:
                pass
            filename = os.path.join(self.parent().snapshot_directory_combobox.currentText(), world_name, worlds[-1])
            world = serializer.load(filename)
            constants_diff = self.get_constants_diff(world)
            table.append([world_name, latest_tick, world.max_generation, str(constants_diff or 'None')])

        print(tabulate.tabulate(table, headers=table_header, tablefmt='pipe'))

    def get_constants_diff(self, world):
        cur_constants = WorldConstants().to_dict(False)
        loaded_constants = world.constants.to_dict(False)
        return {k: loaded_constants[k] for k, v in cur_constants.items() if loaded_constants[k] != v}

    def get_data_for_plot(self, snapshot_dir, world_name, world_times):
        animal_amount_history = []
        for world_time in world_times:
            world = serializer.load(os.path.join(snapshot_dir, world_name, world_time))
            animal_amount_history.append(len(world.animals))

        try:
            x_axis = [int(world_time[:-len('.wrld')]) / 1000 for world_time in world_times]
        except ValueError:
            x_axis = None

        return world_name, x_axis, animal_amount_history

    def show_graphs(self, data: list):
        window = QtWidgets.QMainWindow(parent=self)
        window.setWindowTitle(f'Animal amount')
        scroll_area = QtWidgets.QScrollArea(window)
        scroll_area.setWidgetResizable(True)
        window.setCentralWidget(scroll_area)

        scroll_area_widget = QtWidgets.QWidget()
        grid_layout = QtWidgets.QGridLayout(scroll_area_widget)
        scroll_area.setWidget(scroll_area_widget)

        for world_name, x_axis, y_axis in data:
            label = QtWidgets.QLabel(world_name)

            grid_layout.addWidget(label)
            animals_plot = pyqtgraph.PlotWidget(scroll_area)
            animals_plot.plot(x=x_axis, y=y_axis)
            animals_plot.enableAutoRange()
            animals_plot.setMinimumSize(300, 100)
            grid_layout.addWidget(animals_plot)

        window.resize(600, 400)
        window.show()
