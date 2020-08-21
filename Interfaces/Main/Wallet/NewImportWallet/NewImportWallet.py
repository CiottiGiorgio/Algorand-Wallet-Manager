# PySide2
from PySide2 import QtWidgets, QtCore

# Local project
from Interfaces.Main.Wallet.NewImportWallet.Ui_NewImportWallet import Ui_NewImportWallet


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
