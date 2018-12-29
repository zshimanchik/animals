# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphics_window.ui'
#
# Created: Thu May 25 13:19:23 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_graphics_window(object):
    def setupUi(self, graphics_window):
        graphics_window.setObjectName("graphics_window")
        graphics_window.resize(895, 439)
        self.centralwidget = QtWidgets.QWidget(graphics_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 879, 423))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_1 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_1.setObjectName("widget_1")
        self.verticalLayout_2.addWidget(self.widget_1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        graphics_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(graphics_window)
        QtCore.QMetaObject.connectSlotsByName(graphics_window)

    def retranslateUi(self, graphics_window):
        graphics_window.setWindowTitle(QtWidgets.QApplication.translate("graphics_window", "Graphics"))

