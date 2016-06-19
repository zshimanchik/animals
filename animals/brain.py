import numpy as np


class Brain:
    def __init__(self, shape, values_iter=None):
        self.shape = shape
        self.layers = []
        for i in range(1, len(shape)):
            self.layers.append(Layer(shape[i-1]+1, shape[i], values_iter))

    def calculate(self, x):
        assert len(x) == self.shape[0]
        for layer in self.layers:
            x = list(x) + [1.0]
            x = layer.calculate(x)
        return x

    def __len__(self):
        return len(self.shape)

    def __getitem__(self, item):
        if item == len(self.shape) - 1:
            return self.layers[-1].output
        else:
            return self.layers[item].input


class Layer:
    def __init__(self, input_size, output_size, values_iter=None):
        self.input = np.zeros(shape=[input_size])
        self.output = np.zeros(shape=[output_size])
        self.matrix = np.random.uniform(-0.3, 0.3, size=(input_size, output_size))
        if values_iter:
            for row in self.matrix:
                for i in range(len(row)):
                    row[i] = values_iter.__next__()

    def calculate(self, x):
        self.input = x
        self.output = np.tanh(np.dot(x, self.matrix))
        return self.output


def create_brain(dna, constants):
    def dna_iter(_dna):
        for i in range(0, len(_dna), constants.DNA_BRAIN_VALUE_LEN):
            cur = _dna[i:i + constants.DNA_BRAIN_VALUE_LEN]
            yield (int(cur, constants.DNA_BASE) - constants.DNA_HALF_MAX_VALUE) / constants.DNA_HALF_MAX_VALUE

    dna_values_iter = dna_iter(dna)
    brain = Brain(constants.NEURAL_NETWORK_SHAPE, dna_values_iter)
    return brain


# for debug
def brain_to_dna(brain, constants):
    def val_to_dna(x):
        x = max(0, int((x * constants.DNA_HALF_MAX_VALUE) + constants.DNA_HALF_MAX_VALUE))
        res = []
        while x:
            res.insert(0, str(x % constants.DNA_BASE))
            x /= constants.DNA_BASE
        return "".join(res)

    dna = []
    for layer in brain:
        for neuron in layer:
            for w in neuron.w:
                dna.append(val_to_dna(w))
    return "".join(dna)

