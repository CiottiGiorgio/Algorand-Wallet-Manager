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
from misc.Functions import find_main_window
from Interfaces.Transaction.Ui_Transaction import Ui_TransactionWindow
from Interfaces.Contacts.Window import ContactsWindow

# Python standard libraries
from sys import stderr


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
        self.lineEdit_asset_id.setValidator(QtGui.QIntValidator(1, 999999))
        self.lineEdit_amount.setValidator(QtGui.QIntValidator(0, 999999))
        self.lineEdit_fee.setValidator(QtGui.QIntValidator(1, 999999))
        self.widget.setVisible(False)

        # Initial state
        wallet_list = find_main_window().wallet_frame.listWidget
        for i in range(wallet_list.count()):
            item = wallet_list.item(i)
            widget = wallet_list.itemWidget(item)

            if widget.wallet.algo_wallet:
                for address in widget.wallet.algo_wallet.list_keys():
                    # This is SUPER bad. Basically we rely on the position of the item to retrieve the wallet
                    self.sender_list.append(widget.wallet.algo_wallet)
                    self.comboBox_sender.addItem(f"{widget.wallet.info['name']} - {address}")
                    self.comboBox_receiver.addItem(f"Wallet: {widget.wallet.info['name']} - {address}")

        for contact in ContactsWindow.contacts_from_json_file.memory:
            self.comboBox_receiver.addItem(f"Contact: {contact.name} - {contact.info}")

        # Connections
        self.comboBox_type.currentIndexChanged.connect(self.combobox_type)
        self.checkBox_opt_in.stateChanged.connect(self.checkbox_opt_in)
        self.pushButton_sugg_fee.clicked.connect(self.pushbutton_sf)

        #   We only allow the OK button and the "suggested fee" to be enabled under certain conditions.
        self.comboBox_sender.currentIndexChanged.connect(self.validate_inputs)
        self.comboBox_receiver.editTextChanged.connect(self.validate_inputs)
        self.comboBox_type.currentIndexChanged.connect(self.validate_inputs)
        self.lineEdit_asset_id.textChanged.connect(self.validate_inputs)
        self.checkBox_opt_in.toggled.connect(self.validate_inputs)
        self.lineEdit_amount.textChanged.connect(self.validate_inputs)
        self.lineEdit_fee.textChanged.connect(self.validate_inputs)

        self.validate_inputs()

    def accept(self):
        try:
            sp = find_main_window().wallet_frame.algod_client.suggested_params()
            s_txn = self.sender_list[self.comboBox_sender.currentIndex()].sign_transaction(self.get_transaction(sp))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Could not sign transaction", str(e))
            return

        try:
            find_main_window().wallet_frame.algod_client.send_transaction(s_txn)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Could not send transaction", str(e))
            return

        QtWidgets.QMessageBox.information(self, "Transaction", "Transaction successful")
        super().accept()

    @QtCore.Slot(int)
    def combobox_type(self, new_index: int):
        if new_index == 0:
            for widget in [self.comboBox_amount_unit]:
                widget.setEnabled(True)
            for widget in [self.lineEdit_asset_id, self.checkBox_opt_in]:
                widget.setEnabled(False)
            self.checkBox_opt_in.setChecked(False)

        elif new_index == 1:
            for widget in [self.comboBox_amount_unit]:
                widget.setEnabled(False)
            for widget in [self.lineEdit_asset_id, self.checkBox_opt_in]:
                widget.setEnabled(True)

        else:
            print("This line should be impossible to reach", file=stderr)

    @QtCore.Slot(QtCore.Qt.CheckState)
    def checkbox_opt_in(self, new_state: QtCore.Qt.CheckState):
        if new_state == QtCore.Qt.CheckState.Checked:
            for widget in [self.lineEdit_amount, self.comboBox_receiver]:
                widget.setEnabled(False)

        elif new_state == QtCore.Qt.CheckState.Unchecked:
            for widget in [self.lineEdit_amount, self.comboBox_receiver]:
                widget.setEnabled(True)

        else:
            print("This line should be impossible to reach", file=stderr)

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

        self.comboBox_fee_unit.setCurrentIndex(0)
        self.lineEdit_fee.setText(
            str(
                max(temp_txn.estimate_size() * sp.fee, 1000)
            )
        )

    @QtCore.Slot()
    def validate_inputs(self):
        states = {
            "sender_state": self.comboBox_sender.currentText() != "",
            "receiver_state": False,
            "asset_id_state": False,
            "amount_state": self.lineEdit_amount.text() != "",
            "fee_state": self.lineEdit_fee.text() != ""
        }

        receiver_text = self.comboBox_receiver.currentText()
        # This means: If the user input a valid algorand address or if the selected item has not been messed with.
        if (is_valid_address(receiver_text) or
                self.comboBox_receiver.itemText(self.comboBox_receiver.currentIndex()) == receiver_text):
            states["receiver_state"] = True

        asset_id_text = self.lineEdit_asset_id.text()
        if asset_id_text != "":
            # At this point we are guaranteed to have an integer between 0 and 999999 because of QIntValidator.
            if int(asset_id_text) < 999999:  # TODO Make sure what is the range for an ASA ID.
                states["asset_id_state"] = True

        if self.comboBox_type.currentIndex() == 0:
            # Payment transaction
            del states["asset_id_state"]
            ok_button_enabled = all(states.values())
        else:
            if self.checkBox_opt_in.isChecked():
                # Asset opt-in transaction
                del states["receiver_state"]
                del states["amount_state"]
                ok_button_enabled = all(states.values())
            else:
                # Asset transaction
                ok_button_enabled = all(states.values())

        del states["fee_state"]
        sugg_fee_button_enabled = all(states.values())

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(
            ok_button_enabled
        )
        self.pushButton_sugg_fee.setEnabled(
            sugg_fee_button_enabled
        )

    def get_transaction(self, sp: SuggestedParams) -> transaction.Transaction:
        """
        This method returns the transaction the user set up.

        Because this method is used to build a transaction but also to calculate suggested fee we allow an incorrect
        fee parameter in the GUI.
        """
        data = {
            "sender": self.comboBox_sender.currentText().split(" - ")[1],
            "fee": self.get_microalgos_fee() if self.lineEdit_fee.text() != "" else sp.min_fee,
            "flat_fee": True,
            "first": sp.first,
            "last": sp.last,
            "gh": sp.gh,
            "note": self.textEdit_note.toPlainText()
        }
        if self.comboBox_type.currentIndex() == 0:
            # This returns the whole string if no match with separator is found
            data["receiver"] = self.comboBox_receiver.currentText().split(" - ")[1]
            data["amt"] = self.get_microalgos_amount()
            temp_txn = transaction.PaymentTxn(**data)
        else:
            data["index"] = self.lineEdit_asset_id.text()
            if self.checkBox_opt_in.isChecked():
                data["receiver"] = data["sender"]
                data["amt"] = 0
                temp_txn = transaction.AssetTransferTxn(**data)
            else:
                data["receiver"] = self.comboBox_receiver.currentText().split(" - ")[1]
                data["amt"] = self.get_microalgos_amount()
                temp_txn = transaction.AssetTransferTxn(**data)
        return temp_txn

    def get_microalgos_amount(self) -> int:
        """
        This branchless method return the the amount in microalgos.
        """
        return int(self.lineEdit_amount.text()) * (1 if self.comboBox_amount_unit.currentIndex() == 0 else 0
                                                   + 10**3 if self.comboBox_amount_unit.currentIndex() == 1 else 0
                                                   + 10**6 if self.comboBox_amount_unit.currentIndex() == 2 else 0)

    def get_microalgos_fee(self) -> int:
        """
        This branchless method return the fee in microalgos.
        """
        return int(self.lineEdit_fee.text()) * (1 if self.comboBox_fee_unit.currentIndex() == 0 else 0
                                                + 10**3 if self.comboBox_fee_unit.currentIndex() == 1 else 0
                                                + 10**6 if self.comboBox_fee_unit.currentIndex() == 2 else 0)
