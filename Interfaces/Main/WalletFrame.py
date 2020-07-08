"""
This file contains two frames used in Main.
"""


# PySide2
from PySide2 import QtWidgets, QtCore

# Algorand
from algosdk import kmd

# Local project
from misc.Entities import Wallet, LoadingWidget, ErrorWidget
from Interfaces.Settings.Windows import SettingsWindow
from Interfaces.Contacts.Widgets import WalletListItem, WalletListWidget

# Python standard libraries
from functools import partial


class WalletsFrame(QtWidgets.QFrame):
    """
    This class is the frame for the list of wallet in an Algorand node and the action on those wallets.
    """
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # API for Algorand node KMD client
        self.kmd_client = None

        # Setup interface
        #   Main Horizontal Layout
        main_layout = QtWidgets.QHBoxLayout(self)

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
        # self.button_delete = QtWidgets.QPushButton("Delete")  # Not present in algosdk API
        self.button_export = QtWidgets.QPushButton("Export")

        button_fixed_width = 65
        self.button_manage.setFixedWidth(button_fixed_width)
        self.button_rename.setFixedWidth(button_fixed_width)
        self.button_new.setFixedWidth(button_fixed_width)
        self.button_import.setFixedWidth(button_fixed_width)
        # self.button_delete.setFixedWidth(button_fixed_width)
        self.button_export.setFixedWidth(button_fixed_width)

        wallet_button_layout.addWidget(self.button_manage)
        wallet_button_layout.addStretch(1)
        wallet_button_layout.addWidget(self.button_rename)
        wallet_button_layout.addWidget(self.button_new)
        wallet_button_layout.addWidget(self.button_import)
        # wallet_button_layout.addWidget(self.button_delete)
        wallet_button_layout.addWidget(self.button_export)
        # End setup

        # Connections
        pass

        # These widgets will be enabled when wallets are loaded.
        for widget in [self.button_manage, self.button_rename, self.button_new,
                       self.button_import, self.button_export]:
            widget.setEnabled(False)

        if "kmd" in SettingsWindow.rest_endpoints:
            self.kmd_client = kmd.KMDClient(
                SettingsWindow.rest_endpoints["kmd"]["token"],
                SettingsWindow.rest_endpoints["kmd"]["address"]
            )

            # Load wallets in a threaded way.
            # I think there's no need to disconnect slots from this worker because the next call will overwrite
            #  self.worker thus finalizing that object and disconnect its slots. Haven't tested though.
            self.worker = self.parent().start_worker(
                self.kmd_client.list_wallets,
                self.load_wallets,
                lambda x: self.add_item(ErrorWidget(x))
            )

            #   For some reasons if i make a slot that disconnects these signals it doesn't get called. I think i might
            #    be dealing with python finalizer and Qt C++ destroyer issues.
            self.destroyed.connect(lambda: self.worker.signals.success.disconnect())
            self.destroyed.connect(lambda: self.worker.signals.error.disconnect())

            # We insert a loading widget to signal to the user that a call is in progress but we do so only if
            #  a fixed time has elapsed without a response.
            self.timer_loading_widget = QtCore.QTimer(self)
            self.timer_loading_widget.setSingleShot(True)
            self.timer_loading_widget.timeout.connect(
                partial(self.add_item, LoadingWidget("Loading wallets..."))
            )
            self.timer_loading_widget.start(300)
        else:
            self.add_item(ErrorWidget("kmd settings not valid"))

    # This method is add_item but asks for a widget. This makes sense because this method always adds a WalletListItem.
    #  I know it's confusing but it works.
    def add_item(self, widget: WalletListWidget):
        """
        This method add a WalletListWidget to self.list_wallet through a WalletListItem.
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
        # Prevent timer from adding loading widget.
        self.timer_loading_widget.stop()
        self.timer_loading_widget.deleteLater()

        # At this point the only possible item present should be the loading widget. We remove it before adding
        #  wallet widgets.
        if self.list_wallet.count() > 0:
            self.list_wallet.takeItem(0)

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
        if len(wallets) >= 1:
            for widget in [self.button_manage, self.button_rename, self.button_export,
                           self.parent().menu_action_new_transaction]:
                widget.setEnabled(True)