import datetime
import math
import os
import time
from statistics import mean

from PyQt5.QtCore import QTimer, pyqtSlot as Slot, QRect, Qt, QPointF, QDir
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from analyzers import MammothAnalyzer
from engine import serializer
from ui.constants_window import ConstantsWindow
from ui.graphics_window import GraphicsWindow
from ui.main_window_ui import Ui_MainWindow
from ui.neural_network_viewer import NeuralNetworkViewer
from ui.population_graph_window import PopulationGraphWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    _PERFORMANCE_CALC_INTERVAL = 100
    TIMER_INTERVAL = 1

    def __init__(self, world, parent=None):
        super().__init__(parent)
        self.info_text = []
        self.performance = 0
        self._animal_brush = QBrush(QColor(74, 172, 225))
        self._food_brush = QBrush(QColor(100, 100, 100))
        self._food_bitten_brush = QBrush(QColor(180, 140, 100))
        self._mammoth_brush = QBrush(QColor(50, 50, 200))
        self._animal_pen = Qt.NoPen
        self._selected_animal_pen = QPen(QColor(255, 180, 0), 3)
        self.selected_animal = None
        self.constants_window = None
        self.neural_network_viewer_window = None
        self.population_graph_window = None
        self.graphics_window = None

        self.setupUi(self)
        self.horizontalLayout.insertWidget(0, self.draw_widget)
        snapshot_dir = QDir('./snapshots/')
        snapshot_dir.mkpath('.')
        self.snapshot_directory_combobox.addItem(snapshot_dir.absolutePath())

        self.world = world

        self.draw_widget.paintEvent = self.on_draw_widget_paintEvent
        self.draw_widget.mousePressEvent = self.on_draw_widget_mousePressEvent
        self.draw_widget.mouseMoveEvent = self.on_draw_widget_mouseMoveEvent

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.start(self.TIMER_INTERVAL)

        self._prev_time = time.perf_counter()

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, new_world):
        self._world = new_world

        self.mammoth_analyzer = MammothAnalyzer(self.world)
        if self.constants_window:
            self.constants_window.constants = self.world.constants
        if self.population_graph_window:
            self.population_graph_window.world = self.world
            self.population_graph_window.selected_animal = self.selected_animal

        if self.graphics_window:
            self.graphics_window.world = self.world

        self.draw_widget.setFixedWidth(self.world.constants.WORLD_WIDTH)
        self.draw_widget.setFixedHeight(self.world.constants.WORLD_HEIGHT)

    @Slot()
    def on_timer_button_clicked(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(self.TIMER_INTERVAL)

    @Slot()
    def on_constants_action_triggered(self):
        if not self.constants_window:
            self.constants_window = ConstantsWindow(self.world.constants, parent=self)
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
    def on_action_population_graph_triggered(self):
        if not self.population_graph_window:
            self.population_graph_window = PopulationGraphWindow(world=self.world,
                                                                 selected_animal=self.selected_animal,
                                                                 parent=self)
        if self.population_graph_window.isVisible():
            self.population_graph_window.hide()
        else:
            self.population_graph_window.show()

    @Slot()
    def on_graphics_action_triggered(self):
        if not self.graphics_window:
            self.graphics_window = GraphicsWindow(world=self.world, parent=self)
        if self.graphics_window.isVisible():
            self.graphics_window.hide()
        else:
            self.graphics_window.show()

    @Slot()
    def on_save_action_triggered(self):
        self.make_snapshot()

    @Slot()
    def on_load_action_triggered(self):
        filename = QFileDialog.getOpenFileName(
            self,
            "Open world dump file",
            self.snapshot_directory_combobox.currentText(),
            "WORLD Files (*.wrld)",
            options=QFileDialog.DontUseNativeDialog
        )[0]
        if not filename:
            return

        new_world = serializer.load(filename)
        self.world = new_world
        if filename.startswith(self.snapshot_directory_combobox.currentText()):
            world_name = filename[len(self.snapshot_directory_combobox.currentText()) + 1:]
            if world_name.endswith('.wrld'):
                world_name = world_name[:-len('.wlrd')]
            self.setWindowTitle(f'MainWindow - {world_name}')

    @Slot()
    def on_browse_snapshot_directory_button_clicked(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Directory for saving snapshots",
            self.snapshot_directory_combobox.currentText(),
            options=QFileDialog.DontUseNativeDialog
        )
        if not directory:
            return
        if self.snapshot_directory_combobox.findText(directory) == -1:
            self.snapshot_directory_combobox.addItem(directory)

        self.snapshot_directory_combobox.setCurrentIndex(self.snapshot_directory_combobox.findText(directory))

    @Slot()
    def on_timer_timeout(self):
        self._measure_performance()
        self.world.update()
        self.mammoth_analyzer.update()
        if self.graphics_window and not self.graphics_window.isHidden():
            self.graphics_window.update()
        self._update_text_info()
        self._evoke_repaint_event()
        self._make_snapshot_if_need()

    def _measure_performance(self):
        if self.world.time % self._PERFORMANCE_CALC_INTERVAL == 0:
            self.performance = (time.perf_counter() - self._prev_time) / self._PERFORMANCE_CALC_INTERVAL
            self._prev_time = time.perf_counter()

        if self.world.time == 200:
            print(self.performance)

    def _update_text_info(self):
        self.info_text.append(('Performance', f'{self.performance:.6f}'))
        self.info_text.append(("World time", self.world.time))
        self.info_text.append(("Food timer", self.world.constants.FOOD_TIMER))
        self.info_text.append(("Animal count", len(self.world.animals)))
        self.info_text.append(("Food count", len(self.world.food)))
        self.info_text.append(("Mammoth count", len(self.world.mammoths)))
        self.info_text.append(("Mammoth kills", f'{self.mammoth_analyzer.amount_of_killings:.5f}'))
        avg_lifetime = mean(x[1] for x in self.world.animal_deaths) if self.world.animal_deaths else 0
        self.info_text.append(("Animal lifetime", f'{avg_lifetime:.0f}'))
        new_avg_energy = mean(x[1] for x in self.world.new_animal_avg_energy) if self.world.new_animal_avg_energy else 0
        self.info_text.append(("New animal energy", f'{new_avg_energy:.2f}'))
        self.info_label.setText('\n'.join('{:<20} {:<10}'.format(*args) for args in self.info_text))
        self.info_text.clear()

    def _evoke_repaint_event(self):
        if self.world.time % self.draw_each_times_slider.value() == 0:
            self.draw_widget.repaint()
            if self.neural_network_viewer_window and self.neural_network_viewer_window.isVisible():
                self.neural_network_viewer_window.repaint()
            if self.population_graph_window and self.population_graph_window.isVisible():
                self.population_graph_window.redraw()
            if self.graphics_window and self.graphics_window.isVisible():
                self.graphics_window.redraw()

    def _make_snapshot_if_need(self):
        if self.make_snapshots_checkbox.isChecked() and self.world.time % self.make_snapshots_spinbox.value() == 0:
            self.make_snapshot()

    def make_snapshot(self):
        now = datetime.datetime.now().strftime("%FT%T")
        world_name = self.world_name_lineedit.text()
        if world_name:
            world_name += '--'

        git_commit = os.popen('git rev-parse --short HEAD').read().strip() or 'world'
        filename = f'{now}--{git_commit}--{world_name}{self.world.time}.wrld'
        file_path = os.path.join(self.snapshot_directory_combobox.currentText(), filename)
        try:
            serializer.save(self.world, file_path)
            print("saved into {}".format(file_path))
        except IOError:
            QMessageBox.critical(self, "Unable to open file", "There was an error opening \"%s\"" % file_path)
            return

    # PAINTING

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

        if self.selected_animal:
            self._draw_animal(painter, self.selected_animal, selected=True)

        painter.end()

    def on_draw_widget_mousePressEvent(self, event):
        self.selected_animal = self.world.get_animal(event.x(), event.y())
        if self.neural_network_viewer_window:
            self.neural_network_viewer_window.network = self.selected_animal.brain if self.selected_animal else None
            self.neural_network_viewer_window.repaint()
        if self.population_graph_window:
            self.population_graph_window.selected_animal = self.selected_animal
        self.draw_widget.repaint()

    def on_draw_widget_mouseMoveEvent(self, event):
        if self.selected_animal and self.move_radiobutton.isChecked():
            self.selected_animal.x = event.x()
            self.selected_animal.y = event.y()
            self.draw_widget.repaint()
            if self.neural_network_viewer_window:
                self.neural_network_viewer_window.repaint()


    def _draw_smells(self, painter):
        for smeller in self.world.mammoths + self.world.food + self.world.animals:
            self._draw_smell(painter, smeller)

    def _draw_smell(self, painter, smeller):
        smell_color = QColor(smeller.smell[2] * 255, smeller.smell[1] * 255, smeller.smell[0] * 255, 15)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(smell_color))
        painter.drawEllipse(QRect(
            smeller.x - smeller.smell_size,
            smeller.y - smeller.smell_size,
            smeller.smell_size*2,
            smeller.smell_size*2
        ))

    def _draw_animal(self, painter, animal, selected=False):
        if selected:
            painter.setPen(self._selected_animal_pen)
        else:
            painter.setPen(self._animal_pen)
        painter.setBrush(QBrush(get_color(animal.energy_for_birth / self.world.constants.ENERGY_FOR_BIRTH_DIFF)))

        size = animal.size * 2
        painter.drawEllipse(QRect(animal.x - animal.size, animal.y - animal.size, size, size))

        self._draw_animal_energy_fullness(painter, animal)
        if self.animal_direction_checkbox.isChecked():
            self._draw_animal_direction(painter, animal)

    def _draw_animal_energy_fullness(self, painter, animal):
        painter.setPen(Qt.NoPen)
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
        if food.bitten:
            painter.setBrush(self._food_bitten_brush)
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

        radius = self.world.constants.EATING_DISTANCE + food.size
        painter.drawEllipse(QRect(
            food.x - radius, food.y - radius, radius * 2, radius * 2
        ))


def get_color(color):
    r, g, b = max(0, -color), max(0, color), 0
    return QColor(r * 255, g * 255, b * 255)
