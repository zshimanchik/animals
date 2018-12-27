import resource
import sys

from PySide2.QtWidgets import QApplication

from ui.main_window import MainWindow

if __name__ == "__main__":
    # Increasing size of stack to be able to pickle
    print(resource.getrlimit(resource.RLIMIT_STACK))
    print(sys.getrecursionlimit())

    max_rec = 0x100000

    # May segfault without this line. 0x100 is a guess at the size of each stack frame.
    resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
    sys.setrecursionlimit(max_rec)

    app = QApplication(sys.argv)
    mySW = MainWindow()
    mySW.show()
    sys.exit(app.exec_())
