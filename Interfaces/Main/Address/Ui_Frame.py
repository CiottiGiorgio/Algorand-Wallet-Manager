# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_Frame.ui'
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

from misc.Widgets import CustomListWidget


class Ui_AddressFrame(object):
    def setupUi(self, AddressFrame):
        if not AddressFrame.objectName():
            AddressFrame.setObjectName(u"AddressFrame")
        AddressFrame.resize(737, 353)
        self.horizontalLayout = QHBoxLayout(AddressFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listWidget = CustomListWidget(AddressFrame)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)

        self.horizontalLayout.addWidget(self.listWidget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_Return = QPushButton(AddressFrame)
        self.pushButton_Return.setObjectName(u"pushButton_Return")

        self.verticalLayout.addWidget(self.pushButton_Return)

        self.pushButton_Balance = QPushButton(AddressFrame)
        self.pushButton_Balance.setObjectName(u"pushButton_Balance")
        self.pushButton_Balance.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButton_Balance)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pushButton_New = QPushButton(AddressFrame)
        self.pushButton_New.setObjectName(u"pushButton_New")

        self.verticalLayout.addWidget(self.pushButton_New)

        self.pushButton_ForgetClose = QPushButton(AddressFrame)
        self.pushButton_ForgetClose.setObjectName(u"pushButton_ForgetClose")
        self.pushButton_ForgetClose.setEnabled(False)
        self.pushButton_ForgetClose.setCheckable(False)

        self.verticalLayout.addWidget(self.pushButton_ForgetClose)

        self.pushButton_Import = QPushButton(AddressFrame)
        self.pushButton_Import.setObjectName(u"pushButton_Import")

        self.verticalLayout.addWidget(self.pushButton_Import)

        self.pushButton_Export = QPushButton(AddressFrame)
        self.pushButton_Export.setObjectName(u"pushButton_Export")
        self.pushButton_Export.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButton_Export)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(AddressFrame)

        QMetaObject.connectSlotsByName(AddressFrame)
    # setupUi

    def retranslateUi(self, AddressFrame):
        AddressFrame.setWindowTitle(QCoreApplication.translate("AddressFrame", u"Frame", None))
        self.pushButton_Return.setText(QCoreApplication.translate("AddressFrame", u"Return", None))
        self.pushButton_Balance.setText(QCoreApplication.translate("AddressFrame", u"Open\n"
"Balance", None))
        self.pushButton_New.setText(QCoreApplication.translate("AddressFrame", u"New", None))
        self.pushButton_ForgetClose.setText(QCoreApplication.translate("AddressFrame", u"Forget/Close", None))
        self.pushButton_Import.setText(QCoreApplication.translate("AddressFrame", u"Import", None))
        self.pushButton_Export.setText(QCoreApplication.translate("AddressFrame", u"Export", None))
    # retranslateUi

