import time
import os
import pickle
import multiprocessing as mp

from world import World
from world_constants import WorldConstants

PROCESS_COUNT = mp.cpu_count()
MAX_CYCLE = 1000
COMMON_WORLD_NAME = "mp"
PATH_FOR_SNAPSHOTS = "/mnt/progs/animals/snapshots/food_and_mammoths/mp/"


def main():
    print("{} processes".format(PROCESS_COUNT))
    worlds = []

    w1 = WorldConstants()
    w1.FOOD_TIMER = 20
    worlds.append(_make_params(w1))

    w2 = WorldConstants()
    w2.FOOD_TIMER = 30
    worlds.append(_make_params(w2))

    w3 = WorldConstants()
    w3.FOOD_TIMER = 45
    worlds.append(_make_params(w3))

    w4 = WorldConstants()
    w4.FOOD_TIMER = 60
    worlds.append(_make_params(w4))

    print("START")
    pool = mp.Pool(processes=3)
    pool.map(worker, worlds)

    print("DONE")


def _make_params(constants, id=[1]):
    res = (constants, "{}_{}".format(COMMON_WORLD_NAME, id[0]), MAX_CYCLE)
    id[0] += 1
    return res


def worker(args):
    constants, world_name, max_cycle = args
    print("{} started".format(world_name))
    start_time = time.clock()
    world = World(constants)
    for _ in range(max_cycle):
        world.update()

    performance = (time.clock() - start_time) / max_cycle

    print("saving {}".format(world_name))
    filename = os.path.join(PATH_FOR_SNAPSHOTS, "world_{}--{}.wrld".format(world_name, world.time))
    with open(filename, 'wb') as f:
        pickle.dump(world, f)

    print("{} ended with average performance={}".format(world_name, performance))


if __name__ == '__main__':
    main()