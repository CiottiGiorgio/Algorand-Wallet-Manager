"""
This file contains WalletFrame which is a QFrame that is displayed inside MainWindow.
"""


# PySide2
from PySide2 import QtWidgets, QtCore, QtGui

# Algorand
from algosdk import kmd
from algosdk.v2client import algod
from algosdk.wallet import Wallet as AlgosdkWallet

# Local project
from misc import Constants as ProjectConstants
from misc.Entities import Wallet
from misc.Widgets import LoadingWidget, ErrorWidget
from misc.Widgets import CustomListWidget
from Interfaces.Settings.Windows import SettingsWindow
from Interfaces.Main.WalletWidgets import WalletListItem, WalletListWidget
from Interfaces.Main.AddressFrame import AddressFrame

# Python standard libraries
from functools import partial
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
        self.kmd_client = None
        self.algod_client = None

        self.wallets = list()

        # Setup interface
        #   Main Horizontal Layout
        main_layout = QtWidgets.QHBoxLayout(self)

        self.list_wallet = CustomListWidget(self, WalletListItem, True)
        self.list_wallet.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        main_layout.addWidget(self.list_wallet)

        #   Button Layout on the right
        wallet_button_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(wallet_button_layout)

        #   Button creation, styling & add to Layout
        self.button_manage = QtWidgets.QPushButton("Manage\nAddresses")
        self.button_lock = QtWidgets.QPushButton("Lock")
        self.button_rename = QtWidgets.QPushButton("Rename")
        self.button_new = QtWidgets.QPushButton("New")
        self.button_import = QtWidgets.QPushButton("Import")
        # self.button_delete = QtWidgets.QPushButton("Delete")  # Not present in algosdk API
        self.button_export = QtWidgets.QPushButton("Export")

        button_fixed_width = 65
        buttons_list = [self.button_manage, self.button_lock, self.button_rename, self.button_new, self.button_import,
                        self.button_export]

        for widget in buttons_list:
            widget.setFixedWidth(button_fixed_width)

        wallet_button_layout.addWidget(self.button_manage)
        wallet_button_layout.addWidget(self.button_lock)
        wallet_button_layout.addStretch(1)
        wallet_button_layout.addWidget(self.button_rename)
        wallet_button_layout.addWidget(self.button_new)
        wallet_button_layout.addWidget(self.button_import)
        wallet_button_layout.addWidget(self.button_export)
        # End setup

        # Initial state
        # These widgets will be enabled when wallets are loaded.
        for widget in buttons_list:
            widget.setEnabled(False)

        # Connections
        self.list_wallet.currentItemChanged.connect(self.set_lock_button_status)
        self.button_manage.clicked.connect(self.manage_wallet)
        self.button_lock.clicked.connect(self.lock_wallet)

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
                self.wallet_loading_success,
                self.wallet_loading_failed
            )
        else:
            self.list_wallet.add_widget(ErrorWidget("kmd settings not valid"))

        if "algod" in SettingsWindow.rest_endpoints:
            self.algod_client = algod.AlgodClient(
                SettingsWindow.rest_endpoints["algod"]["token"],
                SettingsWindow.rest_endpoints["algod"]["address"]
            )
        else:
            print("algod settings not valid", file=stderr)

    def closeEvent(self, arg__1: QtGui.QCloseEvent):
        arg__1.accept()
        if self.worker:
            self.worker.signals.success.disconnect()
            self.worker.signals.error.disconnect()

    def showEvent(self, event: QtGui.QShowEvent):
        event.accept()

        self.set_lock_button_status()

    def unlock_item(self, item: WalletListItem) -> bool:
        """
        This method takes an item with a Wallet and creates an algosdk.wallet.Wallet creating a point for
        managing the kmd wallet.

        This method returns true if the wallet is already unlocked otherwise it unlocks it.
        """
        widget = self.list_wallet.itemWidget(item)

        if widget.wallet.algo_wallet:
            return True

        unlock_wallet_dialog = UnlockingWallet(self, widget.wallet)
        unlock_wallet_dialog.exec_()

        if unlock_wallet_dialog.return_value:
            widget.wallet.algo_wallet = unlock_wallet_dialog.return_value
            widget.set_locked(False)
            return True

        return False

    def lock_item(self, item: WalletListItem):
        """
        This methods destroys the algosdk.wallet.Wallet object saved inside Entities.Wallet and marks the corresponding
        widget as locked.
        """
        widget = self.list_wallet.itemWidget(item)

        widget.wallet.lock()
        widget.set_locked(True)

    @QtCore.Slot()
    def manage_wallet(self):
        """
        This method opens up the AddressFrame of a given wallet.
        """
        item = self.list_wallet.currentItem()
        if self.unlock_item(item):
            widget = self.list_wallet.itemWidget(item)

            ProjectConstants.main_window.main_widget.add_widget(
                AddressFrame(widget.wallet)
            )

    @QtCore.Slot()
    def lock_wallet(self):
        """
        This method locks the wallet and forgets user input password without needing to restart application.
        """
        item = self.list_wallet.currentItem()
        self.lock_item(item)
        self.set_lock_button_status()

    @QtCore.Slot()
    def set_lock_button_status(self):
        """
        This method sets self.lock_button enabled or not if the current selected item is locked or not.
        """
        item = self.list_wallet.currentItem()
        widget = self.list_wallet.itemWidget(item)
        if isinstance(widget, WalletListWidget):
            self.button_lock.setEnabled(
                self.list_wallet.itemWidget(item).label_state.text() == "(unlocked)"
            )

    @QtCore.Slot(list)
    def wallet_loading_success(self, wallets: list):
        """
        This method loads node wallet into the list and enables controls that can be applied to such wallets.

        This slot is connected to the result of the thread that.
        """
        self.list_wallet.clear_loading()

        # This is a mouthful. Basically for each dict in wallets that represents a wallet inside kmd, a Entities.Wallet
        #  object is created. This object is then appended to the internal list "self.wallets" inside WalletFrame.
        for wallet in wallets:
            self.wallets.append(
                Wallet(wallet)
            )

        for wallet in self.wallets:
            self.list_wallet.add_widget(
                WalletListWidget(wallet)
            )

        # Enable widgets that allow operation on an active node
        for widget in [self.button_new, self.button_import]:
            widget.setEnabled(True)

        # Also enable widgets that only make sense for the existence of at least one wallet.
        if len(wallets) >= 1:
            self.list_wallet.setCurrentRow(0)

            for widget in [self.button_manage, self.button_rename, self.button_export,
                           ProjectConstants.main_window.menu_action_new_transaction]:
                widget.setEnabled(True)

    @QtCore.Slot(str)
    def wallet_loading_failed(self, error: str):
        self.list_wallet.clear_loading()

        self.list_wallet.add_widget(
            ErrorWidget("Could not load wallets" + '\n' + error)
        )


class UnlockingWallet(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget, wallet: Wallet):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wallet = wallet
        self.return_value = None

        self.worker = None

        # Setup interface
        self.setWindowTitle("Unlock")

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(QtWidgets.QLabel("Please insert wallet's password:"))

        self.line_password = QtWidgets.QLineEdit()
        self.line_password.setEchoMode(QtWidgets.QLineEdit.Password)
        main_layout.addWidget(self.line_password)

        self.widget_loading = LoadingWidget("Unlocking wallet...")
        main_layout.addWidget(self.widget_loading)

        self.button_unlock = QtWidgets.QPushButton("Unlock")
        main_layout.addWidget(self.button_unlock, alignment=QtCore.Qt.AlignRight)
        # End setup

        # Initial state
        self.widget_loading.setVisible(False)
        self.button_unlock.setEnabled(False)

        # Connections
        self.line_password.textChanged.connect(self.set_button_unlock_state)
        self.button_unlock.clicked.connect(self.button_unlock_clicked)

    @QtCore.Slot(str)
    def set_button_unlock_state(self, new_text: str):
        self.button_unlock.setEnabled(
            new_text != ""
        )

    @QtCore.Slot()
    def button_unlock_clicked(self):
        self.line_password.setEnabled(False)
        self.button_unlock.setEnabled(False)
        self.widget_loading.setVisible(True)

        self.worker = ProjectConstants.main_window.start_worker(
            # We have to use partial because for some reason the creation of an object is not considered a callable.
            #  I still have to look into this.
            partial(
                AlgosdkWallet,
                self.wallet.info["name"],
                self.line_password.text(),
                self.parent().kmd_client
            ),
            self.unlock_success,
            self.unlock_failure
        )

    @QtCore.Slot(object)
    def unlock_success(self, result: object):
        self.return_value = result
        self.close()

    # TODO make it obvious for the user that an error has occurred.
    @QtCore.Slot(str)
    def unlock_failure(self, error: str):
        print("Could not open wallet.", file=stderr)
        print(error, file=stderr)
        self.return_value = None
        self.close()
