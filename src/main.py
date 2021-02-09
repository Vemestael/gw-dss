#!/usr/bin/env python

import sys

from PyQt5 import QtWidgets

from interface.interface import Interface


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = Interface()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
