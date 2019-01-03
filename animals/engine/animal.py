import math
from random import random, randint

from engine.brain import create_brain

TWO_PI = math.pi * 2


class WorldObject:
    x = 0
    y = 0
    size = 1

    def update(self):
        pass


class Food(WorldObject):
    def __init__(self, world, x, y, size):
        self._world = world
        self.x = x
        self.y = y
        self._size = size
        self._smell = (0.0, 1.0,)
        self._smell_size = self._size * self._world.constants.FOOD_SMELL_SIZE_RATIO
        self.bitten = False

    def update(self):
        self.bitten = False

    def to_be_bitten(self, value):
        self.bitten = True
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


class Mammoth(WorldObject):
    def __init__(self, world, x, y, size):
        self._world = world
        self.x = x
        self.y = y
        self.size = size
        self.smell = (1.0, 0.0,)
        self.smell_size = self.size * self._world.constants.MAMMOTH_SMELL_SIZE_RATIO
        self.life = 1

    def to_be_bitten(self, value):
        self.life -= self._world.constants.MAMMOTH_BEAT_VALUE
        return 0

    def update(self):
        self.life = min(1.0, self.life + self._world.constants.MAMMOTH_REGENERATION_VALUE)


class Animal(WorldObject):
    def __init__(self, world, energy, dna="", parents=None, save_genealogy=False):
        self.world = world
        self._dna = dna
        self.parents = parents or []
        self.save_genealogy = save_genealogy
        self.birth_time = self.world.time
        self.children = []
        self._x = randint(0, self.world.width)
        self._y = randint(0, self.world.height)
        self.size = self.world.constants.ANIMAL_SIZE
        self.angle = 0
        self.closest_food = None

        self.sensor_values = []
        self._sensors_positions = []
        self._sensors_positions_calculated = False

        self.energy = energy
        self.close_partners = []
        self.answer = []

        if not self._dna:
            self._dna = create_random_dna(self.world.constants)

        self.brain = create_brain(self._dna, self.world.constants)
        self._extract_energy_for_birth_from_dna(self._dna)

    def _extract_energy_for_birth_from_dna(self, dna):
        energy_for_birth_raw_int = int(self._dna[-4:], base=self.world.constants.DNA_BASE)
        # scale to [0;1]
        energy_for_birth_raw_normalized = energy_for_birth_raw_int / (4 ** self.world.constants.DNA_BASE)
        self.energy_for_birth = self.world.constants.ENERGY_FOR_BIRTH_DIFF * energy_for_birth_raw_normalized \
                                + self.world.constants.ENERGY_FOR_BIRTH_MIN

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

        if self.is_ready_to_sex():
            self._search_partner_and_try_to_sex()

        # self.smell_size = (max(-1, self.answer[2]) + 1) / 2.0 * self.world.constants.MAX_ANIMAL_SMELL_SIZE
        self.move(self.answer[0], self.answer[1])

    def is_ready_to_sex(self):
        return self.energy_fullness >= self.world.constants.ENERGY_THRESHOLD_FOR_SEX

    def _search_partner_and_try_to_sex(self):
        for partner in self.close_partners:
            success = partner.be_requested_for_sex(self)
            if success:
                break

    def be_requested_for_sex(self, partner):
        if self.is_ready_to_sex():
            Animal.sex(self, partner)
            return True
        return False

    @staticmethod
    def sex(mother, father):
        child_count = randint(
            mother.world.constants.MIN_AMOUNT_OF_CHILDREN,
            mother.world.constants.MAX_AMOUNT_OF_CHILDREN
        )
        # if it tries to birth more child than it can - bud so many as it can and die.
        if not mother.can_make_n_children(child_count):
            child_count = int(mother.energy / mother.energy_for_birth)
            mother.energy = 0
        if not father.can_make_n_children(child_count):
            child_count = int(father.energy / father.energy_for_birth)
            father.energy = 0

        for _ in range(child_count):
            Animal.make_child(mother, father)

    def can_make_n_children(self, child_count):
        return child_count * self.energy_for_birth <= self.energy

    @staticmethod
    def make_child(mother, father):
        mother.energy -= mother.energy_for_birth
        father.energy -= mother.energy_for_birth
        child = Animal(
            mother.world,
            mother.energy_for_birth + father.energy_for_birth,
            mix_dna(mother.dna, father.dna, mother.world.constants),
            parents=[mother, father] if mother.save_genealogy else None,
            save_genealogy=mother.save_genealogy,
        )
        child.x = mother.x + randint(-30, 30)
        child.y = mother.y + randint(-30, 30)
        mother.world.add_animal(child)
        if mother.save_genealogy:
            mother.children.append(child)
            father.children.append(child)

    def eat(self, food):
        value = min(
            self.world.constants.EATING_VALUE,
            max(0, self.world.constants.ANIMAL_MAX_ENERGY - self.energy) / self.world.constants.FOOD_SIZE_TO_ENERGY_RATIO
        )
        energy = food.to_be_bitten(value)
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

    # @property
    # def smell(self):
    #     return self._smell

    @property
    def energy_fullness(self):
        return self.energy / self.world.constants.ANIMAL_MAX_ENERGY

    @property
    def dna(self):
        return self._dna


def create_random_dna(constants):
    result = "".join(str(randint(0, constants.DNA_BASE - 1)) for _ in range(constants.DNA_LEN))
    result = result[:-4] + '1333'  # just for everybody starts with the same energy_for_birth
    return result


def mutate_dna(dna, constants):
    return ''.join(str(randint(0, constants.DNA_BASE - 1)) if random() < constants.MUTATE_CHANCE else c for c in dna)


def mix_dna(dna1, dna2, constants):
    m = randint(0, len(dna1))
    if randint(0, 1):
        return mutate_dna(dna1[:m] + dna2[m:], constants)
    else:
        return mutate_dna(dna2[:m] + dna1[m:], constants)
