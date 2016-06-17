from cached_property import cached_property


class WorldConstants(object):
    WORLD_WIDTH = 900
    WORLD_HEIGHT = 200

    INITIAL_ANIMAL_COUNT = 55
    INITIAL_FOOD_COUNT = 250

    EATING_DISTANCE = 20
    EATING_VALUE = 0.02
    FOOD_SMELL_SIZE_RATIO = 21.0

    FOOD_TIMER = 1000 * (100 * 100) // (WORLD_WIDTH * WORLD_HEIGHT)

    APPEAR_FOOD_COUNT = 3
    APPEAR_FOOD_SIZE_MIN = 4
    APPEAR_FOOD_SIZE_MAX = 7
    FOOD_SIZE_TO_ENERGY_RATIO = 1.5

    MAMMOTH_COUNT = 5
    MAMMOTH_MIN_DISTANCE_TO_OTHERS = 80
    MAMMOTH_SMELL_SIZE_RATIO = 5.0
    MAMMOTH_BEAT_VALUE = 0.007
    MAMMOTH_REGENERATION_VALUE = 0.01
    FOOD_FROM_MAMMOTH_COUNT = 5

    # Animal

    ANIMAL_MAX_ENERGY = 30
    ENERGY_FOR_EXIST = 0.007
    MOVE_DISTANCE_TO_CONSUMED_ENERGY_RATIO = 0.01

    # neural_network shape
    ANIMAL_SENSOR_COUNT = 7
    ANIMAL_SENSOR_DIMENSION = 1  # how many values in one sensor

    MIDDLE_LAYERS_SIZES = [2]
    OUTPUT_LAYER_SIZE = 2

    # DNA
    DNA_BASE = 4  # must be less or equals than 10, but greater than 1
    DNA_BRAIN_VALUE_LEN = 5

    READINESS_TO_SEX_THRESHOLD = 30
    READINESS_TO_SEX_INCREMENT = 0.2
    ENERGY_FULLNESS_TO_INCREASE_READINESS_TO_SEX = 0.7
    ENERGY_FOR_BIRTH = 5
    MIN_AMOUNT_OF_CHILDREN = 1
    MAX_AMOUNT_OF_CHILDREN = 3

    MUTATE_CHANCE = 0.05

    ANIMAL_SIZE = 10
    MAX_ANIMAL_SMELL_SIZE = 100

    SEX_DISTANCE = 20 + ANIMAL_SIZE * 2

    def __init__(self):
        pass

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
