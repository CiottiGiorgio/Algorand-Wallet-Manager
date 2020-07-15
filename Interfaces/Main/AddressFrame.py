"""
This file contains AddressFrame which is a QFrame displayed as a result of an opened wallet.
"""

# PySide2
from PySide2 import QtWidgets, QtCore, QtGui

# Local project
from misc import Constants as ProjectConstants
from misc.Entities import Wallet


class AddressFrame(QtWidgets.QFrame):
    def __init__(self, wallet: Wallet):
        super().__init__()

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wallet = wallet

        # Setup interface
        main_layout = QtWidgets.QHBoxLayout(self)

        self.list_address = QtWidgets.QListWidget()
        self.list_address.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        main_layout.addWidget(self.list_address)

        address_button_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(address_button_layout)

        #   Button creation, styling & add to layout
        self.button_return = QtWidgets.QPushButton("Return")
        self.button_balance = QtWidgets.QPushButton("Open\nbalance")
        self.button_new = QtWidgets.QPushButton("New")
        self.button_delete = QtWidgets.QPushButton("Delete")
        self.button_import = QtWidgets.QPushButton("Import")
        self.button_export = QtWidgets.QPushButton("Export")

        list_buttons = [self.button_return, self.button_balance, self.button_new,
                        self.button_delete, self.button_import, self.button_export]

        button_fixed_width = 65
        for widget in list_buttons:
            widget.setFixedWidth(button_fixed_width)

        address_button_layout.addWidget(self.button_return)
        address_button_layout.addWidget(self.button_balance)
        address_button_layout.addStretch(1)
        address_button_layout.addWidget(self.button_new)
        address_button_layout.addWidget(self.button_delete)
        address_button_layout.addWidget(self.button_import)
        address_button_layout.addWidget(self.button_export)
        # End setup

        # Initial state
        for widget in [self.button_balance, self.button_export, self.button_delete]:
            widget.setEnabled(False)

        # Connections
        self.button_return.clicked.connect(self.close)

    def showEvent(self, event: QtGui.QShowEvent):
        event.accept()

        # We load the addresses in a non threaded way for now.
        addresses = self.wallet.algo_wallet.list_keys()

        if len(addresses) >= 1:
            for widget in [self.button_balance, self.button_export, self.button_delete]:
                widget.setEnabled(True)

        for address in addresses:
            self.list_address.addItem(address)
            print(ProjectConstants.wallet_frame.algod_client.account_info(address))
