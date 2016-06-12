﻿from math import sqrt
from random import randint, random, gauss
import numpy as np
from scipy.spatial.distance import cdist

from animal import Animal, Food, Mammoth, Gender


def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def close_enough(animal1, animal2, max_distance):
    return distance(animal1.x, animal1.y, animal2.x, animal2.y) < max_distance + animal1.size + animal2.size


class World(object):
    def __init__(self, constants):
        self.constants = constants
        self._calculate_chunks_sizes()

        self.width = constants.WORLD_WIDTH
        self.height = constants.WORLD_HEIGHT

        self.restart()
        self.food_timer = self.constants.DEFAULT_TIMER

    def _calculate_chunks_sizes(self):
        self.food_chunk_size = self.constants.EATING_DISTANCE + self.constants.ANIMAL_SIZE
        self.female_chunk_size = self.constants.SEX_DISTANCE + self.constants.ANIMAL_SIZE * 2

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
        self._prepare_empty_chunks()
        self._split_food_to_chunks()
        self._split_mammoths_to_chunks()
        self._split_animals_to_chunks()

        self._calculate_values_of_animals_sensors()

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

    def _prepare_empty_chunks(self):
        self.food_chunks = self._make_empty_chunks(self.food_chunk_size)
        self.female_chunks = self._make_empty_chunks(self.female_chunk_size)

    def _split_food_to_chunks(self):
        for food in self.food:
            food.beated = False
            self._check_in_bounds(food)
            # food chunks
            chunk_row, chunk_col = self.get_chunk_index(food.x, food.y, self.food_chunk_size)
            self.food_chunks[chunk_row][chunk_col].append(food)

    def _split_mammoths_to_chunks(self):
        for mammoth in self.mammoths:
            self._check_in_bounds(mammoth)
            # food chunks
            chunk_row, chunk_col = self.get_chunk_index(mammoth.x, mammoth.y, self.food_chunk_size)
            self.food_chunks[chunk_row][chunk_col].append(mammoth)

    def _split_animals_to_chunks(self):
        for animal in self.animals:
            self._check_in_bounds(animal)
            # female chunks
            if animal.gender == Gender.FEMALE:
                chunk_row, chunk_col = self.get_chunk_index(animal.x, animal.y, self.female_chunk_size)
                self.female_chunks[chunk_row][chunk_col].append(animal)

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


    def _add_food_if_necessary(self):
        if self.time % self.food_timer == 0:
            for _ in range(self.constants.APPEAR_FOOD_COUNT):
                self.food.append(self._make_random_food())

    def _add_mammoth_if_necessary(self):
        if self.time % self.food_timer == 0 and len(self.mammoths) < self.constants.MAMMOTH_COUNT:
            self.mammoths.append(self._make_random_mammoth())

    def _update_animal(self, animal):
        food = self.get_closest_food(animal.x, animal.y, self.constants.EATING_DISTANCE + animal.size)
        if food:
            animal.eat(food)
        animal.close_females = [female for female in self._adjacent_females(animal.x, animal.y) if
                                close_enough(animal, female, self.constants.SEX_DISTANCE)]
        animal.update()

    def get_closest_food(self, x, y, max_distance):
        min_dist = 10000
        res = None
        for food in self._adjacent_food(x, y):
            dist = distance(x, y, food.x, food.y)
            if dist <= food.size + max_distance and dist < min_dist:
                min_dist = dist
                res = food
        return res

    def _check_in_bounds(self, animal):
        if animal.x > self.width:
            animal.x = self.width
        if animal.x < 0:
            animal.x = 0

        if animal.y > self.height:
            animal.y = self.height
        if animal.y < 0:
            animal.y = 0

    def _adjacent_elements(self, chunks, chunk_size, x, y):
        for chunk_row, chunk_col in self._adjacent_chunks(chunks, *self.get_chunk_index(x, y, chunk_size)):
            chunk = chunks[chunk_row][chunk_col]
            for element in chunk:
                yield element

    def _adjacent_food(self, x, y):
        return self._adjacent_elements(self.food_chunks, self.food_chunk_size, x, y)

    def _adjacent_females(self, x, y):
        return self._adjacent_elements(self.female_chunks, self.female_chunk_size, x, y)

    def _adjacent_chunks(self, chunks, row, col):
        r, c = row - 1, col - 1
        for i in range(9):
            ri = r + i // 3
            ci = c + i % 3
            if 0 <= ri < len(chunks) and 0 <= ci < len(chunks[0]):
                yield (r + i // 3, c + i % 3)

    def get_chunk_index(self, x, y, chunk_size):
        return (int(y // chunk_size), int(x // chunk_size))

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
            dist = distance(x, y, animal.x, animal.y)
            if dist < closest_dist:
                closest_animal = animal
                closest_dist = dist
        return closest_animal

    def _make_empty_chunks(self, chunk_size):
        return [
            [[] for _ in range(int(self.width / chunk_size) + 1)]
            for _ in range(int(self.height / chunk_size) + 1)
            ]
