# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_NewImportWallet.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_NewImportWallet(object):
    def setupUi(self, NewImportWallet):
        if not NewImportWallet.objectName():
            NewImportWallet.setObjectName(u"NewImportWallet")
        NewImportWallet.resize(660, 280)
        NewImportWallet.setMinimumSize(QSize(660, 280))
        NewImportWallet.setMaximumSize(QSize(660, 280))
        self.formLayout = QFormLayout(NewImportWallet)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(NewImportWallet)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit_Name = QLineEdit(NewImportWallet)
        self.lineEdit_Name.setObjectName(u"lineEdit_Name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_Name)

        self.label_2 = QLabel(NewImportWallet)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_Password = QLineEdit(NewImportWallet)
        self.lineEdit_Password.setObjectName(u"lineEdit_Password")
        self.lineEdit_Password.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_Password)

        self.buttonBox = QDialogButtonBox(NewImportWallet)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.buttonBox)

        self.plainTextEdit_MDK = QPlainTextEdit(NewImportWallet)
        self.plainTextEdit_MDK.setObjectName(u"plainTextEdit_MDK")
        self.plainTextEdit_MDK.setMaximumSize(QSize(16777215, 85))

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.plainTextEdit_MDK)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = QLabel(NewImportWallet)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.label_3 = QLabel(NewImportWallet)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)


        self.formLayout.setLayout(3, QFormLayout.LabelRole, self.verticalLayout)

        self.label_5 = QLabel(NewImportWallet)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.lineEdit_Password2 = QLineEdit(NewImportWallet)
        self.lineEdit_Password2.setObjectName(u"lineEdit_Password2")
        self.lineEdit_Password2.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_Password2)

        QWidget.setTabOrder(self.lineEdit_Name, self.lineEdit_Password)
        QWidget.setTabOrder(self.lineEdit_Password, self.lineEdit_Password2)
        QWidget.setTabOrder(self.lineEdit_Password2, self.plainTextEdit_MDK)

        self.retranslateUi(NewImportWallet)
        self.buttonBox.accepted.connect(NewImportWallet.accept)
        self.buttonBox.rejected.connect(NewImportWallet.reject)

        QMetaObject.connectSlotsByName(NewImportWallet)
    # setupUi

    def retranslateUi(self, NewImportWallet):
        NewImportWallet.setWindowTitle(QCoreApplication.translate("NewImportWallet", u"New/Import wallet", None))
        self.label.setText(QCoreApplication.translate("NewImportWallet", u"Name:", None))
        self.label_2.setText(QCoreApplication.translate("NewImportWallet", u"Password:", None))
        self.label_4.setText(QCoreApplication.translate("NewImportWallet", u"Mnemonic master derivation key:", None))
        self.label_3.setText(QCoreApplication.translate("NewImportWallet", u"Only fill this input if you are\n"
"importing a wallet", None))
        self.label_5.setText(QCoreApplication.translate("NewImportWallet", u"Enter your password again:", None))
    # retranslateUi

