"""
This main function will initialize PySide2 & Main and manage the starting of the program
"""


# PySide2
from PySide2 import QtWidgets

# Local project
from misc import Constants as ProjectConstants


def main():
    # Manager of all things regarding a widget-based Qt5 app.
    #  Eg.: mainloop, events, initialization, finalization, ...
    app = QtWidgets.QApplication([])

    # This import has to be done here because there are several static resources inside this package which
    #  will be loaded during the import of the package itself. So because most misc are PySide2 objects
    #  QApplication needs to be running to perform all task needed.
    from Interfaces.Main.Window import MainWindow

    MainWindow.initialize()

    main_window = MainWindow()
    # We write a reference to main_window inside Constants.py file.
    ProjectConstants.main_window = main_window
    main_window.show()

    # Enter main loop.
    return app.exec_()


if __name__ == '__main__':
    main()
