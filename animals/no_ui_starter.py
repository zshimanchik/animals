import time
import os
import pickle
import multiprocessing as mp

from world import World
from world_constants import WorldConstants

PROCESS_COUNT = 4
MAKE_DUMP_EACH = 100000
MAX_CYCLE = 900000
COMMON_WORLD_NAME = "mp"
PATH_FOR_SNAPSHOTS = "/mnt/progs/animals/snapshots/food_and_mammoths/no_cycle/"


def main():
    print("{} processes".format(PROCESS_COUNT))
    worlds = []

    w1 = WorldConstants()
    w1.FOOD_TIMER = 23
    worlds.append((w1, "{}_{}_23".format(COMMON_WORLD_NAME, 1), MAX_CYCLE))

    w2 = WorldConstants()
    w2.FOOD_TIMER = 33
    worlds.append((w2, "{}_{}_33".format(COMMON_WORLD_NAME, 2), MAX_CYCLE))

    w3 = WorldConstants()
    w3.FOOD_TIMER = 23
    worlds.append((w3, "{}_{}_23".format(COMMON_WORLD_NAME, 3), MAX_CYCLE))

    w4 = WorldConstants()
    w4.FOOD_TIMER = 33
    worlds.append((w4, "{}_{}_33".format(COMMON_WORLD_NAME, 4), MAX_CYCLE))

    w5 = WorldConstants()
    w5.FOOD_TIMER = 23
    worlds.append((w4, "{}_{}_23".format(COMMON_WORLD_NAME, 5), MAX_CYCLE))

    w6 = WorldConstants()
    w6.FOOD_TIMER = 33
    worlds.append((w4, "{}_{}_23".format(COMMON_WORLD_NAME, 6), MAX_CYCLE))


    print("START")
    pool = mp.Pool(processes=PROCESS_COUNT)
    pool.map(worker, worlds)

    print("DONE")


def worker(args):
    constants, world_name, max_cycle = args
    print("{} started".format(world_name))
    start_time = time.clock()
    world = World(constants)
    for _ in range(max_cycle):
        if world.time % MAKE_DUMP_EACH == 0:
            make_dump(world, world_name)
        world.update()

    performance = (time.clock() - start_time) / max_cycle

    make_dump(world, world_name)
    print("{} ended with average performance={}".format(world_name, performance))


def make_dump(world, world_name):
    filename = "world_{}--{}.wrld".format(world_name, world.time)
    print("saving {}".format(filename))
    file_full_name = os.path.join(PATH_FOR_SNAPSHOTS, filename)
    with open(file_full_name, 'wb') as f:
        pickle.dump(world, f)


if __name__ == '__main__':
    main()