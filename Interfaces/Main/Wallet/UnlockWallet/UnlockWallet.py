# PySide2
from PySide2 import QtWidgets, QtCore, QtGui

# Algorand
from algosdk.wallet import Wallet as AlgosdkWallet

# Local project
from misc.Entities import Wallet
from misc.Functions import find_main_window
from Interfaces.Main.Wallet.UnlockWallet.Ui_UnlockWallet import Ui_UnlockWallet

# Python standard libraries
from functools import partial


class UnlockWallet(QtWidgets.QDialog, Ui_UnlockWallet):
    def __init__(self, parent: QtWidgets.QWidget, wallet: Wallet):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wallet = wallet
        self.return_value = None

        self.worker = None

        self.setupUi(self)

        self.widget.setVisible(False)

    def closeEvent(self, arg__1: QtGui.QCloseEvent):
        if self.worker:
            self.worker.signals.success.disconnect()
            self.worker.signals.error.disconnect()
        arg__1.accept()

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
