from collections import deque
from statistics import mean, StatisticsError


class BaseAnalyzer:
    def __init__(self, world):
        pass

    def reset(self, world):
        pass

    def analyze_after_animals_update(self, world):
        pass

    def analyze_in_the_end(self, world):
        pass


class MammothAnalyzer(BaseAnalyzer):
    def __init__(self, world, analysis_interval=2000):
        super().__init__(world)
        self.analysis_interval = analysis_interval
        self.killing_history = deque([0] * self.analysis_interval, maxlen=self.analysis_interval)
        self.killing_history_sum = 0
        self._prev_mammoth_amount = len(world.mammoths)

    def analyze_in_the_end(self, world):
        killed_mammoths_amount = max(0, self._prev_mammoth_amount - len(world.mammoths))
        self._prev_mammoth_amount = len(world.mammoths)
        self.killing_history_sum += -self.killing_history[0] + killed_mammoths_amount
        self.killing_history.append(killed_mammoths_amount)

    @property
    def amount_of_killings(self):
        """Amount of killings per 1 tick"""
        return self.killing_history_sum / self.analysis_interval


class AnimalAmountAnalyzer(BaseAnalyzer):
    def __init__(self, world, analysis_interval=2000):
        super().__init__(world)
        self.analysis_interval = analysis_interval
        self.animal_amount_history = deque([len(world.animals)] * self.analysis_interval, maxlen=self.analysis_interval)
        self.animal_amount_history_sum = len(world.animals) * self.analysis_interval

    def analyze_in_the_end(self, world):
        self.animal_amount_history_sum += -self.animal_amount_history[0] + len(world.animals)
        self.animal_amount_history.append(len(world.animals))

    @property
    def average(self):
        """Average amount of animals for the last analysis interval"""
        return self.animal_amount_history_sum / self.analysis_interval


class AnimalLifetimeAnalyzer(BaseAnalyzer):
    def __init__(self, world, analysis_interval=2000):
        super().__init__(world)
        self.analysis_interval = analysis_interval
        self.animals_lifetimes_history = deque(maxlen=analysis_interval)

    def analyze_after_animals_update(self, world):
        new_deaths = []
        for animal in world.animals:
            if animal.energy <= 0:
                new_deaths.append(world.time - animal.birth_time)

        self.animals_lifetimes_history.append(new_deaths)

    @property
    def average(self):
        try:
            return mean(x for tick in self.animals_lifetimes_history for x in tick) if self.animals_lifetimes_history else 0
        except StatisticsError:
            return 0


class NewAnimalEnergyAnalyzer(BaseAnalyzer):
    def __init__(self, world, analysis_interval=2000):
        super().__init__(world)
        self.analysis_interval = analysis_interval
        self.new_animal_energy_history = deque(maxlen=analysis_interval)

    def analyze_after_animals_update(self, world):

        new_births = []
        for animal in world.animals_to_add:
            new_births.append(animal.energy)

        self.new_animal_energy_history.append(new_births)

    @property
    def average(self):
        try:
            return mean(x for tick in self.new_animal_energy_history for x in tick) if self.new_animal_energy_history else 0
        except StatisticsError:
            return 0
