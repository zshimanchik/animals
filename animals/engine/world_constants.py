from cached_property import cached_property


class WorldConstants(object):
    def __init__(self):
        self.WORLD_WIDTH = 900
        self.WORLD_HEIGHT = 200

        self.INITIAL_ANIMAL_COUNT = 55
        self.INITIAL_FOOD_COUNT = 250

        self.EATING_DISTANCE = 20
        self.EATING_VALUE = 0.02
        self.FOOD_SMELL_SIZE_RATIO = 21.0

        self.FOOD_TIMER = 1000 * (100 * 100) // (self.WORLD_WIDTH * self.WORLD_HEIGHT)

        self.APPEAR_FOOD_COUNT = 3
        self.APPEAR_FOOD_SIZE_MIN = 4
        self.APPEAR_FOOD_SIZE_MAX = 7
        self.FOOD_SIZE_TO_ENERGY_RATIO = 1.5

        self.MAMMOTH_COUNT = 5
        self.MAMMOTH_MIN_DISTANCE_TO_OTHERS = 80
        self.MAMMOTH_SMELL_SIZE_RATIO = 14.0
        self.MAMMOTH_BEAT_VALUE = 0.007
        self.MAMMOTH_REGENERATION_VALUE = 0.01
        self.FOOD_FROM_MAMMOTH_COUNT = 5

        # Animal

        self.ANIMAL_MAX_ENERGY = 30
        self.ENERGY_FOR_EXIST = 0.007
        self.MOVE_DISTANCE_TO_CONSUMED_ENERGY_RATIO = 0.01

        # neural_network shape
        self.ANIMAL_SENSOR_COUNT = 3
        self.ANIMAL_SENSOR_DIMENSION = 2  # how many values in one sensor

        self.MIDDLE_LAYERS_SIZES = [2]
        self.OUTPUT_LAYER_SIZE = 2

        # DNA
        self.DNA_BASE = 4  # must be less or equals than 10, but greater than 1
        self.DNA_BRAIN_VALUE_LEN = 5

        self.READINESS_TO_SEX_THRESHOLD = 30
        self.READINESS_TO_SEX_INCREMENT = 0.2
        self.ENERGY_FULLNESS_TO_INCREASE_READINESS_TO_SEX = 0.7
        self.ENERGY_FOR_BIRTH = 5
        self.MIN_AMOUNT_OF_CHILDREN = 1
        self.MAX_AMOUNT_OF_CHILDREN = 3

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
        return self.DNA_FOR_BRAIN_LEN