﻿from math import hypot
from random import randint, random, gauss
import numpy as np
from scipy.spatial.distance import cdist

import pymunk
from pymunk import Vec2d

from animal import Animal, Food, Mammoth


class World(object):
    OFFSET = 20

    def __init__(self, constants):
        self.constants = constants

        self.width = constants.WORLD_WIDTH
        self.height = constants.WORLD_HEIGHT
        self.space = pymunk.Space()

        static_body = pymunk.Body()
        static_lines = [
            # pymunk.Segment(static_body, Vec2d(0, 0), Vec2d(0, self.height), 1),
            # pymunk.Segment(static_body, Vec2d(0, 0), Vec2d(self.width, 0), 1),
            # pymunk.Segment(static_body, Vec2d(0, self.height), Vec2d(self.width, self.height), 1),
            # pymunk.Segment(static_body, Vec2d(self.width, 0), Vec2d(self.width, self.height), 1),
        ]
        for l in static_lines:
            l.friction = 0.3
        self.space.add(static_lines)

        self.animals = []
        self.animals_to_add = []
        self.food = []
        self.mammoths = []
        self.time = 0

        self.restart()

    def restart(self):
        self.animals = []
        self.animals_to_add = [Animal(self, self.space) for _ in range(self.constants.INITIAL_ANIMAL_COUNT)]
        self._add_new_animals()
        self.food = []
        for _ in range(self.constants.INITIAL_FOOD_COUNT):
            self.add_food(self._make_random_food())
        self.mammoths = []
        self.time = 0

    def _make_random_food(self):
        max_gauss_x = 4.5
        x = min(abs(gauss(0, 1)), max_gauss_x)
        return Food(
            self, self.space,
            # int(self.width * x / 2.5),
            randint(self.OFFSET, self.width-self.OFFSET),
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

        steps = 1
        for x in range(steps):
            self.space.step(1/60./steps)

        self.time += 1
        self._check_all_in_bounds()

        self._update_food()
        self._update_mammoths()

        self._calculate_values_of_animals_sensors()
        self._calculate_animals_closest_food()
        self._calculate_animals_close_partners()

        self._update_animals()

        self._add_new_animals()
        self._remove_dead_animals()
        self._clear_empty_food()
        self._transform_dead_mammoths()

        self._add_food_if_necessary()
        # self._add_mammoth_if_necessary()

    def _check_all_in_bounds(self):
        for food in self.food:
            self._check_in_bounds(food)
        for mammoth in self.mammoths:
            self._check_in_bounds(mammoth)
        for animal in self.animals:
            self._check_in_bounds(animal)

    def _check_in_bounds(self, animal):
        if all(body.position.x > self.width-self.OFFSET and body.velocity.x > 0 for body in animal.bodies):
            for body in animal.bodies:
                body.position = body.position.x - self.width + self.OFFSET, body.position.y
        if all(body.position.x < self.OFFSET and body.velocity.x < 0 for body in animal.bodies):
            for body in animal.bodies:
                body.position = body.position.x + self.width - self.OFFSET, body.position.y

        if all(body.position.y > self.height-self.OFFSET and body.velocity.y > 0 for body in animal.bodies):
            for body in animal.bodies:
                body.position = body.position.x, body.position.y - self.height + self.OFFSET
        if all(body.position.y < self.OFFSET and body.velocity.y < 0 for body in animal.bodies):
            for body in animal.bodies:
                body.position = body.position.x, body.position.y + self.height - self.OFFSET

        # if animal.x > self.width:
        #     animal.x = self.width
        # if animal.x < 0:
        #     animal.x = 0
        #
        # if animal.y > self.height:
        #     animal.y = self.height
        # if animal.y < 0:
        #     animal.y = 0

    def _update_food(self):
        for food in self.food:
            food.beated = False

    def _update_mammoths(self):
        for mammoth in self.mammoths:
            mammoth.update()

    def _calculate_values_of_animals_sensors(self):
        smellers = self.food
        smellers_pos = np.array([[smeller.x, smeller.y] for smeller in smellers], dtype=np.float64)
        smells_sizes = np.array([smeller.smell_size for smeller in smellers], dtype=np.float64)
        smells = np.array([smeller.smell for smeller in smellers], dtype=np.float64)
        smells = np.transpose(smells)

        sensors_pos = []
        for animal in self.animals:
            sensors_pos.extend(animal.sensors_positions)
        sensors_pos = np.array(sensors_pos, dtype=np.float64)

        incidence = cdist(sensors_pos, smellers_pos)
        smells_strength = np.nan_to_num(np.maximum(0, 1 - incidence / smells_sizes)) ** 2

        for animal in self.animals:
            animal.sensor_values = []

        for i, sensor_smell_strength in enumerate(smells_strength):
            sensor_values = np.max(sensor_smell_strength * smells, axis=1)
            animal_id = i // self.constants.ANIMAL_SENSOR_COUNT
            self.animals[animal_id].sensor_values.extend(sensor_values)

    def _calculate_animals_closest_food(self):
        eatable = self.food
        food_positions = np.array([[food.x, food.y] for food in eatable], dtype=np.float64)
        animals_positions = np.array([[animal.x, animal.y] for animal in self.animals], dtype=np.float64)
        distances = cdist(animals_positions, food_positions)
        closest_food_indexes = np.argmin(distances, axis=1)
        for animal_i, food_i in enumerate(closest_food_indexes):
            if distances[animal_i, food_i] <= self.constants.EATING_DISTANCE + self.animals[animal_i].size + eatable[food_i].size:
                self.animals[animal_i].closest_food = eatable[food_i]
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

    def _add_new_animals(self):
        self.animals.extend(self.animals_to_add)
        for animal in self.animals_to_add:
            for body in animal.bodies:
                self.add_to_space(body)
        self.animals_to_add = []

    def _remove_dead_animals(self):
        for animal in self.animals[:]:
            if animal.energy <= 0:
                for body in animal.bodies:
                    self.space.remove(body.shapes)
                    self.space.remove(body.constraints)
                    self.space.remove(body)
                self.animals.remove(animal)

    def _clear_empty_food(self):
        for food in self.food[:]:
            if food.size <= 0:
                for body in food.bodies:
                    self.space.remove(body.shapes)
                    self.space.remove(body.constraints)
                    self.space.remove(body)
                self.food.remove(food)

    def _transform_dead_mammoths(self):
        for mammoth in self.mammoths[:]:
            if mammoth.life <= 0:
                self.mammoths.remove(mammoth)
                self._make_food_from_mammoth(mammoth)

    def _make_food_from_mammoth(self, mammoth):
        for _ in range(self.constants.FOOD_FROM_MAMMOTH_COUNT):
            x = mammoth.x + (mammoth.smell_size*random()*2 - mammoth.smell_size)*0.5
            y = mammoth.y + (mammoth.smell_size*random()*2 - mammoth.smell_size)*0.5
            self.add_food(Food(self, self.space, x, y, mammoth.size))

    def _add_food_if_necessary(self):
        if self.time % self.constants.FOOD_TIMER == 0:
            for _ in range(self.constants.APPEAR_FOOD_COUNT):
                self.add_food(self._make_random_food())

    def add_food(self, food):
        self.food.append(food)
        for body in food.bodies:
            self.add_to_space(body)

    def _add_mammoth_if_necessary(self):
        if self.time % self.constants.FOOD_TIMER == 0 and len(self.mammoths) < self.constants.MAMMOTH_COUNT:
            self.mammoths.append(self._make_random_mammoth())

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


    def add_to_space(self, body):
        body.velocity_limit = 100
        pj = pymunk.PivotJoint(self.space.static_body, body, Vec2d.zero(), Vec2d.zero())
        pj.max_force = 1000
        pj.max_bias = 0
        pj.ignore_draw = True
        self.space.add(pj)

        gj = pymunk.GearJoint(self.space.static_body, body, 0.0, 1.0)
        gj.max_force = 5000
        gj.max_bias = 0
        gj.ignore_draw = True
        self.space.add(gj)

        # space.add(body)
        return body
