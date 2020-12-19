from math import hypot
from random import randint, random, gauss

import numpy as np
from scipy.spatial.distance import cdist

from engine.animal import Animal, Food, Mammoth
from engine.world_constants import WorldConstants


class World(object):
    def __init__(self, constants, save_genealogy=False):
        assert isinstance(constants, WorldConstants)
        self.constants = constants
        self.save_genealogy = save_genealogy

        self.width = constants.WORLD_WIDTH
        self.height = constants.WORLD_HEIGHT

        self.first_generation = []
        self.animals = []
        self.animals_to_add = []
        self.food = []
        self.mammoths = []
        self.time = 0
        self.analyzers = []
        self.analysis_period = 20000

        self.restart()

    def restart(self):
        self.animals = [
            Animal(self, self.constants.ANIMAL_WORLD_START_ENERGY, save_genealogy=self.save_genealogy)
            for _ in range(self.constants.INITIAL_ANIMAL_COUNT)
        ]
        if self.save_genealogy:
            self.first_generation = self.animals.copy()
        self.animals_to_add = []
        self.food = [self._make_random_food() for _ in range(self.constants.INITIAL_FOOD_COUNT)]
        self.mammoths = []
        self.time = 0
        self.max_generation = 0

        for analyzer in self.analyzers:
            analyzer.reset()

    def _make_random_food(self):
        if self.constants.FOOD_GAUSS_DISTRIBUTION_SIGMA:  # gauss distribution if sigma was set
            x_ratio = abs(gauss(0, 1)) / self.constants.FOOD_GAUSS_DISTRIBUTION_SIGMA
            while x_ratio > 1:
                x_ratio = abs(gauss(0, 1)) / self.constants.FOOD_GAUSS_DISTRIBUTION_SIGMA
            # x_ratio is now between 0 and 1
        else:  # uniform distribution
            x_ratio = random()

        return Food(
            self,
            int(self.width * x_ratio),
            randint(0, self.height),
            randint(self.constants.APPEAR_FOOD_SIZE_MIN, self.constants.APPEAR_FOOD_SIZE_MAX)
        )

    def _make_random_mammoth(self):
        x, y = randint(self.width / 2, self.width), randint(1, self.height)
        while self._is_close_to_others_mammoths(x, y):
            x, y = randint(self.width / 2, self.width), randint(1, self.height)
        return Mammoth(
            self, x, y,
            randint(self.constants.APPEAR_FOOD_SIZE_MIN, self.constants.APPEAR_FOOD_SIZE_MAX)
        )

    def _is_close_to_others_mammoths(self, x, y):
        if not self.mammoths:
            return False
        distances = cdist([[x,y]], [[m.x, m.y] for m in self.mammoths])
        return np.min(distances) < self.constants.MAMMOTH_MIN_DISTANCE_TO_OTHERS

    def update(self):
        self.time += 1
        self._check_all_in_bounds()

        self._update_food()
        self._update_mammoths()

        self._calculate_values_of_animals_sensors()
        self._calculate_animals_closest_food()
        self._calculate_animals_close_partners()

        self._update_animals()

        self._analyze_after_animals_update()

        self._add_new_animals()
        self._remove_dead_animals()
        self._remove_empty_food()
        self._transform_dead_mammoths()

        self._add_food_if_necessary()
        self._add_mammoth_if_necessary()

        self._analyze_in_the_end()

    def _check_all_in_bounds(self):
        for food in self.food:
            self._check_in_bounds(food)
        for mammoth in self.mammoths:
            self._check_in_bounds(mammoth)
        for animal in self.animals:
            self._check_in_bounds(animal)

    def _check_in_bounds(self, animal):
        if animal.x > self.width:
            animal.x = self.width
        if animal.x < 0:
            animal.x = 0

        if animal.y > self.height:
            animal.y = self.height
        if animal.y < 0:
            animal.y = 0

    def _update_food(self):
        for food in self.food:
            food.update()

    def _update_mammoths(self):
        for mammoth in self.mammoths:
            mammoth.update()

    def _calculate_values_of_animals_sensors(self):
        smellers = self.food + self.mammoths + self.animals
        smellers_pos = np.array([[smeller.x, smeller.y] for smeller in smellers], dtype=np.float64)
        smells_sizes = np.array([smeller.smell_size for smeller in smellers], dtype=np.float64)
        smells = np.array([smeller.smell for smeller in smellers], dtype=np.float64)
        smells = np.transpose(smells)

        sensors_pos = []
        for animal in self.animals:
            sensors_pos.extend(animal.sensors_positions)
        sensors_pos = np.array(sensors_pos, dtype=np.float64)

        incidence = cdist(sensors_pos, smellers_pos)
        with np.errstate(divide='ignore'):
            smells_strength = np.nan_to_num(np.maximum(0, 1 - incidence / smells_sizes)) ** 2

        for animal in self.animals:
            animal.sensor_values = []

        for i, sensor_smell_strength in enumerate(smells_strength):
            sensor_values = np.max(sensor_smell_strength * smells, axis=1)
            animal_id = i // self.constants.ANIMAL_SENSOR_COUNT
            self.animals[animal_id].sensor_values.extend(sensor_values)

    def _calculate_animals_closest_food(self):
        eatable = self.food + self.mammoths
        for food in eatable:
            food.biting_animals_amount = 0

        food_positions = np.array([[food.x, food.y] for food in eatable], dtype=np.float64)
        animals_positions = np.array([[animal.x, animal.y] for animal in self.animals], dtype=np.float64)
        distances = cdist(animals_positions, food_positions)
        closest_food_indexes = np.argmin(distances, axis=1)
        for animal_i, food_i in enumerate(closest_food_indexes):
            if distances[animal_i, food_i] <= self.constants.EATING_DISTANCE + self.animals[animal_i].size + eatable[food_i].size:
                self.animals[animal_i].closest_food = eatable[food_i]
                eatable[food_i].biting_animals_amount += 1
            else:
                self.animals[animal_i].closest_food = None

    def _calculate_animals_close_partners(self):
        """
        method doesn't respect individual animal's sizes, so SEX_DISTANCE must involve ANIMAL_SIZE
        """
        animals_pos = np.array([[animal.x, animal.y] for animal in self.animals], dtype=np.float64)
        distances = cdist(animals_pos, animals_pos)
        for animal, distance_to_partners in zip(self.animals, distances):
            partners_indexes = np.nonzero(distance_to_partners < self.constants.SEX_DISTANCE)[0]
            animal.close_partners = [self.animals[i] for i in partners_indexes if self.animals[i] != animal]

    def _update_animals(self):
        for animal in self.animals:
            animal.update()

    def _analyze_after_animals_update(self):
        for analyzer in self.analyzers:
            analyzer.analyze_after_animals_update(self)

    def _analyze_in_the_end(self):
        for analyzer in self.analyzers:
            analyzer.analyze_in_the_end(self)

    def _add_new_animals(self):
        if self.animals_to_add:
            self.animals.extend(self.animals_to_add)
            self.max_generation = max(self.max_generation, max(a.generation for a in self.animals_to_add))
            self.animals_to_add = []

    def _remove_dead_animals(self):
        self.animals = [animal for animal in self.animals if animal.energy > 0]

    def _remove_empty_food(self):
        self.food = [food for food in self.food if food.size > 0]

    def _transform_dead_mammoths(self):
        for mammoth in self.mammoths[:]:
            if mammoth.size <= 0:
                self.mammoths.remove(mammoth)

    def _add_food_if_necessary(self):
        if self.time % self.constants.FOOD_TIMER == 0:
            for _ in range(self.constants.APPEAR_FOOD_COUNT):
                self.food.append(self._make_random_food())

    def _add_mammoth_if_necessary(self):
        if self.time % self.constants.FOOD_TIMER == 0 and len(self.mammoths) < self.constants.MAMMOTH_COUNT:
            self.mammoths.append(self._make_random_mammoth())

    def add_animal(self, animal):
        self.animals_to_add.append(animal)

    def get_animal(self, x, y) -> Animal:
        closest_animal = None
        closest_dist = self.constants.ANIMAL_SIZE + 10
        for animal in self.animals:
            dist = hypot(x - animal.x, y - animal.y)
            if dist < closest_dist:
                closest_animal = animal
                closest_dist = dist
        return closest_animal
