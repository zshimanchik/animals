# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loader_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoaderWindow(object):
    def setupUi(self, LoaderWindow):
        LoaderWindow.setObjectName("LoaderWindow")
        LoaderWindow.resize(429, 600)
        self.centralwidget = QtWidgets.QWidget(LoaderWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralwidget_layout.setObjectName("centralwidget_layout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.gridLayout_2.addWidget(self.treeWidget, 0, 0, 1, 1)
        self.centralwidget_layout.addLayout(self.gridLayout_2)
        LoaderWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoaderWindow)
        QtCore.QMetaObject.connectSlotsByName(LoaderWindow)

    def retranslateUi(self, LoaderWindow):
        _translate = QtCore.QCoreApplication.translate
        LoaderWindow.setWindowTitle(_translate("LoaderWindow", "Loader Window"))
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.headerItem().setText(0, _translate("LoaderWindow", "filename path"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("LoaderWindow", "World 2"))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("LoaderWindow", "200000"))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("LoaderWindow", "100000"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
