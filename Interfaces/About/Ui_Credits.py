# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_Credits.ui'
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


class Ui_Credits(object):
    def setupUi(self, Credits):
        if not Credits.objectName():
            Credits.setObjectName(u"Credits")
        Credits.resize(250, 80)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Credits.sizePolicy().hasHeightForWidth())
        Credits.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Credits)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Credits)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.label_2 = QLabel(Credits)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)


        self.retranslateUi(Credits)

        QMetaObject.connectSlotsByName(Credits)
    # setupUi

    def retranslateUi(self, Credits):
        Credits.setWindowTitle(QCoreApplication.translate("Credits", u"Credits", None))
        self.label.setText(QCoreApplication.translate("Credits", u"Credits for the icons used in this application:", None))
        self.label_2.setText(QCoreApplication.translate("Credits", u"Freepik, Those Icons & Pixel perfect\n"
"from www.flaticon.com", None))
    # retranslateUi

