import datetime
import json
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

WorkerArgs = namedtuple('WorkerArgs', ['world_constants', 'world_name', 'snapshot_dir'])


class NoUiStarter:

    def __init__(self, process_count, save_world_each, max_cycle, path_for_snapshots):
        self.process_count = process_count
        self.save_world_each = save_world_each
        self.max_cycle = max_cycle
        self.path_for_snapshots = path_for_snapshots
        self.git_commit = os.popen('git rev-parse --short HEAD').read().strip() or 'nocommit'
        self.world_constant_list = []

    def start(self):
        print(f"{self.process_count} processes")
        print("START")
        pool = mp.Pool(processes=self.process_count)
        pool.map(self.worker, self.world_constant_list)
        print("DONE")

    def worker(self, args: WorkerArgs):
        print("{} started".format(args.world_name))
        start_time = time.perf_counter()
        world = World(args.world_constants)
        analyzer = MammothAnalyzer(world)
        got_reaction = False
        for _ in range(self.max_cycle):
            if world.time % self.save_world_each == 0:
                elapsed = time.perf_counter() - start_time
                performance = (time.perf_counter()-start_time) / self.save_world_each
                print(f'{args.world_name}: '
                      f'{world.time} ticks calculated. '
                      f'{elapsed:.3f}s elapsed. '
                      f'{performance:.7f} performance')
                self._save_world(world, args.snapshot_dir)

            world.update()
            analyzer.update()
            if analyzer.amount_of_killings > 0.01 and not got_reaction:
                print(f'World {args.world_name} got reaction at {world.time}')
                got_reaction = True
                self._save_world(world, args.snapshot_dir)

        performance = (time.perf_counter() - start_time) / self.max_cycle

        self._save_world(world, args.snapshot_dir)
        print("{} ended with average performance={}".format(args.world_name, performance))

    def add_world(self, world_constants, world_name):
        snapshot_dir = self._prepare_snapshot_dir(world_constants, world_name)
        self.world_constant_list.append(WorkerArgs(world_constants, world_name, snapshot_dir))

    def _prepare_snapshot_dir(self, world_constants, world_name):
        now = datetime.datetime.now().strftime("%FT%T")
        subdir_name = f'{now}--{self.git_commit}--{world_name}'
        snapshot_dir = os.path.join(self.path_for_snapshots, subdir_name)
        os.makedirs(snapshot_dir, exist_ok=True)
        with open(os.path.join(snapshot_dir, 'world_params.json'), 'w') as f:
            json.dump(world_constants.to_dict(), f, indent=2)
        return snapshot_dir

    def _save_world(self, world, snapshot_dir):
        filename = os.path.join(snapshot_dir, f'{world.time}.wrld')
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

    starter = NoUiStarter(
        process_count=4,
        save_world_each=50_000,
        max_cycle=1_000_000,
        path_for_snapshots='./snapshots/'
    )

    for i in range(6):
        starter.add_world(WorldConstants(), f'world_n{i}')

    starter.start()
