from collections import deque


class MammothAnalyzer:
    def __init__(self, world, analysis_interval=2000):
        self.world = world
        self.analysis_interval = analysis_interval
        self.killing_history = deque([0] * self.analysis_interval, maxlen=self.analysis_interval)
        self.killing_history_sum = 0
        self._prev_mammoth_amount = len(self.world.mammoths)

    def update(self):
        killed_mammoths_amount = max(0, self._prev_mammoth_amount - len(self.world.mammoths))
        self._prev_mammoth_amount = len(self.world.mammoths)
        self.killing_history_sum += -self.killing_history[0] + killed_mammoths_amount
        self.killing_history.append(killed_mammoths_amount)

    @property
    def amount_of_killings(self):
        """Amount of killings per 1 tick"""
        return self.killing_history_sum / self.analysis_interval
