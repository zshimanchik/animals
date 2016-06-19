import sys
import time
import math
from PySide.QtCore import QTimer, SIGNAL, Slot, QRect, Qt, QPointF
from PySide.QtGui import QMainWindow, QPainter, QApplication, QBrush, QPen, QColor
from PySide.QtOpenGL import QGLWidget

from main_window_ui import Ui_MainWindow
from constants_window import ConstantsWindow
from neural_network_viewer import NeuralNetworkViewer
import world
from world_constants import WorldConstants


class MainWindow(QMainWindow, Ui_MainWindow):
    _PERFORMANCE_CALC_INTERVAL = 20
    TIMER_INTERVAL = 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self._animal_brush = QBrush(QColor(74, 172, 225))
        self._food_brush = QBrush(QColor(100, 100, 100))
        self._food_beated_brush = QBrush(QColor(180, 140, 100))
        self._mammoth_brush = QBrush(QColor(50, 50, 200))
        self._animal_pen = Qt.NoPen
        self._selected_animal_pen = QPen(QColor(255, 180, 0), 2)
        self.selected_animal = None
        self.constants_window = None
        self.neural_network_viewer_window = None

        self.setupUi(self)
        self.centralwidget_layout.removeWidget(self.draw_widget)
        self.draw_widget = QGLWidget()
        self.centralwidget_layout.insertWidget(0, self.draw_widget)

        self.world_constants = WorldConstants()
        self.draw_widget.setFixedWidth(self.world_constants.WORLD_WIDTH)
        self.draw_widget.setFixedHeight(self.world_constants.WORLD_HEIGHT)

        self.world = world.World(constants=self.world_constants)
        self.draw_widget.paintEvent = self.on_draw_widget_paintEvent
        self.draw_widget.mousePressEvent = self.on_draw_widget_mousePressEvent

        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.on_timer_timeout)
        self.timer.start(self.TIMER_INTERVAL)

        self._prev_time = time.clock()

    @Slot()
    def on_timer_button_clicked(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(self.TIMER_INTERVAL)

    @Slot()
    def on_constants_action_triggered(self):
        if not self.constants_window:
            self.constants_window = ConstantsWindow(self.world_constants, parent=self)
        if self.constants_window.isVisible():
            self.constants_window.hide()
        else:
            self.constants_window.show()

    @Slot()
    def on_network_viewer_action_triggered(self):
        if not self.neural_network_viewer_window:
            self.neural_network_viewer_window = NeuralNetworkViewer(parent=self)
            if self.selected_animal:
                self.neural_network_viewer_window.network = self.selected_animal.brain
        if self.neural_network_viewer_window.isVisible():
            self.neural_network_viewer_window.hide()
        else:
            self.neural_network_viewer_window.show()

    @Slot()
    def on_timer_timeout(self):
        if self.world.time % self._PERFORMANCE_CALC_INTERVAL == 0:
            self.performance = (time.clock() - self._prev_time) / self._PERFORMANCE_CALC_INTERVAL
            self._prev_time = time.clock()
            self.performance_label.setText("{:.6f}".format(self.performance))

        if self.world.time == 200:
            print(self.performance)

        self.world.update()
        self._update_text_info()
        if self.world.time % self.draw_each_times_slider.value() == 0:
            self.draw_widget.repaint()
            if self.neural_network_viewer_window and self.neural_network_viewer_window.isVisible():
                self.neural_network_viewer_window.repaint()

    def _update_text_info(self):
        self.world_time_label.setText(str(self.world.time))
        self.food_timer_label.setText(str(self.world_constants.FOOD_TIMER))
        self.animal_count_label.setText(str(len(self.world.animals)))
        self.food_count_label.setText(str(len(self.world.food)))
        self.mammoth_count_label.setText(str(len(self.world.mammoths)))

    def on_draw_widget_paintEvent(self, event):
        painter = QPainter()
        painter.begin(self.draw_widget)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawText(QRect(0, 0, 100, 100), Qt.AlignCenter, "Qt")
        if self.smells_checkbox.isChecked():
            self._draw_smells(painter)

        for food in self.world.food:
            self._draw_food(painter, food)
        for mammoth in self.world.mammoths:
            self._draw_mammoth(painter, mammoth)
        for animal in self.world.animals:
            self._draw_animal(painter, animal)

        painter.end()

    def on_draw_widget_mousePressEvent(self, event):
        self.selected_animal = self.world.get_animal(event.x(), event.y())
        if self.selected_animal and self.neural_network_viewer_window:
            self.neural_network_viewer_window.network = self.selected_animal.brain

    def _draw_smells(self, painter):
        for smeller in self.world.food:
            self._draw_smell(painter, smeller)

    def _draw_smell(self, painter, smeller):
        smell_color = QColor(0, smeller.smell[0] * 255, 0, 15)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(smell_color))
        painter.drawEllipse(QRect(
            smeller.x - smeller.smell_size,
            smeller.y - smeller.smell_size,
            smeller.smell_size*2,
            smeller.smell_size*2
        ))

    def _draw_animal(self, painter, animal):
        if animal == self.selected_animal:
            painter.setPen(self._selected_animal_pen)
        else:
            painter.setPen(self._animal_pen)
        painter.setBrush(self._animal_brush)

        size = animal.size * 2
        painter.drawEllipse(QRect(animal.x - animal.size, animal.y - animal.size, size, size))

        self._draw_animal_energy_fullness(painter, animal)
        if self.animal_direction_checkbox.isChecked():
            self._draw_animal_direction(painter, animal)

    def _draw_animal_energy_fullness(self, painter, animal):
        painter.setBrush(QColor(*[255*animal.energy_fullness]*3))
        painter.drawEllipse(QRect(
            animal.x - animal.size/2,
            animal.y - animal.size/2,
            animal.size,
            animal.size
        ))

    def _draw_animal_direction(self, painter, animal):
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawLine(
            QPointF(animal.x, animal.y),
            QPointF(
                animal.x + math.cos(animal.angle) * animal.size,
                animal.y + math.sin(animal.angle) * animal.size
            )
        )

    def _draw_food(self, painter, food):
        painter.setPen(Qt.NoPen)
        if food.beated:
            painter.setBrush(self._food_beated_brush)
        else:
            painter.setBrush(self._food_brush)
        size = food.size * 2
        painter.drawEllipse(QRect(food.x - food.size, food.y - food.size, size, size))

        if self.eat_distance_checkbox.isChecked():
            self._draw_eating_distance(painter, food)

    def _draw_mammoth(self, painter, mammoth):
        r = 255 * (1.0 - mammoth.life)
        g = 215 * (1.0 - mammoth.life)
        b = 255 * mammoth.life
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(r,g,b)))
        size = mammoth.size * 2
        painter.drawEllipse(QRect(mammoth.x - mammoth.size, mammoth.y - mammoth.size, size, size))

        if self.eat_distance_checkbox.isChecked():
            self._draw_eating_distance(painter, mammoth)

    def _draw_eating_distance(self, painter, food):
        painter.setPen(QPen(
            QColor(100, 100, 100),
            0.4,
            Qt.DashLine
        ))
        painter.setBrush(Qt.NoBrush)

        radius = self.world_constants.EATING_DISTANCE + food.size
        painter.drawEllipse(QRect(
            food.x - radius, food.y - radius, radius * 2, radius * 2
        ))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mySW = MainWindow()
    mySW.show()
    sys.exit(app.exec_())