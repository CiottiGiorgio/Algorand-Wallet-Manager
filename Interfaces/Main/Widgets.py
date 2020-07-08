"""
Custom classes for QListWidget for WalletFrame

Subclass for QWidget is the representation inside the list in WalletFrame
Subclass for QListWidgetItem is not really needed right now because there is not ordering inside WalletFrame list.
However it is still used in the code because one day we might need to implement functionality.
"""

# PySide 2
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

        # Setup interface
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 10, 5)

        #   Here the inner layout is created inside addLayout but also is assigned to label_layout
        #    using walrus operator.
        main_layout.addLayout(label_layout := QtWidgets.QVBoxLayout())

        #   Here the label with the name of the wallet is created, styled and added to the window
        self.label_name = QtWidgets.QLabel(wallet.name)
        self.label_name.setStyleSheet("font: 13pt;")
        label_layout.addWidget(self.label_name)

        #   Same for the info label
        self.label_info = QtWidgets.QLabel(wallet.info)
        self.label_info.setStyleSheet("font: 8pt;")
        label_layout.addWidget(self.label_info)

        main_layout.addStretch(1)
        # End setup
