"""
This file contains info window.

Things like author licences and outsourcing images.
"""


# PySide2
from PySide2 import QtWidgets, QtCore


class InfoWindow(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setWindowTitle("Info")

        main_layout = QtWidgets.QVBoxLayout()
        # We let the window resize to the fixed dimension of children widgets rather than setting the size and then
        #  making the children widgets fit.
        main_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        next_label = QtWidgets.QLabel("Algorand Wallet Manager\n")
        next_label.setStyleSheet("font-weight: bold;")
        next_label.setAlignment(QtCore.Qt.AlignHCenter)
        main_layout.addWidget(next_label)

        next_label = QtWidgets.QLabel("This software is released under MIT Licence\n")
        next_label.setAlignment(QtCore.Qt.AlignHCenter)
        main_layout.addWidget(next_label)

        next_label = QtWidgets.QLabel("Author: Ciotti Giorgio")
        next_label.setAlignment(QtCore.Qt.AlignHCenter)
        main_layout.addWidget(next_label)

        next_label = QtWidgets.QLabel()
        next_label.setText("Email: <a href=\"mailto:ciotti.giorgio.96@gmail.com\">ciotti.giorgio.96@gmail.com</a>")
        next_label.setOpenExternalLinks(True)
        next_label.setAlignment(QtCore.Qt.AlignHCenter)
        main_layout.addWidget(next_label)

        self.setLayout(main_layout)


class CreditsWindow(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setWindowTitle("Credits")

        main_layout = QtWidgets.QVBoxLayout()
        # We let the window resize to the fixed dimension of children widgets rather than setting the size and then
        #  making the children widgets fit.
        main_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        next_label = QtWidgets.QLabel("Credits for the icons used in this application:\n\n"
                                      "Freepik, Those Icons & Pixel perfect\n"
                                      "from www.flaticon.com")
        next_label.setAlignment(QtCore.Qt.AlignHCenter)
        main_layout.addWidget(next_label)

        self.setLayout(main_layout)
