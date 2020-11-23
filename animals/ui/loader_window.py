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
        self.listWidget.currentItemChanged.connect(self.tw_current_item_changed)
        self.listWidget2.currentItemChanged.connect(self.list_widget2_current_item_changed)
        self.lineEdit.textChanged.connect(self.line_edit_text_changed)

        # self.print_latest('201122')

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
    def tw_current_item_changed(self, cur: QtWidgets.QListWidgetItem, prev: QtWidgets.QListWidgetItem):
        self.listWidget2.clear()

        if cur is None:
            return

        dirpath = cur.text()
        for world_time in self._db[dirpath]:
            item = QtWidgets.QListWidgetItem()
            item.setText(world_time)
            self.listWidget2.addItem(item)

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

    def print_latest(self, filter_text=''):
        for dirname, worlds in self._db.items():
            if filter_text in dirname:
                print(dirname, '-', worlds[-1][:-len('.wrld')])

