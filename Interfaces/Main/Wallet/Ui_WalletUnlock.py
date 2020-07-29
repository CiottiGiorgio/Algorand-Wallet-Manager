# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_WalletUnlock.ui'
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


class Ui_WalletUnlock(object):
    def setupUi(self, WalletUnlock):
        if not WalletUnlock.objectName():
            WalletUnlock.setObjectName(u"WalletUnlock")
        WalletUnlock.setWindowModality(Qt.ApplicationModal)
        WalletUnlock.resize(260, 120)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WalletUnlock.sizePolicy().hasHeightForWidth())
        WalletUnlock.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(WalletUnlock)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.label = QLabel(WalletUnlock)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(WalletUnlock)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(240, 0))
        self.lineEdit.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.lineEdit)

        self.widget = LoadingWidget(WalletUnlock)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(WalletUnlock)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(WalletUnlock)
        self.buttonBox.accepted.connect(WalletUnlock.accept)
        self.buttonBox.rejected.connect(WalletUnlock.reject)

        QMetaObject.connectSlotsByName(WalletUnlock)
    # setupUi

    def retranslateUi(self, WalletUnlock):
        WalletUnlock.setWindowTitle(QCoreApplication.translate("WalletUnlock", u"Unlock", None))
        self.label.setText(QCoreApplication.translate("WalletUnlock", u"Please insert wallet's password", None))
    # retranslateUi

