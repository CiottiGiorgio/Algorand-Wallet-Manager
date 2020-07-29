# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_Contacts.ui'
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


class Ui_Contacts(object):
    def setupUi(self, Contacts):
        if not Contacts.objectName():
            Contacts.setObjectName(u"Contacts")
        Contacts.resize(480, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Contacts.sizePolicy().hasHeightForWidth())
        Contacts.setSizePolicy(sizePolicy)
        Contacts.setMinimumSize(QSize(480, 600))
        Contacts.setMaximumSize(QSize(480, 600))
        self.verticalLayout = QVBoxLayout(Contacts)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit = QLineEdit(Contacts)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.lineEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listWidget = CustomListWidget(Contacts)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.horizontalLayout.addWidget(self.listWidget)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Contacts)

        QMetaObject.connectSlotsByName(Contacts)
    # setupUi

    def retranslateUi(self, Contacts):
        Contacts.setWindowTitle(QCoreApplication.translate("Contacts", u"Contacts", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Contacts", u"Search...", None))
    # retranslateUi

