from functools import cached_property


class WorldConstants(object):
    def __init__(self):
        self.WORLD_WIDTH = 900
        self.WORLD_HEIGHT = 200

        self.INITIAL_ANIMAL_COUNT = 55
        self.INITIAL_FOOD_COUNT = 200

        self.EATING_DISTANCE = 20
        self.EATING_VALUE = 0.02
        self.FOOD_SMELL_SIZE_RATIO = 10.0

        self.FOOD_TIMER = 1000 * (100 * 100) // (self.WORLD_WIDTH * self.WORLD_HEIGHT)
        # Than more this value then more concentrated x_ratio will be
        # Set 0 for uniform distribution
        self.FOOD_GAUSS_DISTRIBUTION_SIGMA = 2.5

        self.APPEAR_FOOD_COUNT = 3
        self.APPEAR_FOOD_SIZE_MIN = 4
        self.APPEAR_FOOD_SIZE_MAX = 7
        self.FOOD_SIZE_TO_ENERGY_RATIO = 1.5

        self.MAMMOTH_COUNT = 5
        self.MAMMOTH_MIN_DISTANCE_TO_OTHERS = 80
        self.MAMMOTH_SMELL_SIZE_RATIO = 5.0
        self.MAMMOTH_MAX_ANIMAL_N = 20  # How many animals can bite to increase energy by one bite
        self.MAMMOTH_SIZE_TO_ENERGY_RATIO = 2  # how much maximum energy they can get if all MAMMOTH_MAX_ANIMAL_N bite
        self.MAMMOTH_BODY_DENSITY = 7  # It can handle this times more bites than food with the same sizes

        # Animal

        self.ANIMAL_CAN_CLONE = False
        self.ANIMAL_MAX_ENERGY = 30
        self.ANIMAL_WORLD_START_ENERGY = self.ANIMAL_MAX_ENERGY / 3

        self.ENERGY_FOR_EXIST = 0.007
        self.MOVE_DISTANCE_TO_CONSUMED_ENERGY_RATIO = 0.01

        self.ENERGY_FOR_SMELL_RATIO = 0.002  # multiplied on network output in range [0:1]

        # neural_network shape
        self.ANIMAL_SENSOR_COUNT = 3
        self.ANIMAL_SENSOR_DIMENSION = 3  # how many values in one sensor

        self.MIDDLE_LAYERS_SIZES = [6]
        self.OUTPUT_LAYER_SIZE = 3

        # DNA
        self.DNA_BASE = 4  # must be less or equals than 10, but greater than 1
        self.DNA_BRAIN_VALUE_LEN = 5

        self.ENERGY_THRESHOLD_FOR_SEX = 0.7
        self.ENERGY_THRESHOLD_FOR_CLONE = 0.97
        self.ENERGY_FOR_BIRTH_WASTE = 1
        self.ENERGY_FOR_BIRTH_MAX = 10
        self.ENERGY_FOR_BIRTH_MIN = 0

        self.MIN_AMOUNT_OF_CHILDREN = 1
        self.MAX_AMOUNT_OF_CHILDREN = 1

        self.MUTATE_CHANCE = 0.05

        self.ANIMAL_SIZE = 10
        self.MAX_ANIMAL_SMELL_SIZE = 100

        self.SEX_DISTANCE = 20 + self.ANIMAL_SIZE * 2

    @cached_property
    def INPUT_LAYER_SIZE(self):
        return self.ANIMAL_SENSOR_COUNT * self.ANIMAL_SENSOR_DIMENSION

    @cached_property
    def NEURAL_NETWORK_SHAPE(self):
        return [self.INPUT_LAYER_SIZE] + self.MIDDLE_LAYERS_SIZES + [self.OUTPUT_LAYER_SIZE]

    @cached_property
    def DNA_MAX_VALUE(self):
        return self.DNA_BASE ** self.DNA_BRAIN_VALUE_LEN

    @cached_property
    def DNA_HALF_MAX_VALUE(self):
        return int(self.DNA_MAX_VALUE / 2)

    @cached_property
    def DNA_FOR_BRAIN_LEN(self):
        shape = self.NEURAL_NETWORK_SHAPE
        connection_count = sum([ shape[i] * (shape[i+1] + 1) for i in range(len(shape)-1)])
        return connection_count * self.DNA_BRAIN_VALUE_LEN

    @cached_property
    def DNA_LEN(self):
        return self.DNA_FOR_BRAIN_LEN + 4 + 4

    @cached_property
    def ENERGY_FOR_BIRTH_DIFF(self):
        return self.ENERGY_FOR_BIRTH_MAX - self.ENERGY_FOR_BIRTH_MIN

    def to_dict(self, with_cached_properties=True):
        """
        with_cached_properties - will work only if you didn't invoke them, otherwise they will be in instance dict
        """
        if with_cached_properties:
            result = {}
            for attr in dir(self):
                if not attr.startswith('_'):
                    value = getattr(self, attr)
                    if not callable(value):
                        result[attr] = value
            return result
        else:
            return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data):
        self = WorldConstants()
        self.__dict__.update(data)
        return self
