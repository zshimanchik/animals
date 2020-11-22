from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import Qt
import os

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
        self.init_list(self.parent().snapshot_directory_combobox.currentText())
        self.treeWidget.itemDoubleClicked.connect(self.item_clicked)

    def init_list(self, snapshot_dir):
        self.treeWidget.clear()
        for dirpath, dirnames, filenames in os.walk(snapshot_dir):
            dirnames.sort()
            item = QtWidgets.QTreeWidgetItem(self.treeWidget)
            dirpath = dirpath[len(snapshot_dir)+1:]
            item.setText(0, dirpath)
            for filename in sorted((f for f in filenames if f.endswith('.wrld')), key=sort_key):
                subitem = QtWidgets.QTreeWidgetItem(item)
                subitem.setText(0, filename)

    @Slot(QtWidgets.QTreeWidgetItem, int)
    def item_clicked(self, item: QtWidgets.QTreeWidgetItem, column):
        if not item.text(0).endswith('.wrld'):
            return

        if isinstance(item.parent(), QtWidgets.QTreeWidgetItem):
            path = os.path.join(item.parent().text(0), item.text(0))
        else:
            path = './' + item.text(0)
        filename = os.path.join(self.parent().snapshot_directory_combobox.currentText(), path)
        self.parent().load_world(filename)


