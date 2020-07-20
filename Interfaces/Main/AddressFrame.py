"""
This file contains AddressFrame which is a QFrame displayed as a result of an opened wallet.
"""

# PySide2
from PySide2 import QtWidgets, QtCore, QtGui

# algosdk
from algosdk import transaction

# Local project
from misc import Constants as ProjectConstants
from misc.Entities import Wallet
from Interfaces.Main.AddressWidgets import BalanceScrollWidget

# Python standard libraries
from functools import partial


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
        self.list_address.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
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
        self.list_address.customContextMenuRequested.connect(self.show_context_menu)

        # Worker
        # We load the addresses in a non threaded way for now.
        addresses = self.wallet.algo_wallet.list_keys()

        for address in addresses:
            self.list_address.addItem(address)

        if len(addresses) >= 1:
            self.list_address.setCurrentRow(0)

            for widget in [self.button_balance, self.button_export, self.button_delete]:
                widget.setEnabled(True)

    @QtCore.Slot()
    def show_balance(self):
        item = self.list_address.currentItem()

        dialog = BalanceWindow(self, item.text())
        dialog.exec_()

    @QtCore.Slot(QtCore.QPoint)
    def show_context_menu(self, pos: QtCore.QPoint):
        if item := self.list_address.itemAt(pos):
            menu = QtWidgets.QMenu(self)

            menu.addAction("Copy", partial(QtGui.QGuiApplication.clipboard().setText, item.text()))

            global_pos = self.list_address.mapToGlobal(pos)
            menu.exec_(global_pos)

            menu.deleteLater()


class BalanceWindow(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget, address: str):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.address = address

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Setup interface
        self.setWindowTitle("Algos & Assets")

        self.setFixedSize(350, 400)

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

        # Initial state
        new_asset_layout = QtWidgets.QHBoxLayout()
        assets_layout.addLayout(new_asset_layout)

        self.line_asset_id = QtWidgets.QLineEdit()
        self.line_asset_id.setPlaceholderText("id of the asset you want to opt-in")
        # TODO absolutely check what is the range of an ASA
        self.line_asset_id.setValidator(QtGui.QIntValidator())
        new_asset_layout.addWidget(self.line_asset_id)

        self.button_opt_in = QtWidgets.QPushButton("Add")
        new_asset_layout.addWidget(self.button_opt_in)

        new_asset_layout.setStretch(0, 1)

        # Connections
        self.line_asset_id.textChanged.connect(self.validate_id_line)
        self.button_opt_in.clicked.connect(self.button_op_in_clicked)

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

    def validate_id_line(self, new_text: str):
        self.button_opt_in.setEnabled(
            new_text != ""
        )

    def button_op_in_clicked(self):
        try:
            sp = ProjectConstants.wallet_frame.algod_client.suggested_params()
            txn = transaction.AssetTransferTxn(
                self.address,
                sp.min_fee,
                sp.first,
                sp.last,
                sp.gh,
                self.address,
                0,
                int(self.line_asset_id.text())
            )
            s_txn = self.parent().wallet.algo_wallet.sign_transaction(txn)
            ProjectConstants.wallet_frame.algod_client.send_transaction(s_txn)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Could not opt-in", str(e))
        else:
            QtWidgets.QMessageBox.information(
                self,
                "Information",
                "Keep in mind that opting in could take a few seconds\nfor the transaction to be processed"
            )
