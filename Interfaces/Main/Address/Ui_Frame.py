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
        self.pushButton_return = QPushButton(AddressFrame)
        self.pushButton_return.setObjectName(u"pushButton_return")

        self.verticalLayout.addWidget(self.pushButton_return)

        self.pushButton_open_balance = QPushButton(AddressFrame)
        self.pushButton_open_balance.setObjectName(u"pushButton_open_balance")
        self.pushButton_open_balance.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButton_open_balance)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pushButton_new = QPushButton(AddressFrame)
        self.pushButton_new.setObjectName(u"pushButton_new")

        self.verticalLayout.addWidget(self.pushButton_new)

        self.pushButton_delete = QPushButton(AddressFrame)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        self.pushButton_delete.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButton_delete)

        self.pushButton_import = QPushButton(AddressFrame)
        self.pushButton_import.setObjectName(u"pushButton_import")

        self.verticalLayout.addWidget(self.pushButton_import)

        self.pushButton_export = QPushButton(AddressFrame)
        self.pushButton_export.setObjectName(u"pushButton_export")
        self.pushButton_export.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButton_export)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(AddressFrame)

        QMetaObject.connectSlotsByName(AddressFrame)
    # setupUi

    def retranslateUi(self, AddressFrame):
        AddressFrame.setWindowTitle(QCoreApplication.translate("AddressFrame", u"Frame", None))
        self.pushButton_return.setText(QCoreApplication.translate("AddressFrame", u"Return", None))
        self.pushButton_open_balance.setText(QCoreApplication.translate("AddressFrame", u"Open\n"
"Balance", None))
        self.pushButton_new.setText(QCoreApplication.translate("AddressFrame", u"New", None))
        self.pushButton_delete.setText(QCoreApplication.translate("AddressFrame", u"Delete", None))
        self.pushButton_import.setText(QCoreApplication.translate("AddressFrame", u"Import", None))
        self.pushButton_export.setText(QCoreApplication.translate("AddressFrame", u"Export", None))
    # retranslateUi

