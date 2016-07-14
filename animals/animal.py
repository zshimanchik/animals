import math
from random import random, randint

from brain import create_brain

TWO_PI = math.pi * 2


class Food(object):
    def __init__(self, world, x, y, size):
        self._world = world
        self.x = x
        self.y = y
        self._size = size
        self._smell = (1.0,)
        self._smell_size = self._size * self._world.constants.FOOD_SMELL_SIZE_RATIO
        self.beated = False

    def beating(self, value):
        self.beated = True
        real_value = min(self.size, value)
        self.size -= real_value
        return real_value * self._world.constants.FOOD_SIZE_TO_ENERGY_RATIO

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = max(0, value)
        self._smell_size = self._size * self._world.constants.FOOD_SMELL_SIZE_RATIO

    @property
    def smell_size(self):
        return self._smell_size

    @property
    def smell(self):
        return self._smell


class Mammoth(object):
    def __init__(self, world, x, y, size):
        self._world = world
        self.x = x
        self.y = y
        self.size = size
        self.smell = (0.0,)
        self.smell_size = self.size * self._world.constants.MAMMOTH_SMELL_SIZE_RATIO
        self.life = 1

    def beating(self, value):
        self.life -= self._world.constants.MAMMOTH_BEAT_VALUE
        return 0

    def update(self):
        self.life = min(1.0, self.life + self._world.constants.MAMMOTH_REGENERATION_VALUE)


class Animal(object):
    def __init__(self, world, dna=""):
        self.world = world
        self._dna = dna
        self._x = randint(0, self.world.width)
        self._y = randint(0, self.world.height)
        self.size = self.world.constants.ANIMAL_SIZE
        self.angle = 0
        self.closest_food = None

        self.sensor_values = []
        self._sensors_positions = []
        self._sensors_positions_calculated = False

        self.energy = self.world.constants.ENERGY_FOR_BIRTH
        self.readiness_to_sex = 0
        self.close_partners = []
        self.answer = []

        if not self._dna:
            self._dna = create_random_dna(self.world.constants)

        self.brain = create_brain(self._dna, self.world.constants)
        
    @property
    def sensors_positions(self):
        if not self._sensors_positions_calculated:
            self._calculate_sensor_positions()
            self._sensors_positions_calculated = True
        return self._sensors_positions

    def _calculate_sensor_positions(self):
        self._sensors_positions = []
        angle_between_sensors = TWO_PI / self.world.constants.ANIMAL_SENSOR_COUNT
        sensor_angle = self.angle
        for i in range(self.world.constants.ANIMAL_SENSOR_COUNT):
            x = math.cos(sensor_angle) * self.size + self._x
            y = math.sin(sensor_angle) * self.size + self._y
            self._sensors_positions.append((x, y))
            sensor_angle += angle_between_sensors

    def update(self):
        if self.closest_food:
            self.eat(self.closest_food)

        self.answer = self.brain.calculate(self.sensor_values)

        self.energy -= self.world.constants.ENERGY_FOR_EXIST

        if self.energy_fullness > self.world.constants.ENERGY_FULLNESS_TO_INCREASE_READINESS_TO_SEX:
            self.readiness_to_sex += self.world.constants.READINESS_TO_SEX_INCREMENT

        if self.is_ready_to_sex():
            self._search_partner_and_try_to_sex()

        self.move(self.answer[0], self.answer[1])

    def is_ready_to_sex(self):
        return self.readiness_to_sex >= self.world.constants.READINESS_TO_SEX_THRESHOLD

    def _search_partner_and_try_to_sex(self):
        for partner in self.close_partners:
            success = partner.be_requested_for_sex(self)
            if success:
                break

    def be_requested_for_sex(self, partner):
        if self.is_ready_to_sex():
            self.sex(partner)
            return True
        return False

    def sex(mother, father):
        child_count = randint(
            mother.world.constants.MIN_AMOUNT_OF_CHILDREN,
            mother.world.constants.MAX_AMOUNT_OF_CHILDREN
        )
        # if it tries to birth more child than it can - bud so many as it can and die.
        if not mother.can_make_n_children(child_count):
            child_count = int(mother.energy / mother.world.constants.ENERGY_FOR_BIRTH)
            mother.energy = 0
        if not father.can_make_n_children(child_count):
            child_count = int(father.energy / mother.world.constants.ENERGY_FOR_BIRTH)
            father.energy = 0

        for _ in range(child_count):
            mother.make_child(father)

        mother.readiness_to_sex = 0
        father.readiness_to_sex = 0

    def can_make_n_children(self, child_count):
        return child_count * self.world.constants.ENERGY_FOR_BIRTH <= self.energy

    def make_child(mother, father):
        mother.energy -= mother.world.constants.ENERGY_FOR_BIRTH
        father.energy -= mother.world.constants.ENERGY_FOR_BIRTH
        child = Animal(mother.world, mix_dna(mother.dna, father.dna, mother.world.constants))
        child.x = mother.x + randint(-30, 30)
        child.y = mother.y + randint(-30, 30)
        mother.world.add_animal(child)

    def eat(self, food):
        value = min(
            self.world.constants.EATING_VALUE,
            max(0, self.world.constants.ANIMAL_MAX_ENERGY - self.energy) / self.world.constants.FOOD_SIZE_TO_ENERGY_RATIO
        )
        energy = food.beating(value)
        self.energy += energy

    def move(self, move, rotate):
        self.energy -= (abs(move) + abs(rotate)) * self.world.constants.MOVE_DISTANCE_TO_CONSUMED_ENERGY_RATIO

        self._sensors_positions_calculated = False
        self.angle += rotate
        self._x += math.cos(self.angle) * move * 2.0
        self._y += math.sin(self.angle) * move * 2.0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._sensors_positions_calculated = False

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._sensors_positions_calculated = False

    @property
    def energy_fullness(self):
        return self.energy / self.world.constants.ANIMAL_MAX_ENERGY

    @property
    def dna(self):
        return self._dna


def create_random_dna(constants):
    return "".join([str(randint(0, constants.DNA_BASE - 1)) for _ in range(constants.DNA_LEN)])


def mutate_dna(dna, constants):
    dna_ba = bytearray(dna, 'utf8')
    for i in range(len(dna_ba)):
        if random() < constants.MUTATE_CHANCE:
            dna_ba[i] = ord(str(randint(0, constants.DNA_BASE - 1)))
    return dna_ba.decode('utf8')


def mix_dna(dna1, dna2, constants):
    m = randint(0, len(dna1))
    if randint(0, 1):
        return mutate_dna(dna1[:m] + dna2[m:], constants)
    else:
        return mutate_dna(dna2[:m] + dna1[m:], constants)
