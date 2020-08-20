# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_ContactsCreating.ui'
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


class Ui_ContactsCreating(object):
    def setupUi(self, ContactsCreating):
        if not ContactsCreating.objectName():
            ContactsCreating.setObjectName(u"ContactsCreating")
        ContactsCreating.setWindowModality(Qt.ApplicationModal)
        ContactsCreating.resize(500, 550)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ContactsCreating.sizePolicy().hasHeightForWidth())
        ContactsCreating.setSizePolicy(sizePolicy)
        ContactsCreating.setMinimumSize(QSize(500, 550))
        ContactsCreating.setMaximumSize(QSize(500, 550))
        self.verticalLayout = QVBoxLayout(ContactsCreating)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ContactsCreating)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.lineEdit_Name = QLineEdit(ContactsCreating)
        self.lineEdit_Name.setObjectName(u"lineEdit_Name")
        self.lineEdit_Name.setMinimumSize(QSize(0, 25))

        self.verticalLayout.addWidget(self.lineEdit_Name)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label_2 = QLabel(ContactsCreating)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.lineEdit_Address = QLineEdit(ContactsCreating)
        self.lineEdit_Address.setObjectName(u"lineEdit_Address")
        self.lineEdit_Address.setMinimumSize(QSize(0, 25))

        self.verticalLayout.addWidget(self.lineEdit_Address)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.label_3 = QLabel(ContactsCreating)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(ContactsCreating)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(270, 270))
        self.frame.setMaximumSize(QSize(270, 270))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.label_Picture = QLabel(self.frame)
        self.label_Picture.setObjectName(u"label_Picture")
        self.label_Picture.setMaximumSize(QSize(256, 256))

        self.verticalLayout_3.addWidget(self.label_Picture, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout.addWidget(self.frame)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.pushButton_Change = QPushButton(ContactsCreating)
        self.pushButton_Change.setObjectName(u"pushButton_Change")

        self.verticalLayout_2.addWidget(self.pushButton_Change)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)

        self.pushButton_Delete = QPushButton(ContactsCreating)
        self.pushButton_Delete.setObjectName(u"pushButton_Delete")
        self.pushButton_Delete.setEnabled(False)

        self.verticalLayout_2.addWidget(self.pushButton_Delete)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_6)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(0, 60, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(ContactsCreating)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ContactsCreating)
        self.buttonBox.accepted.connect(ContactsCreating.accept)
        self.buttonBox.rejected.connect(ContactsCreating.reject)

        QMetaObject.connectSlotsByName(ContactsCreating)
    # setupUi

    def retranslateUi(self, ContactsCreating):
        ContactsCreating.setWindowTitle(QCoreApplication.translate("ContactsCreating", u"New Contact", None))
        self.label.setText(QCoreApplication.translate("ContactsCreating", u"Name:", None))
        self.lineEdit_Name.setPlaceholderText(QCoreApplication.translate("ContactsCreating", u"Insert a name for your contact", None))
        self.label_2.setText(QCoreApplication.translate("ContactsCreating", u"Address:", None))
        self.lineEdit_Address.setPlaceholderText(QCoreApplication.translate("ContactsCreating", u"Insert a valid Algorand address", None))
        self.label_3.setText(QCoreApplication.translate("ContactsCreating", u"Photo:", None))
        self.label_Picture.setText("")
        self.pushButton_Change.setText(QCoreApplication.translate("ContactsCreating", u"Change", None))
        self.pushButton_Delete.setText(QCoreApplication.translate("ContactsCreating", u"Delete", None))
    # retranslateUi

