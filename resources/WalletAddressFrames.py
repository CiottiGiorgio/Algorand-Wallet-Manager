"""
This file contains two frames used in MainWindow.
"""


# PySide2
from PySide2 import QtWidgets, QtCore

# Algorand
from algosdk import kmd

# Local project
from resources.Entities import Wallet, AlgorandWorker
from resources.SettingsWindow import SettingsWindow
from resources.CustomListWidgetItem import WalletListItem, WalletListWidget

# Python standard libraries
from sys import stderr


class WalletsFrame(QtWidgets.QFrame):
    """
    This class is the frame for the list of wallet in an Algorand node and the action on those wallets.
    """
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # API for Algorand node KMD client
        self.kmd_client = kmd.KMDClient(
            SettingsWindow.rest_endpoints["kmd"]["token"],
            SettingsWindow.rest_endpoints["kmd"]["address"]
        )

        # Setup interface
        #   Main Horizontal Layout
        main_layout = QtWidgets.QHBoxLayout()

        self.list_wallet = QtWidgets.QListWidget()
        #   List of wallet in the connected Algorand node
        #    scrolling is PerPixel because otherwise the list scrolls PerItem and it's not desirable.
        self.list_wallet.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        main_layout.addWidget(self.list_wallet)

        #   Button Layout on the right
        wallet_button_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(wallet_button_layout)

        #   Button creation, styling & add to Layout
        self.button_manage = QtWidgets.QPushButton("Manage\nAddresses")
        self.button_rename = QtWidgets.QPushButton("Rename")
        self.button_new = QtWidgets.QPushButton("New")
        self.button_import = QtWidgets.QPushButton("Import")
        self.button_delete = QtWidgets.QPushButton("Delete")
        self.button_export = QtWidgets.QPushButton("Export")

        button_fixed_width = 65
        self.button_manage.setFixedWidth(button_fixed_width)
        self.button_rename.setFixedWidth(button_fixed_width)
        self.button_new.setFixedWidth(button_fixed_width)
        self.button_import.setFixedWidth(button_fixed_width)
        self.button_delete.setFixedWidth(button_fixed_width)
        self.button_export.setFixedWidth(button_fixed_width)

        wallet_button_layout.addWidget(self.button_manage)
        wallet_button_layout.addStretch(1)
        wallet_button_layout.addWidget(self.button_rename)
        wallet_button_layout.addWidget(self.button_new)
        wallet_button_layout.addWidget(self.button_import)
        wallet_button_layout.addWidget(self.button_delete)
        wallet_button_layout.addWidget(self.button_export)

        #   Setting the frame main layout
        self.setLayout(main_layout)
        # End setup

        # These widgets will be enabled when wallets are loaded.
        for button in [self.button_manage, self.button_rename, self.button_new,
                       self.button_import, self.button_delete, self.button_export]:
            button.setEnabled(False)

        # Load wallets in a threaded way
        # TODO make a macro for this code.
        worker = AlgorandWorker(self.kmd_client.list_wallets)
        # TODO what happens to this worker and this connection after the job is done?
        worker.signals.result.connect(self.load_wallets)
        # TODO implement if this threaded function returns an error.
        worker.signals.error.connect(lambda x: print(x, file=stderr))
        self.parent().thread_pool.start(worker)

    # TODO sort of code duplication for the list of contacts and in the future list of addresses?
    def add_item(self, widget: WalletListWidget):
        """
        This method add a WalletListWidget to self.list_wallet through a WalletListItem
        """
        item = WalletListItem()
        item.setSizeHint(widget.minimumSizeHint())
        self.list_wallet.addItem(item)
        self.list_wallet.setItemWidget(item, widget)

    @QtCore.Slot(list)
    def load_wallets(self, wallets):
        """
        This method loads node wallet into the list and enables controls that can be applied to such wallets.

        This slot is connected to the result of the thread that
        """
        for wallet in wallets:
            self.add_item(
                WalletListWidget(
                    Wallet(wallet["name"], wallet["id"])
                )
            )

        # Enable widgets that allow operation on an active node
        for widget in [self.button_new, self.button_import]:
            widget.setEnabled(True)

        # Also enable widgets that only make sense for the existence of at least one wallet.
        # TODO make the parent enable the menu_action for itself?
        if len(wallets) >= 1:
            for widget in [self.button_manage, self.button_rename, self.button_export, self.button_delete,
                           self.parent().menu_action_new_transaction]:
                widget.setEnabled(True)
