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

from misc.Widgets import StackedQueuedWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 300)
        MainWindow.setMinimumSize(QSize(600, 300))
        self.actionInfo = QAction(MainWindow)
        self.actionInfo.setObjectName(u"actionInfo")
        self.actionCredits = QAction(MainWindow)
        self.actionCredits.setObjectName(u"actionCredits")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.queuedWidget = StackedQueuedWidget(self.centralwidget)
        self.queuedWidget.setObjectName(u"queuedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.queuedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.queuedWidget.addWidget(self.page_2)

        self.gridLayout.addWidget(self.queuedWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Algorand Wallet Manager", None))
        self.actionInfo.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.actionCredits.setText(QCoreApplication.translate("MainWindow", u"Credits", None))
    # retranslateUi

