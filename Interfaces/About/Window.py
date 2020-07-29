"""
This file contains info window.

Things like author licences and outsourcing images.
These windows are made so that they fit the content rather than the content fits the dimention of the window.
"""


# PySide2
from PySide2 import QtWidgets, QtCore

# Local project
from Interfaces.About.Ui_Info import Ui_Info
from Interfaces.About.Ui_Credits import Ui_Credits


class InfoWindow(QtWidgets.QDialog, Ui_Info):
    """
    This class is the info about this application window
    """
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Setup interface
        self.setupUi(self)
        # End setup


class CreditsWindow(QtWidgets.QDialog, Ui_Credits):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Setup interface
        self.setupUi(self)
        # End setup
