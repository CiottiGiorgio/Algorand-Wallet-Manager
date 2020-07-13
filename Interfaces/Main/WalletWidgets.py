"""
Custom classes for QListWidget for WalletFrame

Subclass for QWidget is the representation inside the list in WalletFrame
Subclass for QListWidgetItem is not really needed right now because there is not ordering inside WalletFrame list.
However it is still used in the code because one day we might need to implement functionality.
"""

# PySide2
from PySide2 import QtWidgets, QtCore

# Local project
from misc.Entities import Wallet


class WalletListItem(QtWidgets.QListWidgetItem):
    """
    Dummy class for items in list_wallet. It's kept for the event in which we need to implement
    functionality in the future.
    """
    pass


class WalletListWidget(QtWidgets.QWidget):
    """
    Wallet widget for the list in WalletFrame.
    """
    def __init__(self, wallet: Wallet):
        super().__init__()

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wallet = wallet

        # Setup interface
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(10, 5, 10, 5)

        self.label_primary = QtWidgets.QLabel(self.wallet.info["name"])
        self.label_primary.setStyleSheet("font: 13pt;")
        main_layout.addWidget(self.label_primary, 0, 0, rowSpan=2)

        self.label_secondary = QtWidgets.QLabel(self.wallet.info["id"])
        self.label_secondary.setStyleSheet("font: 8pt;")
        main_layout.addWidget(self.label_secondary, 1, 0)

        self.label_state = QtWidgets.QLabel()
        main_layout.addWidget(self.label_state, 1, 1, alignment=QtCore.Qt.AlignRight)
        # End setup

    def set_locked(self, value: bool):
        self.label_state.setText(
            "" if value else "(unlocked)"
        )
