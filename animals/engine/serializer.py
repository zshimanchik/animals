"""
Ensure that you have increased recursion limits

    # Increasing size of stack to be able to pickle
    print(resource.getrlimit(resource.RLIMIT_STACK))
    print(sys.getrecursionlimit())

    max_rec = 0x100000

    # May segfault without this line. 0x100 is a guess at the size of each stack frame.
    resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
    sys.setrecursionlimit(max_rec)
"""

import random
import numpy as np
import pickle


def save(world, path):
    """
    Saves world and states of random generators: random and numpy.random
    """
    data = {
        'world': world,
        'random.state': random.getstate(),
        'np.random.state': np.random.get_state()
    }
    try:
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    except RecursionError as ex:
        print('RecursionError. Make sure that you increased recursion limit.')
        raise ex


def load(path):
    """
    Loads world from dump and set state to random generators: random and numpy.random
    """
    with open(path, 'rb') as f:
        data = pickle.load(f)

    random.setstate(data['random.state'])
    np.random.set_state(data['np.random.state'])
    return data['world']
