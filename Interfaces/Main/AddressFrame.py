"""
This file contains AddressFrame which is a QFrame displayed as a result of an opened wallet.
"""

# PySide2
from PySide2 import QtWidgets, QtCore

# Local project
from misc import Constants as ProjectConstants
from misc.Entities import Wallet
from Interfaces.Main.AddressWidgets import BalanceScrollWidget


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

        buttons_list = [self.button_return, self.button_balance, self.button_new,
                        self.button_delete, self.button_import, self.button_export]

        button_fixed_width = 65
        for widget in buttons_list:
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
        self.button_balance.clicked.connect(self.show_balance)

        # Worker
        # We load the addresses in a non threaded way for now.
        addresses = self.wallet.algo_wallet.list_keys()

        for address in addresses:
            self.list_address.addItem(address)

        if len(addresses) >= 1:
            self.list_address.setCurrentRow(0)

            for widget in [self.button_balance, self.button_export, self.button_delete]:
                widget.setEnabled(True)

    def show_balance(self):
        item = self.list_address.currentItem()

        dialog = BalanceWindow(self, item.text())
        dialog.exec_()


class BalanceWindow(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget, address: str):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.address = address

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Setup interface
        self.setWindowTitle("Algos & Assets")

        self.setFixedSize(500, 500)

        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.addWidget(QtWidgets.QLabel("Algos:"))

        scrollable_algos = QtWidgets.QScrollArea()
        main_layout.addWidget(scrollable_algos)
        algos_layout = QtWidgets.QVBoxLayout()
        scrollable_algos.setLayout(algos_layout)

        main_layout.addWidget(QtWidgets.QLabel("Assets:"))

        scrollable_assets = QtWidgets.QScrollArea()
        scrollable_assets.setWidget(content_widget := QtWidgets.QWidget())
        scrollable_assets.setWidgetResizable(True)
        main_layout.addWidget(scrollable_assets)
        assets_layout = QtWidgets.QVBoxLayout()
        content_widget.setLayout(assets_layout)

        main_layout.setStretch(3, 1)
        # End setup

        account_info = ProjectConstants.wallet_frame.algod_client.account_info(self.address)

        algos_layout.addWidget(
            BalanceScrollWidget(
                "Balance:",
                str(account_info["amount-without-pending-rewards"]) + " microAlgos"
            )
        )
        algos_layout.addWidget(
            BalanceScrollWidget(
                "Pending rewards:",
                str(account_info["pending-rewards"]) + " microAlgos"
            )
        )

        for i, asset in enumerate(account_info["assets"]):
            assets_layout.addWidget(
                BalanceScrollWidget(
                    "id - " + str(asset["asset-id"]),
                    str(asset["amount"])
                )
            )
        assets_layout.addStretch(1)
