import resource
import sys

from PyQt5.QtWidgets import QApplication

from engine.world import World
from engine.world_constants import WorldConstants
from ui.main_window import MainWindow
import time

from engine import serializer
from engine.world import World
from engine.world_constants import WorldConstants

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def distance(a1, a2):
    return sum(c1 != c2 for c1, c2 in zip(a1.dna, a2.dna))


def build_matrix(world):
    matrix = []
    for a1 in world.animals:
        row = []
        matrix.append(row)
        for a2 in world.animals:
            row.append(distance(a1, a2))
    return matrix


if __name__ == "__main__":
    # world = World(WorldConstants())

    start = time.time()
    # world = serializer.load('snapshots/world_201202_f0041e5_MSTER2.5_03/0.wrld')
    # world = serializer.load('snapshots/world_201202_f0041e5_MSTER2.5_03/50000.wrld')
    # world = serializer.load('snapshots/world_201202_f0041e5_MSTER2.5_03/2850000.wrld')
    world = serializer.load('/Users/neuron/projects/animals/animals/snapshots/world_201202_f0041e5_MSTER2.5_03/20000000.wrld')

    matrix = build_matrix(world)

    matrix = np.array(matrix)
    print(matrix.shape)
    print(matrix)
    pca = PCA(n_components=2)
    pc_matrix = pca.fit_transform(matrix)
    print(pc_matrix.shape)
    print(pc_matrix)


    x = pc_matrix[:, 0]
    y = pc_matrix[:, 1]
    x = (x - np.min(x)) / (np.max(x) - np.min(x))
    y = (y - np.min(y)) / (np.max(y) - np.min(y))

    # plt.plot(pc_matrix[:, 0], pc_matrix[:, 1], 'o')
    plt.plot(x, y, 'o')
    plt.show()

    animal_colors = {}
    for animal, x_p, y_p in zip(world.animals, x, y):
        animal_colors[animal] = (x_p, y_p)

    app = QApplication(sys.argv)
    mySW = MainWindow(world)
    mySW.animal_colors = animal_colors
    mySW.show()
    sys.exit(app.exec_())
