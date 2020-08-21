# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_UnlockWallet.ui'
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


class Ui_UnlockWallet(object):
    def setupUi(self, UnlockWallet):
        if not UnlockWallet.objectName():
            UnlockWallet.setObjectName(u"UnlockWallet")
        UnlockWallet.setWindowModality(Qt.ApplicationModal)
        UnlockWallet.resize(260, 120)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UnlockWallet.sizePolicy().hasHeightForWidth())
        UnlockWallet.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(UnlockWallet)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.label = QLabel(UnlockWallet)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(UnlockWallet)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(240, 0))
        self.lineEdit.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.lineEdit)

        self.widget = LoadingWidget(UnlockWallet)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(UnlockWallet)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(UnlockWallet)
        self.buttonBox.accepted.connect(UnlockWallet.accept)
        self.buttonBox.rejected.connect(UnlockWallet.reject)

        QMetaObject.connectSlotsByName(UnlockWallet)
    # setupUi

    def retranslateUi(self, UnlockWallet):
        UnlockWallet.setWindowTitle(QCoreApplication.translate("", u"Unlock", None))
        self.label.setText(QCoreApplication.translate("", u"Please insert wallet's password", None))
    # retranslateUi

