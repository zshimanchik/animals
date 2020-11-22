import time

from engine import serializer
from engine.world import World
from engine.world_constants import WorldConstants


if __name__ == '__main__':
    # world = World(WorldConstants())

    start = time.time()
    world = serializer.load('snapshots/world_201121_07d07e8_01/4400000.wrld')
    # world = serializer.load('snapshots/world_201121_07d07e8_02/4400000.wrld')
    print(f'load: {time.time() - start}s')

    print(f'world time: {world.time}')
    start = time.time()
    for _ in range(10_000):
        world.update()
    print(f'world time: {world.time}')
    print(f'calc: {time.time() - start}s')

    start = time.time()
    serializer.save(world, 'snapshots/xz2.wrld')
    print(f'save: {time.time() - start}s')
