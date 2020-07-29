"""
This file contains AddressFrame which is a QFrame displayed as a result of an opened wallet.
"""

# PySide2
from PySide2 import QtWidgets, QtCore, QtGui

# Local project
from misc import Constants as ProjectConstants
from misc.Entities import Wallet
from Interfaces.Main.Address.Ui_Frame import Ui_AddressFrame
from Interfaces.Main.Address.Ui_BalanceWindow import Ui_BalanceWindow
from Interfaces.Main.Address.Widgets import AddressListItem
from Interfaces.Main.Address.Widgets import BalanceScrollWidget

# Python standard libraries
from functools import partial


class AddressFrame(QtWidgets.QFrame, Ui_AddressFrame):
    def __init__(self, wallet: Wallet):
        super().__init__()

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wallet = wallet

        self.setupUi(self)

        self.listWidget.set_item_type(AddressListItem)

        # Connections
        self.pushButton_return.clicked.connect(self.close)
        self.pushButton_open_balance.clicked.connect(self.show_balance)
        self.listWidget.customContextMenuRequested.connect(self.show_context_menu)
        self.listWidget.itemDoubleClicked.connect(self.show_balance)

        # Worker
        # We load the addresses in a non threaded way for now.
        addresses = self.wallet.algo_wallet.list_keys()

        for address in addresses:
            self.listWidget.addItem(address)

        if len(addresses) >= 1:
            self.listWidget.setCurrentRow(0)

            for widget in [self.pushButton_open_balance, self.pushButton_pending_transactions,
                           self.pushButton_delete, self.pushButton_export]:
                widget.setEnabled(True)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        if key == int(QtCore.Qt.Key_Return):
            if self.listWidget.hasFocus():
                self.show_balance()
        elif key == int(QtCore.Qt.Key_Escape):
            self.close()

    @QtCore.Slot()
    def show_balance(self, item: AddressListItem = None):
        if not ProjectConstants.wallet_frame.algod_client:
            QtWidgets.QMessageBox.critical(self, "algod settings", "algod settings not valid.")
            return

        if not item:
            item = self.listWidget.currentItem()

        dialog = BalanceWindow(self, item.text())
        dialog.exec_()

    @QtCore.Slot(QtCore.QPoint)
    def show_context_menu(self, pos: QtCore.QPoint):
        if item := self.listWidget.itemAt(pos):
            menu = QtWidgets.QMenu(self)

            menu.addAction("Copy to clipboard", partial(QtGui.QGuiApplication.clipboard().setText, item.text()))

            global_pos = self.listWidget.mapToGlobal(pos)
            menu.exec_(global_pos)

            menu.deleteLater()


class BalanceWindow(QtWidgets.QDialog, Ui_BalanceWindow):
    def __init__(self, parent: QtWidgets.QWidget, address: str):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.address = address

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setupUi(self)

        account_info = ProjectConstants.wallet_frame.algod_client.account_info(self.address)

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
