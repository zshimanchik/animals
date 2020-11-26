# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1294, 344)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralwidget_layout.setObjectName("centralwidget_layout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 902, 269))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.draw_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.draw_widget.setMinimumSize(QtCore.QSize(900, 200))
        self.draw_widget.setMaximumSize(QtCore.QSize(900, 200))
        self.draw_widget.setObjectName("draw_widget")
        self.horizontalLayout.addWidget(self.draw_widget)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.centralwidget_layout.addWidget(self.scrollArea)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(350, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(350, 16777215))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.info_label = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(12)
        self.info_label.setFont(font)
        self.info_label.setText("Performance   0.00312231\n"
"World time    1231231\n"
"Food timer    55\n"
"Animal count  32\n"
"Food count    32\n"
"Mammoth count 5\n"
"")
        self.info_label.setObjectName("info_label")
        self.gridLayout_3.addWidget(self.info_label, 4, 0, 7, 2)
        self.draw_each_times_slider = QtWidgets.QSlider(self.tab)
        self.draw_each_times_slider.setMinimum(1)
        self.draw_each_times_slider.setMaximum(200)
        self.draw_each_times_slider.setProperty("value", 1)
        self.draw_each_times_slider.setOrientation(QtCore.Qt.Horizontal)
        self.draw_each_times_slider.setObjectName("draw_each_times_slider")
        self.gridLayout_3.addWidget(self.draw_each_times_slider, 3, 2, 1, 1)
        self.smells_checkbox = QtWidgets.QCheckBox(self.tab)
        self.smells_checkbox.setObjectName("smells_checkbox")
        self.gridLayout_3.addWidget(self.smells_checkbox, 5, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.select_radiobutton = QtWidgets.QRadioButton(self.tab)
        self.select_radiobutton.setChecked(True)
        self.select_radiobutton.setObjectName("select_radiobutton")
        self.horizontalLayout_2.addWidget(self.select_radiobutton)
        self.move_radiobutton = QtWidgets.QRadioButton(self.tab)
        self.move_radiobutton.setObjectName("move_radiobutton")
        self.horizontalLayout_2.addWidget(self.move_radiobutton)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 8, 2, 1, 1)
        self.draw_each_times_label = QtWidgets.QLabel(self.tab)
        self.draw_each_times_label.setObjectName("draw_each_times_label")
        self.gridLayout_3.addWidget(self.draw_each_times_label, 3, 0, 1, 1)
        self.eat_distance_checkbox = QtWidgets.QCheckBox(self.tab)
        self.eat_distance_checkbox.setObjectName("eat_distance_checkbox")
        self.gridLayout_3.addWidget(self.eat_distance_checkbox, 4, 2, 1, 1)
        self.draw_each_times_lcd = QtWidgets.QLCDNumber(self.tab)
        self.draw_each_times_lcd.setProperty("intValue", 1)
        self.draw_each_times_lcd.setObjectName("draw_each_times_lcd")
        self.gridLayout_3.addWidget(self.draw_each_times_lcd, 3, 1, 1, 1)
        self.animal_direction_checkbox = QtWidgets.QCheckBox(self.tab)
        self.animal_direction_checkbox.setObjectName("animal_direction_checkbox")
        self.gridLayout_3.addWidget(self.animal_direction_checkbox, 6, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 13, 0, 1, 3)
        self.timer_button = QtWidgets.QPushButton(self.tab)
        self.timer_button.setMinimumSize(QtCore.QSize(0, 20))
        self.timer_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.timer_button.setObjectName("timer_button")
        self.gridLayout_3.addWidget(self.timer_button, 2, 0, 1, 3)
        self.sensors_checkbox = QtWidgets.QCheckBox(self.tab)
        self.sensors_checkbox.setObjectName("sensors_checkbox")
        self.gridLayout_3.addWidget(self.sensors_checkbox, 7, 2, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.world_name_lbl = QtWidgets.QLabel(self.tab_2)
        self.world_name_lbl.setObjectName("world_name_lbl")
        self.gridLayout_4.addWidget(self.world_name_lbl, 0, 0, 1, 1)
        self.snapshot_directory_combobox = QtWidgets.QComboBox(self.tab_2)
        self.snapshot_directory_combobox.setEditable(True)
        self.snapshot_directory_combobox.setObjectName("snapshot_directory_combobox")
        self.gridLayout_4.addWidget(self.snapshot_directory_combobox, 3, 0, 1, 2)
        self.make_snapshots_spinbox = QtWidgets.QSpinBox(self.tab_2)
        self.make_snapshots_spinbox.setMinimum(1)
        self.make_snapshots_spinbox.setMaximum(10000000)
        self.make_snapshots_spinbox.setSingleStep(1000)
        self.make_snapshots_spinbox.setProperty("value", 100000)
        self.make_snapshots_spinbox.setObjectName("make_snapshots_spinbox")
        self.gridLayout_4.addWidget(self.make_snapshots_spinbox, 1, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 4, 0, 1, 3)
        self.snapshot_directory_label = QtWidgets.QLabel(self.tab_2)
        self.snapshot_directory_label.setObjectName("snapshot_directory_label")
        self.gridLayout_4.addWidget(self.snapshot_directory_label, 2, 0, 1, 2)
        self.browse_snapshot_directory_button = QtWidgets.QPushButton(self.tab_2)
        self.browse_snapshot_directory_button.setObjectName("browse_snapshot_directory_button")
        self.gridLayout_4.addWidget(self.browse_snapshot_directory_button, 3, 2, 1, 1)
        self.make_snapshots_checkbox = QtWidgets.QCheckBox(self.tab_2)
        self.make_snapshots_checkbox.setObjectName("make_snapshots_checkbox")
        self.gridLayout_4.addWidget(self.make_snapshots_checkbox, 1, 0, 1, 2)
        self.world_name_lineedit = QtWidgets.QLineEdit(self.tab_2)
        self.world_name_lineedit.setObjectName("world_name_lineedit")
        self.gridLayout_4.addWidget(self.world_name_lineedit, 0, 1, 1, 2)
        self.tabWidget.addTab(self.tab_2, "")
        self.centralwidget_layout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1294, 22))
        self.menubar.setObjectName("menubar")
        self.menuRestart_world = QtWidgets.QMenu(self.menubar)
        self.menuRestart_world.setObjectName("menuRestart_world")
        self.menuWorld = QtWidgets.QMenu(self.menubar)
        self.menuWorld.setObjectName("menuWorld")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionRestart = QtWidgets.QAction(MainWindow)
        self.actionRestart.setObjectName("actionRestart")
        self.constants_action = QtWidgets.QAction(MainWindow)
        self.constants_action.setObjectName("constants_action")
        self.network_viewer_action = QtWidgets.QAction(MainWindow)
        self.network_viewer_action.setObjectName("network_viewer_action")
        self.save_action = QtWidgets.QAction(MainWindow)
        self.save_action.setObjectName("save_action")
        self.load_action = QtWidgets.QAction(MainWindow)
        self.load_action.setObjectName("load_action")
        self.action_population_graph = QtWidgets.QAction(MainWindow)
        self.action_population_graph.setObjectName("action_population_graph")
        self.graphics_action = QtWidgets.QAction(MainWindow)
        self.graphics_action.setObjectName("graphics_action")
        self.loader_action = QtWidgets.QAction(MainWindow)
        self.loader_action.setObjectName("loader_action")
        self.menuRestart_world.addAction(self.constants_action)
        self.menuRestart_world.addAction(self.network_viewer_action)
        self.menuRestart_world.addAction(self.action_population_graph)
        self.menuRestart_world.addAction(self.graphics_action)
        self.menuRestart_world.addAction(self.loader_action)
        self.menuWorld.addAction(self.save_action)
        self.menuWorld.addAction(self.load_action)
        self.menubar.addAction(self.menuWorld.menuAction())
        self.menubar.addAction(self.menuRestart_world.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.draw_each_times_slider.valueChanged['int'].connect(self.draw_each_times_lcd.display)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.smells_checkbox.setText(_translate("MainWindow", "Smells"))
        self.select_radiobutton.setText(_translate("MainWindow", "Select"))
        self.move_radiobutton.setText(_translate("MainWindow", "Move"))
        self.draw_each_times_label.setText(_translate("MainWindow", "Draw each"))
        self.eat_distance_checkbox.setText(_translate("MainWindow", "Eat distance"))
        self.animal_direction_checkbox.setText(_translate("MainWindow", "Animal direction"))
        self.timer_button.setText(_translate("MainWindow", "Run/Pause"))
        self.sensors_checkbox.setText(_translate("MainWindow", "Sensors"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Main"))
        self.world_name_lbl.setText(_translate("MainWindow", "World name"))
        self.snapshot_directory_label.setText(_translate("MainWindow", "Snapshots directory:"))
        self.browse_snapshot_directory_button.setText(_translate("MainWindow", "browse"))
        self.make_snapshots_checkbox.setText(_translate("MainWindow", "Make snapshot each"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Autosave"))
        self.menuRestart_world.setTitle(_translate("MainWindow", "wi&ndows"))
        self.menuWorld.setTitle(_translate("MainWindow", "wor&ld"))
        self.actionRestart.setText(_translate("MainWindow", "restart"))
        self.constants_action.setText(_translate("MainWindow", "&constants"))
        self.network_viewer_action.setText(_translate("MainWindow", "&network viewer"))
        self.save_action.setText(_translate("MainWindow", "&save"))
        self.load_action.setText(_translate("MainWindow", "&load"))
        self.action_population_graph.setText(_translate("MainWindow", "&population graph"))
        self.graphics_action.setText(_translate("MainWindow", "graphics"))
        self.loader_action.setText(_translate("MainWindow", "loader"))
