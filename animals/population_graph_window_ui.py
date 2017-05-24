# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'population_graph_window.ui'
#
# Created: Mon May 22 16:41:26 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PopulationGraphWidget(object):
    def setupUi(self, PopulationGraphWidget):
        PopulationGraphWidget.setObjectName("PopulationGraphWidget")
        PopulationGraphWidget.resize(1061, 355)
        self.centralwidget = QtGui.QWidget(PopulationGraphWidget)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 9, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 6, 1, 1, 1)
        self.draw_lines_checkbox = QtGui.QCheckBox(self.groupBox)
        self.draw_lines_checkbox.setChecked(True)
        self.draw_lines_checkbox.setObjectName("draw_lines_checkbox")
        self.gridLayout.addWidget(self.draw_lines_checkbox, 5, 1, 1, 1)
        self.all_radio_button = QtGui.QRadioButton(self.groupBox)
        self.all_radio_button.setObjectName("all_radio_button")
        self.gridLayout.addWidget(self.all_radio_button, 1, 1, 1, 1)
        self.ancestors_radio_button = QtGui.QRadioButton(self.groupBox)
        self.ancestors_radio_button.setChecked(True)
        self.ancestors_radio_button.setObjectName("ancestors_radio_button")
        self.gridLayout.addWidget(self.ancestors_radio_button, 2, 1, 1, 1)
        self.successors_radio_button = QtGui.QRadioButton(self.groupBox)
        self.successors_radio_button.setObjectName("successors_radio_button")
        self.gridLayout.addWidget(self.successors_radio_button, 4, 1, 1, 1)
        self.depth_spinbox = QtGui.QSpinBox(self.groupBox)
        self.depth_spinbox.setObjectName("depth_spinbox")
        self.gridLayout.addWidget(self.depth_spinbox, 7, 1, 1, 1)
        self.info_label = QtGui.QLabel(self.groupBox)
        self.info_label.setObjectName("info_label")
        self.gridLayout.addWidget(self.info_label, 8, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 929, 339))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout = QtGui.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.draw_widget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.draw_widget.setObjectName("draw_widget")
        self.horizontalLayout.addWidget(self.draw_widget)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        PopulationGraphWidget.setCentralWidget(self.centralwidget)

        self.retranslateUi(PopulationGraphWidget)
        QtCore.QMetaObject.connectSlotsByName(PopulationGraphWidget)

    def retranslateUi(self, PopulationGraphWidget):
        PopulationGraphWidget.setWindowTitle(QtGui.QApplication.translate("PopulationGraphWidget", "Population Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PopulationGraphWidget", "Depth:", None, QtGui.QApplication.UnicodeUTF8))
        self.draw_lines_checkbox.setText(QtGui.QApplication.translate("PopulationGraphWidget", "draw lines", None, QtGui.QApplication.UnicodeUTF8))
        self.all_radio_button.setText(QtGui.QApplication.translate("PopulationGraphWidget", "a&ll", None, QtGui.QApplication.UnicodeUTF8))
        self.ancestors_radio_button.setText(QtGui.QApplication.translate("PopulationGraphWidget", "a&ncestors", None, QtGui.QApplication.UnicodeUTF8))
        self.successors_radio_button.setText(QtGui.QApplication.translate("PopulationGraphWidget", "s&uccessors", None, QtGui.QApplication.UnicodeUTF8))
        self.info_label.setText(QtGui.QApplication.translate("PopulationGraphWidget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

