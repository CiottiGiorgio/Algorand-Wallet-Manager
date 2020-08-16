"""
This main function will initialize PySide2 & Main and manage the starting of the program.
"""


# PySide2
from PySide2 import QtWidgets


# TODO Maybe look into Qt model/view because management of contacts, wallets and addresses is getting out of hand
#  especially in TransactionWindow
# TODO deploying on linux is a NIGHTMARE. Find a way to freeze the app for Windows/MacOS/Linux.
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
    main_window.show()

    # Enter main loop.
    return app.exec_()


if __name__ == '__main__':
    main()
