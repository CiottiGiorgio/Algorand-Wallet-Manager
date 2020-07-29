# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_BalanceWindow.ui'
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


class Ui_BalanceWindow(object):
    def setupUi(self, BalanceWindow):
        if not BalanceWindow.objectName():
            BalanceWindow.setObjectName(u"BalanceWindow")
        BalanceWindow.resize(320, 430)
        BalanceWindow.setMinimumSize(QSize(320, 430))
        BalanceWindow.setMaximumSize(QSize(320, 430))
        self.verticalLayout = QVBoxLayout(BalanceWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(BalanceWindow)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.scrollArea = QScrollArea(BalanceWindow)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 300, 69))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(6)
        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_balance = QLabel(self.scrollAreaWidgetContents)
        self.label_balance.setObjectName(u"label_balance")
        self.label_balance.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_balance, 0, 1, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_pending_rewards = QLabel(self.scrollAreaWidgetContents)
        self.label_pending_rewards.setObjectName(u"label_pending_rewards")
        self.label_pending_rewards.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_pending_rewards, 1, 1, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.verticalSpacer = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.label_2 = QLabel(BalanceWindow)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.scrollArea_2 = QScrollArea(BalanceWindow)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 300, 274))
        self.verticalLayout_assets = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_assets.setObjectName(u"verticalLayout_assets")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollArea_2)

        self.verticalLayout.setStretch(4, 1)

        self.retranslateUi(BalanceWindow)

        QMetaObject.connectSlotsByName(BalanceWindow)
    # setupUi

    def retranslateUi(self, BalanceWindow):
        BalanceWindow.setWindowTitle(QCoreApplication.translate("BalanceWindow", u"Algos & Assets", None))
        self.label.setText(QCoreApplication.translate("BalanceWindow", u"Algos:", None))
        self.label_3.setText(QCoreApplication.translate("BalanceWindow", u"Balance:", None))
        self.label_balance.setText("")
        self.label_5.setText(QCoreApplication.translate("BalanceWindow", u"Pending rewards:", None))
        self.label_pending_rewards.setText("")
        self.label_2.setText(QCoreApplication.translate("BalanceWindow", u"Assets:", None))
    # retranslateUi

