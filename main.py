from PyQt5 import QtWidgets


def main():
    app = QtWidgets.QApplication([])

    # This import has to be done here because inside MainWindow there's an import to CustomListWidgetItem
    #  and inside that there is some static icon that can only be loaded if Q.Application has started
    from resources.MainWindow import MainWindow

    main_window = MainWindow()
    main_window.show()

    app.exec()


if __name__ == '__main__':
    main()
