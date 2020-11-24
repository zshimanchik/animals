import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot as Slot

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
        self.pushButton.clicked.connect(self.push_button_click)

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

        filter = self.lineEdit.text()
        filtered_db = (wn for wn in self._db if filter in wn)
        for dirpath in filtered_db:
            item = QtWidgets.QListWidgetItem(self.listWidget)
            item.setText(dirpath)

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
    def push_button_click(self):
        self.print_latest(self.lineEdit.text())

    def print_latest(self, filter_text=''):
        table = []
        table.append(['World name', 'Latest tick'])
        for dirname, worlds in self._db.items():
            if filter_text in dirname:
                latest_tick = worlds[-1][:-len('.wrld')]
                try:
                    latest_tick = '{:_}'.format(int(latest_tick))
                except ValueError:
                    pass
                table.append([dirname, latest_tick])

        col0_len = max(len(row[0]) for row in table)
        col1_len = max(len(row[1]) for row in table)
        table.insert(1, [':' + '-' * (col0_len-1), ':' + '-' * (col1_len-1)])
        for col0, col1 in table:
            print(f'| {col0:{col0_len}} | {col1:{col1_len}} |')
