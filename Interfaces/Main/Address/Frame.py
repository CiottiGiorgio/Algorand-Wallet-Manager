"""
This file contains AddressFrame which is a QFrame displayed as a result of an opened wallet.
"""

# PySide2
from PySide2 import QtWidgets, QtCore, QtGui

# Local project
from misc.Entities import Wallet
from misc.Functions import find_main_window
from Interfaces.Main.Address.Ui_Frame import Ui_AddressFrame
from Interfaces.Main.Address.Ui_BalanceWindow import Ui_BalanceWindow
from Interfaces.Main.Address.Widgets import BalanceScrollWidget

# Python standard libraries
from functools import partial


class AddressFrame(QtWidgets.QFrame, Ui_AddressFrame):
    def __init__(self, parent: QtWidgets.QWidget, wallet: Wallet):
        super().__init__(parent)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wallet = wallet

        self.setupUi(self)

        # Connections
        #   listWidget
        self.listWidget.itemDoubleClicked.connect(self.show_balance)
        self.listWidget.customContextMenuRequested.connect(self.show_context_menu)

        #   pushButtons
        self.pushButton_return.clicked.connect(self.close)
        self.pushButton_open_balance.clicked.connect(self.show_balance)
        self.pushButton_new.clicked.connect(self.new_address)
        self.pushButton_delete.clicked.connect(self.delete_address)
        self.pushButton_import.clicked.connect(self.import_address)
        self.pushButton_export.clicked.connect(self.export_address)

        # Worker
        # We load the addresses in a non threaded way for now. It's reasonable because if we are at this point we know
        #  there is a working kmd server online.
        addresses = self.wallet.algo_wallet.list_keys()

        for address in addresses:
            self.listWidget.addItem(address)

        if len(addresses) >= 1:
            self.listWidget.setCurrentRow(0)

            for widget in [self.pushButton_open_balance, self.pushButton_delete, self.pushButton_export]:
                widget.setEnabled(True)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        if key == int(QtCore.Qt.Key_Return):
            if self.listWidget.hasFocus():
                self.show_balance()
        elif key == int(QtCore.Qt.Key_Escape):
            self.close()

    @QtCore.Slot()
    def show_balance(self, item: QtWidgets.QListWidgetItem = None):
        if not item:
            item = self.listWidget.currentItem()

        if not find_main_window().wallet_frame.algod_client:
            QtWidgets.QMessageBox.critical(self, "algod settings", "Please check algod settings.")
            return

        try:
            account_info = find_main_window().wallet_frame.algod_client.account_info(item.text())
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Could not load balance", str(e))
        else:
            dialog = BalanceWindow(self, account_info)
            dialog.exec_()

    @QtCore.Slot()
    def new_address(self):
        try:
            self.wallet.algo_wallet.generate_key()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Could not generate new address", str(e))
        else:
            self.restart()

    @QtCore.Slot()
    def delete_address(self):
        item = self.listWidget.currentItem()

        if QtWidgets.QMessageBox.question(
            self, "Deleting address",
            "Please keep in mind that deleting an address means that it will disappear from the wallet.\n\n"
            "However there is no way to delete the presence of this address from the blockchain.\n\n"
            "Would you like to continue?"
        ) != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        try:
            self.wallet.algo_wallet.delete_key(item.text())
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Could not delete address", str(e))
        else:
            self.restart()

    @QtCore.Slot()
    def import_address(self):
        if QtWidgets.QMessageBox.question(
                self, "Importing address",
                "Please keep in mind that, when recovering a wallet in the future, only the addresses derived from "
                "the Master Derivation Key are restored.\n\n"
                "Importing an address inside a wallet is not the same as deriving it from the wallet.\n\n"
                "Would you like to continue?"
        ) != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        new_address = QtWidgets.QInputDialog.getText(
            self, "Importing address",
            "Please fill in with the address private key", QtWidgets.QLineEdit.EchoMode.Password
        )
        if new_address[1]:
            try:
                self.wallet.algo_wallet.import_key(new_address[0])
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Could not import address", str(e))
            else:
                self.restart()

    @QtCore.Slot()
    def export_address(self):
        item = self.listWidget.currentItem()

        try:
            private_key = self.wallet.algo_wallet.export_key(item.text())
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Could not export address", str(e))
        else:
            QtGui.QGuiApplication.clipboard().setText(private_key)
            QtWidgets.QMessageBox.information(self, "Success", "Private key copied into clipboard")

    @QtCore.Slot(QtCore.QPoint)
    def show_context_menu(self, pos: QtCore.QPoint):
        if item := self.listWidget.itemAt(pos):
            menu = QtWidgets.QMenu(self)

            menu.addAction("Copy to clipboard", partial(QtGui.QGuiApplication.clipboard().setText, item.text()))

            global_pos = self.listWidget.mapToGlobal(pos)
            menu.exec_(global_pos)

            menu.deleteLater()

    def restart(self):
        queued_widget = find_main_window().queuedWidget

        queued_widget.remove_top_widget()
        queued_widget.add_widget(AddressFrame(queued_widget, self.wallet))


class BalanceWindow(QtWidgets.QDialog, Ui_BalanceWindow):
    def __init__(self, parent: QtWidgets.QWidget, account_info: dict):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.account_info = account_info

        self.setupUi(self)

        self.label_balance.setText(str(account_info["amount-without-pending-rewards"]) + " microAlgos")
        self.label_pending_rewards.setText(str(account_info["pending-rewards"]) + " microAlgos")

        for asset in account_info["assets"]:
            self.verticalLayout_assets.addWidget(
                BalanceScrollWidget(
                    "id - " + str(asset["asset-id"]),
                    str(asset["amount"])
                )
            )
        self.verticalLayout_assets.addStretch(1)
