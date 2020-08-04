"""
This file contains WalletFrame which is a QFrame that is displayed inside MainWindow.
"""


# PySide2
from PySide2 import QtWidgets, QtCore, QtGui

# Algorand
from algosdk import kmd
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk.wallet import Wallet as AlgosdkWallet
from algosdk.mnemonic import to_master_derivation_key

# Local project
from misc.Entities import Wallet
from misc.Functions import find_main_window
from Interfaces.Main.Wallet.Ui_Frame import Ui_WalletFrame
from Interfaces.Main.Wallet.Ui_WalletUnlock import Ui_WalletUnlock
from Interfaces.Main.Wallet.Ui_NewImportWallet import Ui_NewImportWallet
from Interfaces.Main.Wallet.Widgets import WalletListItem, WalletListWidget
from Interfaces.Main.Address.Frame import AddressFrame
from Interfaces.Settings.Window import SettingsWindow

# Python standard libraries
from functools import partial
from sys import stderr


class WalletsFrame(QtWidgets.QFrame, Ui_WalletFrame):
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
        self.indexer_client = None

        self.setupUi(self)

        self.listWidget.set_item_type(WalletListItem)
        self.listWidget.activate_timer()

        # Connections
        self.listWidget.itemDoubleClicked.connect(self.manage_wallet)
        self.pushButton_Manage.clicked.connect(self.manage_wallet)
        self.pushButton_LockUnlock.clicked.connect(self.lock_unlock_wallet)
        self.pushButton_Rename.clicked.connect(self.rename_wallet)
        self.pushButton_NewImport.clicked.connect(self.new_import_wallet)
        self.pushButton_Export.clicked.connect(self.export_wallet)

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
            self.listWidget.clear_loading()
            QtWidgets.QMessageBox.critical(self, "kmd settings", "kmd settings not valid.")

        if "algod" in SettingsWindow.rest_endpoints:
            self.algod_client = AlgodClient(
                SettingsWindow.rest_endpoints["algod"]["token"],
                SettingsWindow.rest_endpoints["algod"]["address"]
            )
        else:
            print("algod settings not valid.", file=stderr)

        if "indexer" in SettingsWindow.rest_endpoints:
            self.indexer_client = IndexerClient(
                SettingsWindow.rest_endpoints["indexer"]["token"],
                SettingsWindow.rest_endpoints["indexer"]["address"]
            )
        else:
            pass
            # print("indexer settings not valid.", file=stderr)

    def closeEvent(self, arg__1: QtGui.QCloseEvent):
        if self.worker:
            self.worker.signals.success.disconnect()
            self.worker.signals.error.disconnect()
        arg__1.accept()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == int(QtCore.Qt.Key_Return) and self.listWidget.hasFocus():
            self.manage_wallet()

    @QtCore.Slot()
    def manage_wallet(self, item: WalletListItem = None):
        """
        This method opens up the AddressFrame of a given wallet.
        """
        if not item:
            item = self.listWidget.currentItem()

        if self.unlock_item(item):
            widget = self.listWidget.itemWidget(item)

            queued_widget = find_main_window().queuedWidget
            queued_widget.add_widget(
                AddressFrame(queued_widget, widget.wallet)
            )

    @QtCore.Slot()
    def rename_wallet(self):
        item = self.listWidget.currentItem()

        if self.unlock_item(item):
            widget = self.listWidget.itemWidget(item)

            new_name = QtWidgets.QInputDialog.getText(
                self, "Rename", "New name",
                QtWidgets.QLineEdit.EchoMode.Normal,
                widget.wallet.info["name"]
            )
            if new_name[1]:
                try:
                    # FIXME These functions could both raise an error and we wouldn't know at which point occurred.
                    # FIXME Put this bad boi in a thread because these calls last quite a while.
                    # Actually if only one of this operation fails it's not clear how to revert the one that succeeded.
                    widget.wallet.algo_wallet.rename(new_name[0])
                    widget.wallet.info = widget.wallet.algo_wallet.info()["wallet"]
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Could not rename", str(e))
                else:
                    widget.label_primary.setText(new_name[0])

    @QtCore.Slot()
    def new_import_wallet(self):
        # TODO when importing a wallet ask the user how many addresses must be recovered.
        input_dialog = NewImportWallet(self)

        if input_dialog.exec_() == QtWidgets.QDialog.Accepted:
            try:
                new_wallet = self.kmd_client.create_wallet(
                    input_dialog.return_value[0], input_dialog.return_value[1],
                    master_deriv_key=to_master_derivation_key(
                        input_dialog.return_value[2] if input_dialog.return_value[2] != "" else None
                    )
                )
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Could not create wallet", str(e))
            else:
                self.listWidget.add_widget(
                    WalletListWidget(
                        Wallet(new_wallet)
                    )
                )

    @QtCore.Slot()
    def export_wallet(self):
        item = self.listWidget.currentItem()

        if self.unlock_item(item):
            widget = self.listWidget.itemWidget(item)

            try:
                mnemonic_mdk = widget.wallet.algo_wallet.get_mnemonic()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Could not export wallet", str(e))
            else:
                QtGui.QGuiApplication.clipboard().setText(mnemonic_mdk)
                QtWidgets.QMessageBox.information(
                    self, "Success", "Mnemonic master derivation key copied into clipboard"
                )

    @QtCore.Slot()
    def lock_unlock_wallet(self):
        """
        This method unlocks a locked item and viceversa.
        """
        item = self.listWidget.currentItem()
        widget = self.listWidget.itemWidget(item)

        if widget.wallet.algo_wallet:
            self.lock_item(item)
        else:
            self.unlock_item(item)

    @QtCore.Slot(list)
    def wallet_loading_success(self, wallets: list):
        """
        This method loads node wallet into the list and enables controls that can be applied to such wallets.

        This slot is connected to the result of the thread that.
        """
        self.listWidget.clear_loading()

        for wallet in wallets:
            self.listWidget.add_widget(
                WalletListWidget(
                    Wallet(wallet)
                )
            )

        # Enable widgets that allow operation on an active node
        for widget in [self.pushButton_NewImport]:
            widget.setEnabled(True)

        # Also enable widgets that only make sense for the existence of at least one wallet.
        if len(wallets) >= 1:
            self.listWidget.setCurrentRow(0)

            for widget in [self.pushButton_Manage, self.pushButton_LockUnlock, self.pushButton_Rename,
                           self.pushButton_Export, find_main_window().menuAction_NewTransaction]:
                widget.setEnabled(True)

    @QtCore.Slot(Exception)
    def wallet_loading_failed(self, error: Exception):
        self.listWidget.clear_loading()

        QtWidgets.QMessageBox.critical(self, "Could not load wallets", str(error))

    def unlock_item(self, item: WalletListItem) -> bool:
        """
        This method takes an item with a misc.Entities.Wallet and creates an algosdk.wallet.Wallet creating a point for
        managing the kmd wallet.

        This method returns true if the wallet is already unlocked otherwise it tries to unlock it.
        """
        widget = self.listWidget.itemWidget(item)

        if widget.wallet.algo_wallet:
            return True

        unlock_wallet_dialog = UnlockingWallet(self, widget.wallet)
        if unlock_wallet_dialog.exec_() == QtWidgets.QDialog.Accepted:
            widget.wallet.algo_wallet = unlock_wallet_dialog.return_value
            widget.set_locked(False)
            return True

        return False

    def lock_item(self, item: WalletListItem):
        """
        This methods destroys the algosdk.wallet.Wallet object saved inside Entities.Wallet and marks the corresponding
        widget as locked.
        """
        widget = self.listWidget.itemWidget(item)

        widget.wallet.lock()
        widget.set_locked(True)


class UnlockingWallet(QtWidgets.QDialog, Ui_WalletUnlock):
    def __init__(self, parent: QtWidgets.QWidget, wallet: Wallet):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wallet = wallet
        self.return_value = None

        self.worker = None

        self.setupUi(self)

        self.widget.setVisible(False)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        # Connections
        self.lineEdit.textChanged.connect(self.validate_inputs)

    def closeEvent(self, arg__1: QtGui.QCloseEvent):
        if self.worker:
            self.worker.signals.success.disconnect()
            self.worker.signals.error.disconnect()
        arg__1.accept()

    @QtCore.Slot(str)
    def validate_inputs(self, new_text: str):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(
            new_text != ""
        )

    # We override accept of this class and don't use super().accept() inside.
    #  This is because we just treat this method as a slot connected to the OK button.
    #  Either super().accept() or super().reject() will be eventually called when the worker is done.
    def accept(self):
        self.lineEdit.setEnabled(False)
        self.widget.setVisible(True)
        self.buttonBox.setEnabled(False)

        self.worker = find_main_window().start_worker(
            # We have to use partial because for some reason the creation of an object is not considered a callable.
            #  I still have to look into this.
            partial(
                AlgosdkWallet,
                self.wallet.info["name"],
                self.lineEdit.text(),
                find_main_window().wallet_frame.kmd_client
            ),
            self.unlock_success,
            self.unlock_failure
        )

    @QtCore.Slot(object)
    def unlock_success(self, result: object):
        self.return_value = result
        super().accept()

    @QtCore.Slot(Exception)
    def unlock_failure(self, error: Exception):
        QtWidgets.QMessageBox.critical(self, "Could not open wallet", str(error))
        self.return_value = None
        super().reject()


class NewImportWallet(QtWidgets.QDialog, Ui_NewImportWallet):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.return_value = None

        self.setupUi(self)

        # Connections
        self.lineEdit_Name.textChanged.connect(self.validate_inputs)
        self.lineEdit_Password.textChanged.connect(self.validate_inputs)
        self.lineEdit_Password2.textChanged.connect(self.validate_inputs)
        self.plainTextEdit_MDK.textChanged.connect(self.validate_inputs)

        self.validate_inputs()

    def validate_inputs(self):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(
            self.lineEdit_Name.text != "" and
            self.lineEdit_Password.text() != "" and
            self.lineEdit_Password.text() == self.lineEdit_Password2.text()
        )

    def accept(self):
        self.return_value = (
            self.lineEdit_Name.text(), self.lineEdit_Password.text(), self.plainTextEdit_MDK.toPlainText()
        )
        super().accept()
