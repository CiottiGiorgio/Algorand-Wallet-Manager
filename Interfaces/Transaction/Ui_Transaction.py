# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_Transaction.ui'
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


class Ui_TransactionWindow(object):
    def setupUi(self, TransactionWindow):
        if not TransactionWindow.objectName():
            TransactionWindow.setObjectName(u"TransactionWindow")
        TransactionWindow.resize(700, 410)
        TransactionWindow.setMinimumSize(QSize(700, 410))
        TransactionWindow.setMaximumSize(QSize(700, 410))
        self.formLayout = QFormLayout(TransactionWindow)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(15)
        self.label = QLabel(TransactionWindow)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.comboBox_Sender = QComboBox(TransactionWindow)
        self.comboBox_Sender.setObjectName(u"comboBox_sender")
        self.comboBox_Sender.setMinimumSize(QSize(0, 25))
        self.comboBox_Sender.setEditable(False)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox_Sender)

        self.label_2 = QLabel(TransactionWindow)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.comboBox_Receiver = QComboBox(TransactionWindow)
        self.comboBox_Receiver.setObjectName(u"comboBox_receiver")
        self.comboBox_Receiver.setMinimumSize(QSize(0, 25))
        self.comboBox_Receiver.setEditable(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox_Receiver)

        self.label_7 = QLabel(TransactionWindow)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_7)

        self.comboBox_CloseTo = QComboBox(TransactionWindow)
        self.comboBox_CloseTo.setObjectName(u"comboBox_close_to")
        self.comboBox_CloseTo.setEnabled(False)
        self.comboBox_CloseTo.setMinimumSize(QSize(0, 25))
        self.comboBox_CloseTo.setEditable(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox_CloseTo)

        self.label_3 = QLabel(TransactionWindow)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox_Type = QComboBox(TransactionWindow)
        self.comboBox_Type.addItem("")
        self.comboBox_Type.addItem("")
        self.comboBox_Type.setObjectName(u"comboBox_type")

        self.horizontalLayout.addWidget(self.comboBox_Type)

        self.lineEdit_AssetId = QLineEdit(TransactionWindow)
        self.lineEdit_AssetId.setObjectName(u"lineEdit_asset_id")
        self.lineEdit_AssetId.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEdit_AssetId)

        self.comboBox_AssetMode = QComboBox(TransactionWindow)
        self.comboBox_AssetMode.addItem("")
        self.comboBox_AssetMode.addItem("")
        self.comboBox_AssetMode.addItem("")
        self.comboBox_AssetMode.setObjectName(u"comboBox_asset_mode")
        self.comboBox_AssetMode.setEnabled(False)

        self.horizontalLayout.addWidget(self.comboBox_AssetMode)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(3, 1)

        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_5 = QLabel(TransactionWindow)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit_Amount = QLineEdit(TransactionWindow)
        self.lineEdit_Amount.setObjectName(u"lineEdit_amount")
        self.lineEdit_Amount.setMinimumSize(QSize(100, 0))
        self.lineEdit_Amount.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_Amount.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit_Amount)

        self.comboBox_AmountUnit = QComboBox(TransactionWindow)
        self.comboBox_AmountUnit.addItem("")
        self.comboBox_AmountUnit.addItem("")
        self.comboBox_AmountUnit.addItem("")
        self.comboBox_AmountUnit.setObjectName(u"comboBox_amount_unit")

        self.horizontalLayout_3.addWidget(self.comboBox_AmountUnit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_4 = QLabel(TransactionWindow)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_Fee = QLineEdit(TransactionWindow)
        self.lineEdit_Fee.setObjectName(u"lineEdit_fee")
        self.lineEdit_Fee.setMinimumSize(QSize(100, 0))
        self.lineEdit_Fee.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_Fee.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.lineEdit_Fee)

        self.comboBox_FeeUnit = QComboBox(TransactionWindow)
        self.comboBox_FeeUnit.addItem("")
        self.comboBox_FeeUnit.addItem("")
        self.comboBox_FeeUnit.addItem("")
        self.comboBox_FeeUnit.setObjectName(u"comboBox_fee_unit")

        self.horizontalLayout_2.addWidget(self.comboBox_FeeUnit)

        self.pushButton_SuggestedFee = QPushButton(TransactionWindow)
        self.pushButton_SuggestedFee.setObjectName(u"pushButton_sugg_fee")
        self.pushButton_SuggestedFee.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.pushButton_SuggestedFee)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_6 = QLabel(TransactionWindow)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_6)

        self.textEdit_note = QTextEdit(TransactionWindow)
        self.textEdit_note.setObjectName(u"textEdit_note")
        self.textEdit_note.setMaximumSize(QSize(16777215, 70))

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.textEdit_note)

        self.buttonBox = QDialogButtonBox(TransactionWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.buttonBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(7, QFormLayout.SpanningRole, self.verticalSpacer)


        self.retranslateUi(TransactionWindow)
        self.buttonBox.accepted.connect(TransactionWindow.accept)
        self.buttonBox.rejected.connect(TransactionWindow.reject)

        QMetaObject.connectSlotsByName(TransactionWindow)
    # setupUi

    def retranslateUi(self, TransactionWindow):
        TransactionWindow.setWindowTitle(QCoreApplication.translate("TransactionWindow", u"Transaction", None))
        self.label.setText(QCoreApplication.translate("TransactionWindow", u"Sender:", None))
#if QT_CONFIG(tooltip)
        self.comboBox_Sender.setToolTip(QCoreApplication.translate("TransactionWindow", u"Addresses from unlocked wallets will be displayed here.", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("TransactionWindow", u"Receiver:", None))
#if QT_CONFIG(tooltip)
        self.comboBox_Receiver.setToolTip(QCoreApplication.translate("TransactionWindow", u"Addresses from contact list and unlocked wallets will be displayed here.", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("TransactionWindow", u"Close to:", None))
        self.label_3.setText(QCoreApplication.translate("TransactionWindow", u"Type:", None))
        self.comboBox_Type.setItemText(0, QCoreApplication.translate("TransactionWindow", u"Algos", None))
        self.comboBox_Type.setItemText(1, QCoreApplication.translate("TransactionWindow", u"Asset", None))

        self.lineEdit_AssetId.setPlaceholderText(QCoreApplication.translate("TransactionWindow", u"Asset ID", None))
        self.comboBox_AssetMode.setItemText(0, QCoreApplication.translate("TransactionWindow", u"Transfer", None))
        self.comboBox_AssetMode.setItemText(1, QCoreApplication.translate("TransactionWindow", u"Opt-in", None))
        self.comboBox_AssetMode.setItemText(2, QCoreApplication.translate("TransactionWindow", u"Close to", None))

        self.label_5.setText(QCoreApplication.translate("TransactionWindow", u"Amount:", None))
        self.comboBox_AmountUnit.setItemText(0, QCoreApplication.translate("TransactionWindow", u"microAlgos", None))
        self.comboBox_AmountUnit.setItemText(1, QCoreApplication.translate("TransactionWindow", u"milliAlgos", None))
        self.comboBox_AmountUnit.setItemText(2, QCoreApplication.translate("TransactionWindow", u"Algos", None))

        self.label_4.setText(QCoreApplication.translate("TransactionWindow", u"Fee:", None))
        self.comboBox_FeeUnit.setItemText(0, QCoreApplication.translate("TransactionWindow", u"microAlgos", None))
        self.comboBox_FeeUnit.setItemText(1, QCoreApplication.translate("TransactionWindow", u"milliAlgos", None))
        self.comboBox_FeeUnit.setItemText(2, QCoreApplication.translate("TransactionWindow", u"Algos", None))

#if QT_CONFIG(tooltip)
        self.pushButton_SuggestedFee.setToolTip(QCoreApplication.translate("TransactionWindow", u"Fill all parameters to calculate the suggested fee for this transaction.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_SuggestedFee.setText(QCoreApplication.translate("TransactionWindow", u"Suggested fee", None))
        self.label_6.setText(QCoreApplication.translate("TransactionWindow", u"Note:", None))
    # retranslateUi

