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
from Interfaces.Transaction.Ui_Transaction import Ui_TransactionWindow
from Interfaces.Contacts.Window import ContactsWindow


class TransactionWindow(QtWidgets.QDialog, Ui_TransactionWindow):
    """
    This class implements the transaction window.
    """
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.worker = None
        self.sender_list = list()

        self.setupUi(self)

        # Setup interface
        self.lineEdit_AssetId.setValidator(QtGui.QIntValidator(1, 999999))
        self.lineEdit_Amount.setValidator(QtGui.QIntValidator(0, 999999))
        self.lineEdit_Fee.setValidator(QtGui.QIntValidator(1, 999999))

        # Initial state
        wallet_list = find_main_window().wallet_frame.listWidget
        for i in range(wallet_list.count()):
            item = wallet_list.item(i)
            widget = wallet_list.itemWidget(item)

            if widget.wallet.algo_wallet:
                for address in widget.wallet.algo_wallet.list_keys():
                    # FIXME This is SUPER bad. Basically we rely on the position of the item to retrieve the wallet
                    self.sender_list.append(widget.wallet.algo_wallet)
                    self.comboBox_Sender.addItem(f"Wallet: {widget.wallet.info['name']} - {address}")
                    self.comboBox_Receiver.addItem(f"Wallet: {widget.wallet.info['name']} - {address}")
                    self.comboBox_CloseTo.addItem(f"Wallet: {widget.wallet.info['name']} - {address}")

        for contact in ContactsWindow.contacts_from_json_file.memory:
            self.comboBox_Receiver.addItem(f"Contact: {contact.name} - {contact.info}")

        # Connections
        self.comboBox_Type.currentIndexChanged.connect(self.combobox_type)
        self.comboBox_AssetMode.currentIndexChanged.connect(self.combobox_asset_mode)
        self.pushButton_SuggestedFee.clicked.connect(self.pushbutton_sf)

        #   We only allow the OK button and the "suggested fee" to be enabled under certain conditions.
        self.comboBox_Sender.currentIndexChanged.connect(self.validate_inputs)
        self.comboBox_Receiver.editTextChanged.connect(self.validate_inputs)
        self.comboBox_Type.currentIndexChanged.connect(self.validate_inputs)
        self.lineEdit_AssetId.textChanged.connect(self.validate_inputs)
        self.comboBox_AssetMode.currentIndexChanged.connect(self.validate_inputs)
        self.lineEdit_Amount.textChanged.connect(self.validate_inputs)
        self.lineEdit_Fee.textChanged.connect(self.validate_inputs)

        self.validate_inputs()

    def accept(self):
        try:
            sp = find_main_window().wallet_frame.algod_client.suggested_params()
            s_txn = self.sender_list[self.comboBox_Sender.currentIndex()].sign_transaction(self.get_transaction(sp))
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
        enables, disables = list(), list()

        if new_index == 0:
            enables.append(self.comboBox_Receiver)
            enables.append(self.lineEdit_Amount)
            disables.append(self.comboBox_CloseTo)
        elif new_index == 1:
            # Opt-in
            disables.append(self.comboBox_Receiver)
            disables.append(self.comboBox_CloseTo)
            disables.append(self.lineEdit_Amount)
        elif new_index == 2:
            # Close
            enables.append(self.comboBox_Receiver)
            enables.append(self.comboBox_CloseTo)
            enables.append(self.lineEdit_Amount)
        else:
            raise ProjectException(
                f"new_index has unexpected value - {new_index}"
            )

        for widget in enables:
            widget.setEnabled(True)

        for widget in disables:
            widget.setEnabled(False)

    @QtCore.Slot()
    def pushbutton_sf(self):
        """
        This method calculates the suggested fee for the whole transaction.

        This method compiles an unsigned transaction with the parameters and then uses .estimate_size() on
        the transaction. Then uses .suggested_params() from algod client to get fee per byte. Then it's easy math.
        """
        try:
            sp = find_main_window().wallet_frame.algod_client.suggested_params()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Could not load suggested fee", str(e))
            return

        temp_txn = self.get_transaction(sp)
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
        """
        This method ensures that the correct subset of user inputs has a valid input.

        The subset changes based on the type of transaction the user is choosing.
        """
        states = {
            "sender_state": self.comboBox_Sender.currentText() != "",
            "receiver_state": False,
            "close_to_state": False,
            "asset_id_state": False,
            "amount_state": self.lineEdit_Amount.text() != "",
            "fee_state": self.lineEdit_Fee.text() != ""
        }

        receiver_text = self.comboBox_Receiver.currentText()
        # This means: If the user input a valid algorand address or if the selected item has not been messed with.
        if (is_valid_address(receiver_text) or
                self.comboBox_Receiver.itemText(self.comboBox_Receiver.currentIndex()) == receiver_text):
            states["receiver_state"] = True

        close_to_text = self.comboBox_CloseTo.currentText()
        # This means: If the user input a valid algorand address or if the selected item has not been messed with.
        if (is_valid_address(close_to_text) or
                self.comboBox_CloseTo.itemText(self.comboBox_CloseTo.currentIndex()) == close_to_text):
            states["close_to_state"] = True

        asset_id_text = self.lineEdit_AssetId.text()
        if asset_id_text != "":
            # At this point we are guaranteed to have an integer between 0 and 999999 because of QIntValidator.
            if int(asset_id_text) < 999999999:  # TODO Make sure what is the range for an ASA ID.
                states["asset_id_state"] = True

        # Here we save only the states that are compulsory for the OK button.
        if self.comboBox_Type.currentIndex() == 0:
            # Algos transaction
            del states["asset_id_state"]
            del states["close_to_state"]
        else:
            # Asset transaction
            if self.comboBox_AssetMode.currentIndex() == 0:
                # Transfer
                del states["close_to_state"]
            elif self.comboBox_AssetMode.currentIndex() == 1:
                # Opt-in
                del states["receiver_state"]
                del states["close_to_state"]
                del states["amount_state"]
            elif self.comboBox_AssetMode.currentIndex() == 2:
                # Close
                pass
            else:
                raise ProjectException(
                    f"self.comboBox_type.currentIndex() has unexpected value - {self.comboBox_Type.currentIndex()}"
                )

        ok_button_enabled = all(states.values())
        del states["fee_state"]
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
        data = {
            "sender": self.comboBox_Sender.currentText().split(" - ")[1],
            "receiver": self.comboBox_Receiver.currentText().split(" - ")[1],
            "fee": self.get_microalgos_fee() if self.lineEdit_Fee.text() != "" else sp.min_fee,
            "flat_fee": True,
            "first": sp.first,
            "last": sp.last,
            "gh": sp.gh,
            "note": self.textEdit_note.toPlainText()
        }
        if self.comboBox_Type.currentIndex() == 0:
            # This returns the whole string if no match with separator is found
            data["amt"] = self.get_microalgos_amount()
            temp_txn = transaction.PaymentTxn(**data)
        elif self.comboBox_Type.currentIndex() == 1:
            data["index"] = int(self.lineEdit_AssetId.text())
            if self.comboBox_AssetMode.currentIndex() == 0:
                data["amt"] = int(self.lineEdit_Amount.text())
            elif self.comboBox_AssetMode.currentIndex() == 1:
                data["receiver"] = data["sender"]
                data["amt"] = 0
            elif self.comboBox_AssetMode.currentIndex() == 2:
                data["amt"] = int(self.lineEdit_Amount.text())
                data["close_assets_to"] = self.comboBox_CloseTo.currentText().split(" - ")[1]

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
