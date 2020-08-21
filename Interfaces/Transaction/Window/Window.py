"""
This file only contains TransactionWindow.
"""


# PySide2
from PySide2 import QtWidgets, QtCore, QtGui

# algosdk
from algosdk import transaction
from algosdk.encoding import is_valid_address
from algosdk.future.transaction import SuggestedParams

# Local project
from misc.Functions import ProjectException, find_main_window
from Interfaces.Transaction.Window.Ui_Window import Ui_TransactionWindow
from Interfaces.Contacts.Window.Window import ContactsWindow


class TransactionWindow(QtWidgets.QDialog, Ui_TransactionWindow):
    """
    This class implements the transaction window.
    """
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.worker = None

        self.setupUi(self)

        # Setup interface
        self.lineEdit_AssetId.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+")))
        self.lineEdit_Amount.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+")))
        self.lineEdit_Fee.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+")))

        # Initial state
        self.comboBox_Sender.addItem("Select a valid Algorand address from the unlocked wallets...")
        self.comboBox_Receiver.addItem("Type in a valid Algorand address or select one...")
        self.comboBox_CloseTo.addItem("Type in a valid Algorand address or select one...")

        wallet_list = find_main_window().wallet_frame.listWidget
        for i in range(wallet_list.count()):
            item = wallet_list.item(i)
            widget = wallet_list.itemWidget(item)

            if widget.wallet.algo_wallet:
                for address in widget.wallet.algo_wallet.list_keys():
                    self.comboBox_Sender.addItem(f"{widget.wallet.info['name']} - {address}", widget.wallet.algo_wallet)
                    self.comboBox_Receiver.addItem(f"Wallet: {widget.wallet.info['name']} - {address}")
                    self.comboBox_CloseTo.addItem(f"Wallet: {widget.wallet.info['name']} - {address}")

        for contact in ContactsWindow.contacts_from_json_file.memory:
            self.comboBox_Receiver.addItem(f"Contact: {contact.name} - {contact.info}")
            self.comboBox_CloseTo.addItem(f"Contact: {contact.name} - {contact.info}")

        # Connections
        self.checkBox_CloseTo.toggled.connect(self.checkbox_close_to)
        self.comboBox_Type.currentIndexChanged.connect(self.combobox_type)
        self.comboBox_AssetMode.currentIndexChanged.connect(self.combobox_asset_mode)
        self.pushButton_SuggestedFee.clicked.connect(self.pushbutton_sf)

        #   We only allow the OK button and the "suggested fee" to be enabled under certain conditions.
        self.comboBox_Sender.currentIndexChanged.connect(self.validate_inputs)
        self.comboBox_Receiver.editTextChanged.connect(self.validate_inputs)
        self.comboBox_CloseTo.editTextChanged.connect(self.validate_inputs)
        self.checkBox_CloseTo.toggled.connect(self.validate_inputs)
        self.comboBox_Type.currentIndexChanged.connect(self.validate_inputs)
        self.lineEdit_AssetId.textChanged.connect(self.validate_inputs)
        self.comboBox_AssetMode.currentIndexChanged.connect(self.validate_inputs)
        self.lineEdit_Amount.textChanged.connect(self.validate_inputs)
        self.lineEdit_Fee.textChanged.connect(self.validate_inputs)

        self.validate_inputs()

    def accept(self):
        try:
            sp = find_main_window().wallet_frame.algod_client.suggested_params()
            wallet = self.comboBox_Sender.currentData()
            s_txn = wallet.sign_transaction(self.get_transaction(sp))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Could not sign transaction", str(e))
            return

        try:
            addr_txn = find_main_window().wallet_frame.algod_client.send_transaction(s_txn)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Could not send transaction", str(e))
            return

        QtGui.QGuiApplication.clipboard().setText(addr_txn)
        QtWidgets.QMessageBox.information(self, "Transaction", "Transaction sent to the node.\n"
                                                               "Transaction address copied into clipboard")
        super().accept()

    @QtCore.Slot()
    def checkbox_close_to(self):
        if self.checkBox_CloseTo.isChecked():
            self.comboBox_CloseTo.setEnabled(True)
        else:
            self.comboBox_CloseTo.setEnabled(False)

    @QtCore.Slot(int)
    def combobox_type(self, new_index: int):
        if new_index == 0:
            for widget in [self.comboBox_AmountUnit]:
                widget.setEnabled(True)
            for widget in [self.lineEdit_AssetId, self.comboBox_AssetMode]:
                widget.setEnabled(False)
            self.comboBox_AssetMode.setCurrentIndex(0)

        elif new_index == 1:
            for widget in [self.comboBox_AmountUnit]:
                widget.setEnabled(False)
            for widget in [self.lineEdit_AssetId, self.comboBox_AssetMode]:
                widget.setEnabled(True)

        else:
            raise ProjectException(
                f"new_index has unexpected value - {new_index}"
            )

    @QtCore.Slot(int)
    def combobox_asset_mode(self, new_index: int):
        if new_index == 0:
            # Transfer
            for widget in [self.comboBox_Receiver, self.checkBox_CloseTo, self.lineEdit_Amount]:
                widget.setEnabled(True)
        elif new_index == 1:
            # Opt-in
            for widget in [self.comboBox_Receiver, self.checkBox_CloseTo, self.lineEdit_Amount]:
                widget.setEnabled(False)
            # This next line also triggers a slot that disabled self.comboBox_CloseTo
            self.checkBox_CloseTo.setChecked(False)
        else:
            raise ProjectException(
                f"new_index has unexpected value - {new_index}"
            )

    @QtCore.Slot()
    def pushbutton_sf(self):
        """
        This method calculates the suggested fee for the whole transaction.

        This method compiles an unsigned transaction with the parameters and then uses .estimate_size() on
        the transaction. Then uses .suggested_params() from algod client to get fee per byte. Then it's easy math.
        """
        try:
            sp = find_main_window().wallet_frame.algod_client.suggested_params()
            temp_txn = self.get_transaction(sp)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Could not load suggested fee", str(e))
            return

        # We do this because we don't want the current fee to change the size of the transaction.
        #  We are going to change this anyway and you can't get a smaller fee than the minimum.
        # Also we are changing the value directly into the instance but we are all grownups it's fine.
        temp_txn.fee = sp.min_fee

        self.comboBox_FeeUnit.setCurrentIndex(0)
        self.lineEdit_Fee.setText(
            str(
                max(sp.min_fee, temp_txn.estimate_size() * sp.fee)
            )
        )

    @QtCore.Slot()
    def validate_inputs(self):
        # TODO Right now when a single widget changes all widgets get checked. Would be better to only update the state
        #  of the changed widget. We would still need to check all states to decide OK button and "suggested fee" button
        #  but at least we wouldn't have to calculate them.
        """
        This method ensures OK button and "suggested fee" button are enabled under the right conditions.

        This method checked the right subset of user inputs based on what type of transaction is taking place.
        """
        states = {
            "sender": self.comboBox_Sender.currentText() != "" and self.comboBox_Sender.currentIndex() != 0,
            "receiver": False,
            "close_to": False,
            "asset_id": self.lineEdit_AssetId.text() != "",
            "amount": self.lineEdit_Amount.text() != "",
            "fee": self.lineEdit_Fee.text() != ""
        }

        # This means: If the selected item is not the first AND (the item is either a valid algorand address OR
        #   is the same as the pre-compiled item)
        receiver_text = self.comboBox_Receiver.currentText()
        if (
                self.comboBox_Receiver.currentIndex() != 0 and (
                    is_valid_address(receiver_text) or
                    self.comboBox_Receiver.itemText(self.comboBox_Receiver.currentIndex()) == receiver_text
                )):
            states["receiver"] = True

        close_to_text = self.comboBox_CloseTo.currentText()
        if (
                self.comboBox_CloseTo.currentIndex() != 0 and (
                    is_valid_address(close_to_text) or
                    self.comboBox_CloseTo.itemText(self.comboBox_CloseTo.currentIndex()) == close_to_text
                )):
            states["close_to"] = True

        # Here we save only the states that are compulsory for the OK button.
        if not self.checkBox_CloseTo.isChecked():
            del states["close_to"]

        if self.comboBox_Type.currentIndex() == 0:
            # Algos transaction
            del states["asset_id"]
        else:
            # Asset transaction
            if self.comboBox_AssetMode.currentIndex() == 0:
                # Transfer
                pass
            elif self.comboBox_AssetMode.currentIndex() == 1:
                # Opt-in
                del states["receiver"]
                del states["amount"]
            elif self.comboBox_AssetMode.currentIndex() == 2:
                # Close
                pass
            else:
                raise ProjectException(
                    f"self.comboBox_type.currentIndex() has unexpected value - {self.comboBox_Type.currentIndex()}"
                )

        ok_button_enabled = all(states.values())
        del states["fee"]
        suggested_fee_button_enabled = all(states.values())

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(
            ok_button_enabled
        )
        self.pushButton_SuggestedFee.setEnabled(
            suggested_fee_button_enabled
        )

    def get_transaction(self, sp: SuggestedParams) -> transaction.Transaction:
        """
        This method returns the transaction the user set up.

        Because this method is used to build a transaction but also to calculate suggested fee we allow an incorrect
        fee parameter in the GUI.
        """
        # TODO we should subclass QComboBox to encapsulate the method that returns the contained algorand address so to
        #  avoid code duplication of the "[-58:]" bit.
        # Here we fill in the fields that are compulsory across the different types of transactions.
        data = {
            "sender": self.comboBox_Sender.currentText()[-58:],
            "receiver": self.comboBox_Receiver.currentText()[-58:],
            "fee": self.get_microalgos_fee() if self.lineEdit_Fee.text() != "" else sp.min_fee,
            "flat_fee": True,
            "first": sp.first,
            "last": sp.last,
            "gh": sp.gh,
            "note": self.textEdit_Note.toPlainText()
        }

        # If the algosdk.transaction raises an error it will be simply propagated and dealt with outside of this
        #  function.
        if self.comboBox_Type.currentIndex() == 0:
            # Algos
            data["amt"] = self.get_microalgos_amount()
            if self.checkBox_CloseTo.isChecked():
                data["close_remainder_to"] = self.comboBox_CloseTo.currentText()[-58:]

            temp_txn = transaction.PaymentTxn(**data)
        elif self.comboBox_Type.currentIndex() == 1:
            # ASA
            if self.checkBox_CloseTo.isChecked():
                data["close_assets_to"] = self.comboBox_CloseTo.currentText()[-58:]
            data["index"] = int(self.lineEdit_AssetId.text())
            if self.comboBox_AssetMode.currentIndex() == 0:
                # Transfer
                data["amt"] = int(self.lineEdit_Amount.text())
            elif self.comboBox_AssetMode.currentIndex() == 1:
                # Opt-in
                data["receiver"] = data["sender"]
                data["amt"] = 0
            elif self.comboBox_AssetMode.currentIndex() == 2:
                # Close
                data["amt"] = int(self.lineEdit_Amount.text())

            temp_txn = transaction.AssetTransferTxn(**data)
        else:
            raise ProjectException(
                f"self.comboBox_type.currentIndex() has unexpected value: {self.comboBox_Type.currentIndex()}"
            )

        return temp_txn

    def get_microalgos_amount(self) -> int:
        """
        This branchless method returns the the amount in microalgos.
        """
        return int(self.lineEdit_Amount.text()) * (1 if self.comboBox_AmountUnit.currentIndex() == 0 else 0
                                                   + 10 ** 3 if self.comboBox_AmountUnit.currentIndex() == 1 else 0
                                                   + 10 ** 6 if self.comboBox_AmountUnit.currentIndex() == 2 else 0)

    def get_microalgos_fee(self) -> int:
        """
        This branchless method returns the fee in microalgos.
        """
        return int(self.lineEdit_Fee.text()) * (1 if self.comboBox_FeeUnit.currentIndex() == 0 else 0
                                                + 10 ** 3 if self.comboBox_FeeUnit.currentIndex() == 1 else 0
                                                + 10 ** 6 if self.comboBox_FeeUnit.currentIndex() == 2 else 0)
