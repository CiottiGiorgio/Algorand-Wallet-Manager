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

from misc.Widgets import LoadingWidget


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

        self.comboBox_sender = QComboBox(TransactionWindow)
        self.comboBox_sender.setObjectName(u"comboBox_sender")
        self.comboBox_sender.setMinimumSize(QSize(0, 25))
        self.comboBox_sender.setEditable(False)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox_sender)

        self.label_2 = QLabel(TransactionWindow)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.comboBox_receiver = QComboBox(TransactionWindow)
        self.comboBox_receiver.setObjectName(u"comboBox_receiver")
        self.comboBox_receiver.setMinimumSize(QSize(0, 25))
        self.comboBox_receiver.setEditable(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox_receiver)

        self.label_3 = QLabel(TransactionWindow)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox_type = QComboBox(TransactionWindow)
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.setObjectName(u"comboBox_type")

        self.horizontalLayout.addWidget(self.comboBox_type)

        self.lineEdit_asset_id = QLineEdit(TransactionWindow)
        self.lineEdit_asset_id.setObjectName(u"lineEdit_asset_id")
        self.lineEdit_asset_id.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEdit_asset_id)

        self.checkBox_opt_in = QCheckBox(TransactionWindow)
        self.checkBox_opt_in.setObjectName(u"checkBox_opt_in")
        self.checkBox_opt_in.setEnabled(False)

        self.horizontalLayout.addWidget(self.checkBox_opt_in)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_5 = QLabel(TransactionWindow)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit_amount = QLineEdit(TransactionWindow)
        self.lineEdit_amount.setObjectName(u"lineEdit_amount")
        self.lineEdit_amount.setMinimumSize(QSize(100, 0))
        self.lineEdit_amount.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_amount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit_amount)

        self.comboBox_amount_unit = QComboBox(TransactionWindow)
        self.comboBox_amount_unit.addItem("")
        self.comboBox_amount_unit.addItem("")
        self.comboBox_amount_unit.addItem("")
        self.comboBox_amount_unit.setObjectName(u"comboBox_amount_unit")

        self.horizontalLayout_3.addWidget(self.comboBox_amount_unit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_4 = QLabel(TransactionWindow)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_fee = QLineEdit(TransactionWindow)
        self.lineEdit_fee.setObjectName(u"lineEdit_fee")
        self.lineEdit_fee.setMinimumSize(QSize(100, 0))
        self.lineEdit_fee.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_fee.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.lineEdit_fee)

        self.comboBox_fee_unit = QComboBox(TransactionWindow)
        self.comboBox_fee_unit.addItem("")
        self.comboBox_fee_unit.addItem("")
        self.comboBox_fee_unit.addItem("")
        self.comboBox_fee_unit.setObjectName(u"comboBox_fee_unit")

        self.horizontalLayout_2.addWidget(self.comboBox_fee_unit)

        self.pushButton_sugg_fee = QPushButton(TransactionWindow)
        self.pushButton_sugg_fee.setObjectName(u"pushButton_sugg_fee")
        self.pushButton_sugg_fee.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.pushButton_sugg_fee)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_6 = QLabel(TransactionWindow)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.textEdit_note = QTextEdit(TransactionWindow)
        self.textEdit_note.setObjectName(u"textEdit_note")
        self.textEdit_note.setMaximumSize(QSize(16777215, 70))

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.textEdit_note)

        self.buttonBox = QDialogButtonBox(TransactionWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.buttonBox)

        self.widget = LoadingWidget(TransactionWindow)
        self.widget.setObjectName(u"widget")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.widget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(6, QFormLayout.LabelRole, self.verticalSpacer)


        self.retranslateUi(TransactionWindow)
        self.buttonBox.accepted.connect(TransactionWindow.accept)
        self.buttonBox.rejected.connect(TransactionWindow.reject)

        QMetaObject.connectSlotsByName(TransactionWindow)
    # setupUi

    def retranslateUi(self, TransactionWindow):
        TransactionWindow.setWindowTitle(QCoreApplication.translate("TransactionWindow", u"Transaction", None))
        self.label.setText(QCoreApplication.translate("TransactionWindow", u"Sender:", None))
#if QT_CONFIG(tooltip)
        self.comboBox_sender.setToolTip(QCoreApplication.translate("TransactionWindow", u"Addresses from unlocked wallets will be displayed here.", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("TransactionWindow", u"Receiver:", None))
#if QT_CONFIG(tooltip)
        self.comboBox_receiver.setToolTip(QCoreApplication.translate("TransactionWindow", u"Addresses from contact list and unlocked wallets will be displayed here.", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("TransactionWindow", u"Type:", None))
        self.comboBox_type.setItemText(0, QCoreApplication.translate("TransactionWindow", u"Algos", None))
        self.comboBox_type.setItemText(1, QCoreApplication.translate("TransactionWindow", u"Asset", None))

        self.lineEdit_asset_id.setPlaceholderText(QCoreApplication.translate("TransactionWindow", u"Asset ID", None))
        self.checkBox_opt_in.setText(QCoreApplication.translate("TransactionWindow", u"Opt-in", None))
        self.label_5.setText(QCoreApplication.translate("TransactionWindow", u"Amount:", None))
        self.comboBox_amount_unit.setItemText(0, QCoreApplication.translate("TransactionWindow", u"microAlgos", None))
        self.comboBox_amount_unit.setItemText(1, QCoreApplication.translate("TransactionWindow", u"milliAlgos", None))
        self.comboBox_amount_unit.setItemText(2, QCoreApplication.translate("TransactionWindow", u"Algos", None))

        self.label_4.setText(QCoreApplication.translate("TransactionWindow", u"Fee:", None))
        self.comboBox_fee_unit.setItemText(0, QCoreApplication.translate("TransactionWindow", u"microAlgos", None))
        self.comboBox_fee_unit.setItemText(1, QCoreApplication.translate("TransactionWindow", u"milliAlgos", None))
        self.comboBox_fee_unit.setItemText(2, QCoreApplication.translate("TransactionWindow", u"Algos", None))

#if QT_CONFIG(tooltip)
        self.pushButton_sugg_fee.setToolTip(QCoreApplication.translate("TransactionWindow", u"Fill all parameters to calculate the suggested fee for this transaction.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_sugg_fee.setText(QCoreApplication.translate("TransactionWindow", u"Suggested fee", None))
        self.label_6.setText(QCoreApplication.translate("TransactionWindow", u"Note:", None))
    # retranslateUi

