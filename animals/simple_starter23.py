import math
import time

from engine import serializer
from engine.world import World
from engine.world_constants import WorldConstants

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def distance(a1, a2):
    return math.sqrt((a1[0] - a2[0]) ** 2 + (a1[1] - a2[1]) ** 2)


def build_matrix(xs, ys):
    matrix = []
    for a1 in range(len(xs)):
        row = []
        matrix.append(row)
        for a2 in range(len(xs)):
            row.append(distance((xs[a1], ys[a1]), (xs[a2], ys[a2])))
    return matrix


if __name__ == '__main__':
    # world = World(WorldConstants())

    start = time.time()
    # world = serializer.load('snapshots/world_201202_f0041e5_MSTER2.5_03/0.wrld')
    # world = serializer.load('snapshots/world_201202_f0041e5_MSTER2.5_03/50000.wrld')
    # world = serializer.load('snapshots/world_201202_f0041e5_MSTER2.5_03/2850000.wrld')

    orig_x = np.arange(1, 11)
    orig_y = 2 * orig_x + np.random.randn(10) * 2
    orig_x2 = np.arange(21, 26)
    orig_y2 = orig_x2 - 20 + np.random.randn(5) * 1
    orig_x = np.concatenate((orig_x, orig_x2))
    orig_y = np.concatenate((orig_y, orig_y2))
    X = np.vstack((orig_x, orig_y))
    print(X)
    # plt.plot(orig_x, orig_y, 'o')
    # plt.show()

    matrix = build_matrix(orig_x, orig_y)
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

    # plt.plot(x, y, 'o')
    # plt.show()

    fig, (ax, ax2) = plt.subplots(2)

    ax.plot(orig_x, orig_y, 'o')
    ax2.plot(x, y, 'o')
    plt.show()


