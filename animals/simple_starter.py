import time

from engine import serializer
from engine.world import World
from engine.world_constants import WorldConstants


if __name__ == '__main__':
    # world = World(WorldConstants())

    start = time.time()
    world = serializer.load('snapshots/world_201202_cf95206_MSTER3_MMAN_15_MC3_02/50000.wrld')
    # world = serializer.load('snapshots/world_201121_07d07e8_02/4400000.wrld')
    print(f'load: {time.time() - start}s')

    print(f'world time: {world.time}')
    TICKS = 10_000
    start = time.time()
    for _ in range(TICKS):
        world.update()
    print(f'world time: {world.time}')
    calc_time = time.time() - start
    print(f'calc: {calc_time}s')
    print(f'performance: {calc_time/TICKS}')

    start = time.time()
    serializer.save(world, 'snapshots/xz2.wrld')
    print(f'save: {time.time() - start}s')
