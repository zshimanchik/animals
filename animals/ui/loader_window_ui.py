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
        LoaderWindow.resize(542, 600)
        self.centralwidget = QtWidgets.QWidget(LoaderWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralwidget_layout.setObjectName("centralwidget_layout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.gridLayout_2.addWidget(self.listWidget, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.refresh_button = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_button.setObjectName("refresh_button")
        self.gridLayout_2.addWidget(self.refresh_button, 0, 2, 1, 1)
        self.listWidget2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget2.setObjectName("listWidget2")
        item = QtWidgets.QListWidgetItem()
        self.listWidget2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget2.addItem(item)
        self.gridLayout_2.addWidget(self.listWidget2, 1, 1, 1, 2)
        self.centralwidget_layout.addLayout(self.gridLayout_2)
        LoaderWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoaderWindow)
        QtCore.QMetaObject.connectSlotsByName(LoaderWindow)

    def retranslateUi(self, LoaderWindow):
        _translate = QtCore.QCoreApplication.translate
        LoaderWindow.setWindowTitle(_translate("LoaderWindow", "Loader Window"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("LoaderWindow", "world 1"))
        item = self.listWidget.item(1)
        item.setText(_translate("LoaderWindow", "world 2"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("LoaderWindow", "Print latest"))
        self.lineEdit.setPlaceholderText(_translate("LoaderWindow", "filter"))
        self.refresh_button.setText(_translate("LoaderWindow", "Refresh"))
        __sortingEnabled = self.listWidget2.isSortingEnabled()
        self.listWidget2.setSortingEnabled(False)
        item = self.listWidget2.item(0)
        item.setText(_translate("LoaderWindow", "10000"))
        item = self.listWidget2.item(1)
        item.setText(_translate("LoaderWindow", "20000"))
        item = self.listWidget2.item(2)
        item.setText(_translate("LoaderWindow", "30000"))
        self.listWidget2.setSortingEnabled(__sortingEnabled)
