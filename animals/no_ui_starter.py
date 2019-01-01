import datetime
import json
import logging
import multiprocessing as mp
import os
import resource
import sys
import time
from collections import namedtuple

from analyzers import MammothAnalyzer
from engine import serializer
from engine.world import World
from engine.world_constants import WorldConstants

# I know... Don't look at this file

WorkerArgs = namedtuple('WorkerArgs', ['world_constants', 'world_save', 'world_name', 'snapshot_dir'])


class NoUiStarter:

    def __init__(self, process_count, save_world_each, max_cycle, path_for_snapshots):
        """
        :param process_count:
        :param save_world_each:
        :param max_cycle: 0 for endless emulation
        :param path_for_snapshots:
        """
        self.process_count = process_count
        self.save_world_each = save_world_each
        self.max_cycle = max_cycle
        self.path_for_snapshots = path_for_snapshots
        self.git_commit = os.popen('git rev-parse --short HEAD').read().strip() or 'nocommit'
        self.world_constant_list = []

    def start(self):
        logging.info(f"{self.process_count} processes")
        logging.info("START")
        pool = mp.Pool(processes=self.process_count)
        pool.map(self.worker, self.world_constant_list)
        logging.info("DONE")

    def worker(self, args: WorkerArgs):
        logging.info("{} started".format(args.world_name))
        start_time = time.perf_counter()
        if args.world_constants:
            world = World(args.world_constants)
        else:
            world = serializer.load(args.world_save)
        analyzer = MammothAnalyzer(world)
        while True:
            if world.time % self.save_world_each == 0:
                elapsed = time.perf_counter() - start_time
                performance = (time.perf_counter()-start_time) / self.save_world_each
                logging.info(f'{args.world_name}: '
                      f'{world.time} ticks calculated. '
                      f'{elapsed:.3f}s elapsed. '
                      f'{performance:.7f} performance')
                self._save_world(world, args.snapshot_dir)

            world.update()
            analyzer.update()
            if analyzer.amount_of_killings > 0.01:
                logging.info(f'World {args.world_name} got reaction at {world.time}')
                break

            if self.max_cycle and world.time >= self.max_cycle:
                break

        performance = (time.perf_counter() - start_time) / self.max_cycle

        self._save_world(world, args.snapshot_dir)
        logging.info("{} ended with average performance={}".format(args.world_name, performance))

    def add_new_world(self, world_constants, world_name):
        snapshot_dir = self._prepare_snapshot_dir(world_name, world_constants)
        self.world_constant_list.append(WorkerArgs(world_constants, None, world_name, snapshot_dir))

    def add_saved_world(self, world_save, world_name):
        snapshot_dir = self._prepare_snapshot_dir(world_name)
        self.world_constant_list.append(WorkerArgs(None, world_save, world_name, snapshot_dir))

    def _prepare_snapshot_dir(self, world_name, world_constants=None):
        now = datetime.datetime.now().strftime("%FT%T")
        subdir_name = f'{now}--{self.git_commit}--{world_name}'
        snapshot_dir = os.path.join(self.path_for_snapshots, subdir_name)
        os.makedirs(snapshot_dir, exist_ok=True)
        if world_constants is not None:
            with open(os.path.join(snapshot_dir, 'world_params.json'), 'w') as f:
                json.dump(world_constants.to_dict(), f, indent=2)
        return snapshot_dir

    def _save_world(self, world, snapshot_dir):
        filename = os.path.join(snapshot_dir, f'{world.time}.wrld')
        logging.info(f'saving {filename}')
        serializer.save(world, filename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format= '[%(asctime)s]: %(message)s')

    # Increasing size of stack to be able to pickle
    logging.info(resource.getrlimit(resource.RLIMIT_STACK))
    logging.info(sys.getrecursionlimit())

    max_rec = 0x100000

    # May segfault without this line. 0x100 is a guess at the size of each stack frame.
    resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
    sys.setrecursionlimit(max_rec)

    starter = NoUiStarter(
        process_count=4,
        save_world_each=50_000,
        max_cycle=0,
        path_for_snapshots='./snapshots/'
    )

    for i in range(6):
        starter.add_new_world(WorldConstants(), f'world_n{i:02}')

    starter.start()
