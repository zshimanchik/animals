from itertools import cycle

from PySide2 import QtWidgets


class ConstantsWindow(QtWidgets.QMainWindow):
    EDITABLE_PROPERTIES = ['WORLD_HEIGHT', 'WORLD_WIDTH', 'FOOD_TIMER', 'ANIMAL_MAX_ENERGY', 'ANIMAL_SIZE',
                           'APPEAR_FOOD_COUNT', 'APPEAR_FOOD_SIZE_MAX', 'APPEAR_FOOD_SIZE_MIN', 'EATING_DISTANCE',
                           'EATING_VALUE', 'ENERGY_FOR_BIRTH', 'ENERGY_FOR_EXIST',
                           'ENERGY_FULLNESS_TO_INCREASE_READINESS_TO_SEX', 'FOOD_FROM_MAMMOTH_COUNT',
                           'FOOD_SIZE_TO_ENERGY_RATIO', 'FOOD_SMELL_SIZE_RATIO', 'INITIAL_ANIMAL_COUNT',
                           'INITIAL_FOOD_COUNT', 'MAMMOTH_BEAT_VALUE', 'MAMMOTH_COUNT',
                           'MAMMOTH_MIN_DISTANCE_TO_OTHERS', 'MAMMOTH_REGENERATION_VALUE', 'MAMMOTH_SMELL_SIZE_RATIO',
                           'MAX_AMOUNT_OF_CHILDREN', 'MAX_ANIMAL_SMELL_SIZE', 'MIN_AMOUNT_OF_CHILDREN',
                           'MOVE_DISTANCE_TO_CONSUMED_ENERGY_RATIO', 'MUTATE_CHANCE', 'READINESS_TO_SEX_INCREMENT',
                           'READINESS_TO_SEX_THRESHOLD', 'SEX_DISTANCE']

    READONLY_PROPERTIES = ['INPUT_LAYER_SIZE', 'NEURAL_NETWORK_SHAPE', 'DNA_BASE', 'DNA_BRAIN_VALUE_LEN',
                           'DNA_MAX_VALUE', 'DNA_HALF_MAX_VALUE', 'DNA_FOR_BRAIN_LEN', 'DNA_LEN', 'MIDDLE_LAYERS_SIZES',
                           'OUTPUT_LAYER_SIZE', 'ANIMAL_SENSOR_COUNT', 'ANIMAL_SENSOR_DIMENSION']

    COLUMN_AMOUNT = 3

    def __init__(self, constants, parent=None):
        super().__init__(parent)
        self.constants = constants

        self.property_widget = {}

        self.centralwidget = QtWidgets.QWidget(self)
        self.setWindowTitle("Constants")
        self.centralwidget_layout = QtWidgets.QGridLayout(self.centralwidget)
        self.centralwidget_layout.setObjectName("centralwidget_layout")

        row = 0
        column_cycle = cycle(range(self.COLUMN_AMOUNT))
        for column, prop in zip(column_cycle, self.EDITABLE_PROPERTIES):
            if column == 0:
                row += 1
            label = QtWidgets.QLabel()
            label.setText(prop)
            text_edit = QtWidgets.QLineEdit()
            text_edit.setText(str(self.constants.__getattribute__(prop)))
            self.centralwidget_layout.addWidget(label, row, column * 2 + 1, 1, 1)
            self.centralwidget_layout.addWidget(text_edit, row, column * 2 + 2, 1, 1)
            self.property_widget[prop] = text_edit

        column_cycle = cycle(range(self.COLUMN_AMOUNT))
        for column, prop in zip(column_cycle, self.READONLY_PROPERTIES):
            if column == 0:
                row += 1
            label = QtWidgets.QLabel()
            label.setText(prop)
            text_edit = QtWidgets.QLineEdit()
            text_edit.setReadOnly(True)
            text_edit.setText(str(self.constants.__getattribute__(prop)))
            self.centralwidget_layout.addWidget(label, row, column * 2 + 1, 1, 1)
            self.centralwidget_layout.addWidget(text_edit, row, column * 2 + 2, 1, 1)

        reset_button = QtWidgets.QPushButton()
        reset_button.setText("reset")
        reset_button.clicked.connect(self.reset_values)
        self.centralwidget_layout.addWidget(reset_button, row + 1, self.COLUMN_AMOUNT * 2, 1, 1)

        apply_button = QtWidgets.QPushButton()
        apply_button.setText("apply")
        apply_button.clicked.connect(self.apply_values)
        self.centralwidget_layout.addWidget(apply_button, row + 1, self.COLUMN_AMOUNT * 2 - 1, 1, 1)

        self.setCentralWidget(self.centralwidget)

    def reset_values(self):
        for prop, widget in self.property_widget.items():
            widget.setText(str(self.constants.__getattribute__(prop)))

    def apply_values(self):
        for prop, widget in self.property_widget.items():
            tp = type(self.constants.__getattribute__(prop))
            value = tp(widget.text())
            self.constants.__setattr__(prop, value)

        self.reset_values()
