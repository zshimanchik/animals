import sys
import time
from PySide.QtCore import QTimer, SIGNAL, Slot, QRect, Qt
from PySide.QtGui import QMainWindow, QPainter, QApplication, QBrush, QPen, QColor

from main_window_ui import Ui_MainWindow
import world
from world_constants import WorldConstants
from animal import Gender


class MainWindow(QMainWindow, Ui_MainWindow):
    _PERFORMANCE_CALC_INTERVAL = 20

    def __init__(self, parent=None):
        super().__init__(parent)
        self._animal_female_brush = QBrush(QColor(200, 50, 50))
        self._animal_male_brush = QBrush(QColor(50, 200, 50))
        self._food_brush = QBrush(QColor(100, 100, 100))
        self._food_beated_brush = QBrush(QColor(180, 140, 100))
        self._mammoth_brush = QBrush(QColor(50, 50, 200))
        self._animal_pen = Qt.NoPen

        self.setupUi(self)

        self.world_constants = WorldConstants()
        self.draw_widget.setFixedWidth(self.world_constants.WORLD_WIDTH)
        self.draw_widget.setFixedHeight(self.world_constants.WORLD_HEIGHT)

        self.world = world.World(constants=self.world_constants, thread_count=1)
        self.draw_widget.paintEvent = self.on_draw_widget_paintEvent

        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.on_timer_timeout)
        self.timer.start(1)

        self._prev_time = time.time()

    @Slot()
    def on_timer_button_clicked(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(1)

    @Slot()
    def on_timer_timeout(self):
        if self.world.time % self._PERFORMANCE_CALC_INTERVAL == 0:
            self.performance = (time.time() - self._prev_time) / self._PERFORMANCE_CALC_INTERVAL
            self._prev_time = time.time()
            self.performance_label.setText(str(self.performance))

        self.world.update()
        self.world_time_label.setText(str(self.world.time))
        self.animal_count_label.setText(str(len(self.world.animals)))
        self.food_count_label.setText(str(len(self.world.food)))
        self.draw_widget.repaint()

    def on_draw_widget_paintEvent(self, event):
        painter = QPainter()
        painter.begin(self.draw_widget)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawText(QRect(0, 0, 100, 100), Qt.AlignCenter, "Qt")
        for animal in self.world.animals:
            self._draw_animal(painter, animal)
        for food in self.world.food:
            self._draw_food(painter, food)
        for mammoth in self.world.mammoths:
            self._draw_mammoth(painter, mammoth)

        painter.end()

    def _draw_animal(self, painter, animal):
        painter.setPen(self._animal_pen)
        if animal.gender == Gender.FEMALE:
            painter.setBrush(self._animal_female_brush)
        else:
            painter.setBrush(self._animal_male_brush)

        size = animal.size * 2
        painter.drawEllipse(QRect(animal.x - animal.size, animal.y - animal.size, size, size))

    def _draw_food(self, painter, food):
        painter.setPen(Qt.NoPen)
        if food.beated:
            painter.setBrush(self._food_beated_brush)
        else:
            painter.setBrush(self._food_brush)
        size = food.size * 2
        painter.drawEllipse(QRect(food.x - food.size, food.y - food.size, size, size))

        if self.eat_distance_checkbox.isChecked():
            self._draw_food_eating_distance(painter, food)

    def _draw_food_eating_distance(self, painter, food):
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

    def _draw_mammoth(self, painter, mammoth):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._mammoth_brush)
        size = mammoth.size * 2
        painter.drawEllipse(QRect(mammoth.x - mammoth.size, mammoth.y - mammoth.size, size, size))




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mySW = MainWindow()
    mySW.show()
    sys.exit(app.exec_())