# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_Window.ui'
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


class Ui_ContactsWindow(object):
    def setupUi(self, ContactsWindow):
        if not ContactsWindow.objectName():
            ContactsWindow.setObjectName(u"ContactsWindow")
        ContactsWindow.resize(560, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ContactsWindow.sizePolicy().hasHeightForWidth())
        ContactsWindow.setSizePolicy(sizePolicy)
        ContactsWindow.setMinimumSize(QSize(560, 700))
        ContactsWindow.setMaximumSize(QSize(560, 700))
        self.verticalLayout = QVBoxLayout(ContactsWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit = QLineEdit(ContactsWindow)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.lineEdit)

        self.listWidget = CustomListWidget(ContactsWindow)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)

        self.verticalLayout.addWidget(self.listWidget)


        self.retranslateUi(ContactsWindow)

        QMetaObject.connectSlotsByName(ContactsWindow)
    # setupUi

    def retranslateUi(self, ContactsWindow):
        ContactsWindow.setWindowTitle(QCoreApplication.translate("ContactsWindow", u"Contacts", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("ContactsWindow", u"Search...", None))
    # retranslateUi

