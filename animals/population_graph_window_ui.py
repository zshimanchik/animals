# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'population_graph_window.ui'
#
# Created: Mon May 22 16:41:26 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtWidgets

class Ui_PopulationGraphWidget(object):
    def setupUi(self, PopulationGraphWidget):
        PopulationGraphWidget.setObjectName("PopulationGraphWidget")
        PopulationGraphWidget.resize(1061, 355)
        self.centralwidget = QtWidgets.QWidget(PopulationGraphWidget)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 9, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 6, 1, 1, 1)
        self.draw_lines_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.draw_lines_checkbox.setChecked(True)
        self.draw_lines_checkbox.setObjectName("draw_lines_checkbox")
        self.gridLayout.addWidget(self.draw_lines_checkbox, 5, 1, 1, 1)
        self.all_radio_button = QtWidgets.QRadioButton(self.groupBox)
        self.all_radio_button.setObjectName("all_radio_button")
        self.gridLayout.addWidget(self.all_radio_button, 1, 1, 1, 1)
        self.ancestors_radio_button = QtWidgets.QRadioButton(self.groupBox)
        self.ancestors_radio_button.setChecked(True)
        self.ancestors_radio_button.setObjectName("ancestors_radio_button")
        self.gridLayout.addWidget(self.ancestors_radio_button, 2, 1, 1, 1)
        self.successors_radio_button = QtWidgets.QRadioButton(self.groupBox)
        self.successors_radio_button.setObjectName("successors_radio_button")
        self.gridLayout.addWidget(self.successors_radio_button, 4, 1, 1, 1)
        self.depth_spinbox = QtWidgets.QSpinBox(self.groupBox)
        self.depth_spinbox.setObjectName("depth_spinbox")
        self.gridLayout.addWidget(self.depth_spinbox, 7, 1, 1, 1)
        self.info_label = QtWidgets.QLabel(self.groupBox)
        self.info_label.setObjectName("info_label")
        self.gridLayout.addWidget(self.info_label, 8, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 929, 339))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.draw_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.draw_widget.setObjectName("draw_widget")
        self.horizontalLayout.addWidget(self.draw_widget)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        PopulationGraphWidget.setCentralWidget(self.centralwidget)

        self.retranslateUi(PopulationGraphWidget)
        QtCore.QMetaObject.connectSlotsByName(PopulationGraphWidget)

    def retranslateUi(self, PopulationGraphWidget):
        PopulationGraphWidget.setWindowTitle(QtWidgets.QApplication.translate("PopulationGraphWidget", "Population Graph"))
        self.label.setText(QtWidgets.QApplication.translate("PopulationGraphWidget", "Depth:"))
        self.draw_lines_checkbox.setText(QtWidgets.QApplication.translate("PopulationGraphWidget", "draw lines"))
        self.all_radio_button.setText(QtWidgets.QApplication.translate("PopulationGraphWidget", "a&ll"))
        self.ancestors_radio_button.setText(QtWidgets.QApplication.translate("PopulationGraphWidget", "a&ncestors"))
        self.successors_radio_button.setText(QtWidgets.QApplication.translate("PopulationGraphWidget", "s&uccessors"))
        self.info_label.setText(QtWidgets.QApplication.translate("PopulationGraphWidget", "TextLabel"))

