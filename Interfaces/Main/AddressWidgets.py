"""
Custom c
lasses for QListWidget for AddressFrame
"""


# PySide2
from PySide2 import QtWidgets, QtCore


class AddressListItem(QtWidgets.QListWidgetItem):
    """
    Empty class that might be useful in the future.
    """
    pass


class AddressListWidget(QtWidgets.QWidget):
    """
    Address widget for the list in AddressFrame.
    """
    def __init__(self):
        super().__init__()

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Setup interface
        main_layout = QtWidgets.QHBoxLayout(self)

        label_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(label_layout)
        main_layout.addStretch(1)

        self.label_primary = None
