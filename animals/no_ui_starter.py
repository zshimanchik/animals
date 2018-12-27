import multiprocessing as mp
import os
import resource
import sys
import time

from engine import serializer
from engine.world import World
from engine.world_constants import WorldConstants

# I know... Don't look at this file


class NoUiStarter:

    PROCESS_COUNT = 4
    MAKE_DUMP_EACH = 20000
    MAX_CYCLE = 900000
    COMMON_WORLD_NAME = "mp"
    PATH_FOR_SNAPSHOTS = "../snapshots/"

    def __init__(self):
        self.git_commit = os.popen('git rev-parse --short HEAD').read().strip() or 'nocommit'

    def start(self):
        print("{} processes".format(self.PROCESS_COUNT))
        worlds = []

        w1 = WorldConstants()
        w1.FOOD_TIMER = 23
        worlds.append((w1, "{}_{}_23".format(self.COMMON_WORLD_NAME, 1), self.MAX_CYCLE))

        w2 = WorldConstants()
        w2.FOOD_TIMER = 33
        worlds.append((w2, "{}_{}_33".format(self.COMMON_WORLD_NAME, 2), self.MAX_CYCLE))

        w3 = WorldConstants()
        w3.FOOD_TIMER = 23
        worlds.append((w3, "{}_{}_23".format(self.COMMON_WORLD_NAME, 3), self.MAX_CYCLE))

        w4 = WorldConstants()
        w4.FOOD_TIMER = 33
        worlds.append((w4, "{}_{}_33".format(self.COMMON_WORLD_NAME, 4), self.MAX_CYCLE))

        w5 = WorldConstants()
        w5.FOOD_TIMER = 23
        worlds.append((w4, "{}_{}_23".format(self.COMMON_WORLD_NAME, 5), self.MAX_CYCLE))

        w6 = WorldConstants()
        w6.FOOD_TIMER = 33
        worlds.append((w4, "{}_{}_23".format(self.COMMON_WORLD_NAME, 6), self.MAX_CYCLE))

        print("START")
        pool = mp.Pool(processes=self.PROCESS_COUNT)
        pool.map(self.worker, worlds)
        print("DONE")

    def worker(self, args):
        constants, world_name, max_cycle = args
        print("{} started".format(world_name))
        start_time = time.clock()
        world = World(constants)
        for _ in range(max_cycle):
            if world.time % self.MAKE_DUMP_EACH == 0:
                self.make_dump(world, world_name)
            world.update()

        performance = (time.clock() - start_time) / max_cycle

        self.make_dump(world, world_name)
        print("{} ended with average performance={}".format(world_name, performance))

    def make_dump(self, world, world_name):
        subdir_name = f'{self.git_commit}_{world_name}'
        subdir = os.path.join(self.PATH_FOR_SNAPSHOTS, subdir_name)
        os.makedirs(subdir, exist_ok=True)
        filename = os.path.join(subdir, f'{world.time}.wrld')
        print(f'saving {filename}')
        serializer.save(world, filename)


if __name__ == '__main__':
    # Increasing size of stack to be able to pickle
    print(resource.getrlimit(resource.RLIMIT_STACK))
    print(sys.getrecursionlimit())

    max_rec = 0x100000

    # May segfault without this line. 0x100 is a guess at the size of each stack frame.
    resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
    sys.setrecursionlimit(max_rec)

    NoUiStarter().start()
