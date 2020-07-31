"""
Custom c
lasses for QListWidget for AddressFrame
"""


# PySide2
from PySide2 import QtWidgets, QtCore


class BalanceScrollWidget(QtWidgets.QWidget):
    def __init__(self, name, quantity):
        super().__init__()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Setup interface
        main_layout = QtWidgets.QHBoxLayout(self)

        self.label_name = QtWidgets.QLabel(name)
        main_layout.addWidget(self.label_name, alignment=QtCore.Qt.AlignLeft)

        self.label_quantity = QtWidgets.QLabel(quantity)
        main_layout.addWidget(self.label_quantity, alignment=QtCore.Qt.AlignRight)
        # End setup
