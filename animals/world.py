from math import hypot
from random import randint, random, gauss
import numpy as np
from scipy.spatial.distance import cdist

from animal import Animal, Food, Mammoth, Gender


class World(object):
    def __init__(self, constants):
        self.constants = constants

        self.width = constants.WORLD_WIDTH
        self.height = constants.WORLD_HEIGHT

        self.restart()
        self.food_timer = self.constants.DEFAULT_TIMER

    def restart(self):
        self.animals = [Animal(self) for _ in range(self.constants.INITIAL_ANIMAL_COUNT)]
        self.animals_to_add = []
        self.dead_animals = []
        self.empty_food = []
        self.dead_mammoths = []
        self.food = [self._make_random_food() for _ in range(self.constants.INITIAL_FOOD_COUNT)]
        self.mammoths = [self._make_random_mammoth() for _ in range(self.constants.MAMMOTH_COUNT)]
        self.time = 0

    def _make_random_food(self):
        max_gauss_x = 4.5
        x = min(abs(gauss(0, 1)), max_gauss_x)
        return Food(
            self,
            int(self.width * x / 2.5),
            randint(0, self.height),
            randint(self.constants.APPEAR_FOOD_SIZE_MIN, self.constants.APPEAR_FOOD_SIZE_MAX)
        )

    def _make_random_mammoth(self):
        return Mammoth(
            self,
            randint(self.width / 2, self.width),
            randint(self.height / 2, self.height),
            randint(self.constants.APPEAR_FOOD_SIZE_MIN, self.constants.APPEAR_FOOD_SIZE_MAX)
        )

    def update(self):
        self.time += 1
        self._check_animals_in_bounds()
        self._update_food()
        self._update_mammoths()

        self._calculate_values_of_animals_sensors()
        self._calculate_closest_food()
        self._calculate_close_females()

        for mammoth in self.mammoths:
            mammoth.update()

        for animal in self.animals:
            self._update_animal(animal)

        self.animals.extend(self.animals_to_add)
        self.animals_to_add = []
        self._remove_dead_animals()
        self._clear_empty_food()
        self._transform_dead_mammoths()

        self._add_food_if_necessary()
        self._add_mammoth_if_necessary()

    def _update_food(self):
        for food in self.food:
            food.beated = False
            self._check_in_bounds(food)

    def _update_mammoths(self):
        for mammoth in self.mammoths:
            self._check_in_bounds(mammoth)

    def _check_animals_in_bounds(self):
        for animal in self.animals:
            self._check_in_bounds(animal)

    def _calculate_values_of_animals_sensors(self):
        self.smellers = self.animals + self.food + self.mammoths
        smellers_pos = np.array([[smeller.x, smeller.y] for smeller in self.smellers], dtype=np.float64)
        smells_sizes = np.array([smeller.smell_size for smeller in self.smellers], dtype=np.float64)
        smells = np.array([smeller.smell for smeller in self.smellers], dtype=np.float64)
        smells = np.transpose(smells)

        sensors_pos = []
        for animal in self.animals:
            sensors_pos.extend(animal.sensors_positions)
        sensors_pos = np.array(sensors_pos, dtype=np.float64)

        self.incidence = cdist(sensors_pos, smellers_pos)
        self.smells_strength = np.maximum(0, 1 - self.incidence / smells_sizes) ** 2

        for animal in self.animals:
            animal.sensor_values = []

        for i, sensor_smell_strength in enumerate(self.smells_strength):
            sensor_values = np.max(sensor_smell_strength * smells, axis=1)
            animal_id = i // self.constants.ANIMAL_SENSOR_COUNT
            sensor_id = i % self.constants.ANIMAL_SENSOR_COUNT
            self.animals[animal_id].sensor_values.extend(sensor_values)

    def _calculate_closest_food(self):
        eatable = self.food + self.mammoths
        food_positions = np.array([[food.x, food.y] for food in eatable], dtype=np.float64)
        animals_positions = np.array([[animal.x, animal.y] for animal in self.animals], dtype=np.float64)
        distances = cdist(animals_positions, food_positions)
        closest_food_indexes = np.argmin(distances, axis=1)
        for animal_i, food_i in enumerate(closest_food_indexes):
            if distances[animal_i, food_i] <= self.constants.EATING_DISTANCE + self.animals[animal_i].size + eatable[food_i].size:
                self.animals[animal_i].closest_food = eatable[food_i]
            else:
                self.animals[animal_i].closest_food = None

    def _calculate_close_females(self):
        """
        method doesn't respect individual animal's sizes, so SEX_DISTANCE must involve ANIMAL_SIZE
        """
        animals_pos = np.array([[animal.x, animal.y] for animal in self.animals], dtype=np.float64)
        distances = cdist(animals_pos, animals_pos)
        for animal_i, distance_to_others in enumerate(distances):
            females_indexes = np.nonzero(distance_to_others < self.constants.SEX_DISTANCE)[0]
            females = [self.animals[i] for i in females_indexes if i != animal_i and self.animals[i].gender == Gender.FEMALE]
            self.animals[animal_i].close_females = females

    def _add_food_if_necessary(self):
        if self.time % self.food_timer == 0:
            for _ in range(self.constants.APPEAR_FOOD_COUNT):
                self.food.append(self._make_random_food())

    def _add_mammoth_if_necessary(self):
        if self.time % self.food_timer == 0 and len(self.mammoths) < self.constants.MAMMOTH_COUNT:
            self.mammoths.append(self._make_random_mammoth())

    def _update_animal(self, animal):
        if animal.closest_food:
            animal.eat(animal.closest_food)
        animal.update()

    def _check_in_bounds(self, animal):
        if animal.x > self.width:
            animal.x = self.width
        if animal.x < 0:
            animal.x = 0

        if animal.y > self.height:
            animal.y = self.height
        if animal.y < 0:
            animal.y = 0

    def _remove_dead_animals(self):
        self.dead_animals = []
        for animal in self.animals[:]:
            if animal.energy <= 0:
                self.animals.remove(animal)
                self.dead_animals.append(animal)

    def _clear_empty_food(self):
        self.empty_food = []
        for food in self.food[:]:
            if food.size <= 0:
                self.food.remove(food)
                self.empty_food.append(food)

    def _transform_dead_mammoths(self):
        self.dead_mammoths = []
        for mammoth in self.mammoths[:]:
            if mammoth.life <= 0:
                self.mammoths.remove(mammoth)
                self.dead_mammoths.append(mammoth)
                self._make_food_from_mammoth(mammoth)

    def _make_food_from_mammoth(self, mammoth):
        for _ in range(self.constants.FOOD_FROM_MAMMOTH_COUNT):
            x = mammoth.x + (mammoth.smell_size*random()*2 - mammoth.smell_size)*0.5
            y = mammoth.y + (mammoth.smell_size*random()*2 - mammoth.smell_size)*0.5
            self.food.append(Food(self, x, y, mammoth.size))

    def add_animal(self, animal):
        self.animals_to_add.append(animal)

    def get_animal(self, x, y):
        closest_animal = None
        closest_dist = self.constants.ANIMAL_SIZE + 10
        for animal in self.animals:
            dist = hypot(x - animal.x, y - animal.y)
            if dist < closest_dist:
                closest_animal = animal
                closest_dist = dist
        return closest_animal
