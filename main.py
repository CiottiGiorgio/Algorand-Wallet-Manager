"""
This main function will initialize PySide2 & MainWindow and manage the starting of the program
"""


# PySide2
from PySide2 import QtWidgets

# TODO write docstring for class and methods
# TODO create user data folder if it doesn't exists
# TODO learn about unit test and decide if we need those
# TODO check if the code that edit and create new contact makes sense


def main():
    # Manager of all things regarding a widget-based Qt5 app.
    #  Eg.: mainloop, events, initialization, finalization, ...
    app = QtWidgets.QApplication([])

    # This import has to be done here because there are several static resources inside this package which
    #  will be loaded during the import of the package itself. So because most resources are PySide2 objects
    #  QApplication needs to be running to perform all task needed.
    from resources.MainWindow import MainWindow

    MainWindow.initialize()

    main_window = MainWindow()
    main_window.show()

    main_window.show_contacts()

    app.exec_()


if __name__ == '__main__':
    main()
