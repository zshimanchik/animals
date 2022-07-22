import random
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

def build_vectors(world):
    vectors = []
    for a in world.animals:
        vectors.append([int(c) for c in a.dna])
    return vectors

def scale(arr):
    x = arr[:, 0]
    y = arr[:, 1]
    z = arr[:, 2]
    x = (x - np.min(x)) / (np.max(x) - np.min(x))
    y = (y - np.min(y)) / (np.max(y) - np.min(y))
    z = (z - np.min(z)) / (np.max(z) - np.min(z))
    arr[:, 0] = x
    arr[:, 1] = y
    arr[:, 2] = z

if __name__ == '__main__':
    # world = World(WorldConstants())

    start = time.time()
    # world = serializer.load('snapshots/world_201202_f0041e5_MSTER2.5_03/0.wrld')
    world = serializer.load('snapshots/world_201202_f0041e5_MSTER2.5_03/50000.wrld')
    # world = serializer.load('snapshots/world_201202_f0041e5_MSTER2.5_03/2850000.wrld')

    vectors = np.array(build_vectors(world))
    print(vectors.shape)
    print(vectors)

    pca = PCA(n_components=3)
    pc_vectors = pca.fit_transform(vectors)
    print(pc_vectors.shape)
    print(pc_vectors)

    matrix = build_matrix(world)

    matrix = np.array(matrix)
    print(matrix.shape)
    print(matrix)
    pca = PCA(n_components=3)
    pc_matrix = pca.fit_transform(matrix)
    print(pc_matrix.shape)
    print(pc_matrix)

    scale(pc_matrix)
    scale(pc_vectors)

    # fig, (ax, ax2) = plt.subplots(2)
    fig = plt.figure()
    ax = fig.add_subplot(211, projection='3d')
    ax2 = fig.add_subplot(212, projection='3d')

    colors = [(random.random(), random.random(), random.random()) for _ in range(pc_matrix.shape[0])]

    # ax.plot(x, y, 'o', color=colors)
    ax.scatter3D(pc_matrix[:, 0], pc_matrix[:, 1],pc_matrix[:, 2], color=colors)
    ax2.scatter3D(pc_vectors[:,0], pc_vectors[:,1], pc_vectors[:,2], color=colors)
    plt.show()


    # plt.plot(x, y, 'o')
    # plt.show()


