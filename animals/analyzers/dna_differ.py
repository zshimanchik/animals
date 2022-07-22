from analyzers import BaseAnalyzer
import numpy as np
from sklearn.decomposition import PCA


class DnaDiffer(BaseAnalyzer):
    def __init__(self, world):
        super().__init__(world)
        self.world = world
        self.colors = {}
        self.needs_update = True

    def reset(self, world):
        pass

    def analyze_after_animals_update(self, world):
        if len(world.animals_to_add) or any(animal.energy <= 0 for animal in world.animals):
            self.needs_update = True
            print('need_update triggered')

    def analyze_in_the_end(self, world):
        if self.needs_update:
            self.clusterize()
            self.needs_update = False

    def clusterize(self):
        vectors = np.array(self.build_vectors())
        # print(vectors.shape)
        # print(vectors)
        pca = PCA(n_components=3)
        pc_vectors = pca.fit_transform(vectors)
        # print(pc_vectors.shape)
        # print(pc_vectors)
        self.scale(pc_vectors)

        self.colors = dict(zip(self.world.animals, pc_vectors))
        # print(self.colors)


    def build_vectors(self):
        vectors = []
        for a in self.world.animals:
            vectors.append([int(c) for c in a.dna])
        return vectors

    def scale(self, arr):
        x = arr[:, 0]
        y = arr[:, 1]
        z = arr[:, 2]
        x = (x - np.min(x)) / (np.max(x) - np.min(x))
        y = (y - np.min(y)) / (np.max(y) - np.min(y))
        z = (z - np.min(z)) / (np.max(z) - np.min(z))
        arr[:, 0] = x
        arr[:, 1] = y
        arr[:, 2] = z
