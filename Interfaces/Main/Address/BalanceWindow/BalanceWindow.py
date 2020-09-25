# Algosdk
from PySide2 import QtWidgets, QtCore

# Local project
from Interfaces.Main.Address.BalanceWindow.Ui_BalanceWindow import Ui_BalanceWindow
from Interfaces.Main.Address.Widgets import BalanceScrollWidget

# Python standard libraries
import locale


class BalanceWindow(QtWidgets.QDialog, Ui_BalanceWindow):
    """
    This class implements the balance window. It displays current balance, pending rewards and assets.
    """
    def __init__(self, parent: QtWidgets.QWidget, account_info: dict):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.account_info = account_info

        self.setupUi(self)

        self.label_Balance.setText(
            str(locale.currency(account_info["amount-without-pending-rewards"], False, True))[:-3] + " microAlgos"
        )
        self.label_Pending.setText(
            str(locale.currency(account_info["pending-rewards"], False, True))[:-3] + " microAlgos"
        )

        for asset in account_info["assets"]:
            self.verticalLayout_assets.addWidget(
                BalanceScrollWidget(
                    "id - " + str(asset["asset-id"]),
                    str(asset["amount"])
                )
            )
        self.verticalLayout_assets.addStretch(1)
