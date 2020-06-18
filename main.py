from PySide2 import QtWidgets

# TODO write docstring for class and methods


def main():
    app = QtWidgets.QApplication([])

    # This import has to be done here because inside MainWindow there's an import to CustomListWidgetItem
    #  and inside that there is some static icon that can only be loaded if Q.Application has started
    from resources.MainWindow import MainWindow

    main_window = MainWindow()
    main_window.show()

    main_window.show_contacts()

    app.exec_()


if __name__ == '__main__':
    main()
