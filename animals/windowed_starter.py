import resource
import sys

from PyQt5.QtWidgets import QApplication

from engine.world import World
from engine.world_constants import WorldConstants
from ui.main_window import MainWindow

if __name__ == "__main__":
    # Increasing size of stack to be able to pickle
    print(resource.getrlimit(resource.RLIMIT_STACK))
    print(sys.getrecursionlimit())

    max_rec = 0x100000

    # May segfault without this line. 0x100 is a guess at the size of each stack frame.
    # resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
    sys.setrecursionlimit(max_rec)

    world_constants = WorldConstants()
    save_genealogy = False
    world = World(constants=world_constants, save_genealogy=save_genealogy)

    app = QApplication(sys.argv)
    mySW = MainWindow(world)
    mySW.show()
    sys.exit(app.exec_())
