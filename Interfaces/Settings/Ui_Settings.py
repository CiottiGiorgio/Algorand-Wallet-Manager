# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_Settings.ui'
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


class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.setWindowModality(Qt.ApplicationModal)
        Settings.resize(480, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Settings.sizePolicy().hasHeightForWidth())
        Settings.setSizePolicy(sizePolicy)
        Settings.setMinimumSize(QSize(480, 700))
        Settings.setMaximumSize(QSize(480, 700))
        Settings.setBaseSize(QSize(0, 0))
        Settings.setWindowOpacity(1.000000000000000)
        Settings.setModal(True)
        self.verticalLayout = QVBoxLayout(Settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label = QLabel(Settings)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.radioButton_local = QRadioButton(Settings)
        self.radioButton_local.setObjectName(u"radioButton_local")

        self.verticalLayout.addWidget(self.radioButton_local)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_local = QLineEdit(Settings)
        self.lineEdit_local.setObjectName(u"lineEdit_local")

        self.horizontalLayout.addWidget(self.lineEdit_local)

        self.pushButton_folder = QPushButton(Settings)
        self.pushButton_folder.setObjectName(u"pushButton_folder")

        self.horizontalLayout.addWidget(self.pushButton_folder)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.radioButton_remote = QRadioButton(Settings)
        self.radioButton_remote.setObjectName(u"radioButton_remote")

        self.verticalLayout.addWidget(self.radioButton_remote)

        self.groupBox = QGroupBox(Settings)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.lineEdit_algod_url = QLineEdit(self.groupBox)
        self.lineEdit_algod_url.setObjectName(u"lineEdit_algod_url")

        self.gridLayout.addWidget(self.lineEdit_algod_url, 1, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.lineEdit_algod_port = QLineEdit(self.groupBox)
        self.lineEdit_algod_port.setObjectName(u"lineEdit_algod_port")

        self.gridLayout.addWidget(self.lineEdit_algod_port, 1, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.lineEdit_algod_token = QLineEdit(self.groupBox)
        self.lineEdit_algod_token.setObjectName(u"lineEdit_algod_token")

        self.gridLayout.addWidget(self.lineEdit_algod_token, 3, 0, 1, 2)

        self.gridLayout.setColumnStretch(0, 1)

        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Settings)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setAlignment(Qt.AlignCenter)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)

        self.lineEdit_kmd_url = QLineEdit(self.groupBox_2)
        self.lineEdit_kmd_url.setObjectName(u"lineEdit_kmd_url")

        self.gridLayout_2.addWidget(self.lineEdit_kmd_url, 1, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 1, 1, 1)

        self.lineEdit_kmd_port = QLineEdit(self.groupBox_2)
        self.lineEdit_kmd_port.setObjectName(u"lineEdit_kmd_port")

        self.gridLayout_2.addWidget(self.lineEdit_kmd_port, 1, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)

        self.lineEdit_kmd_token = QLineEdit(self.groupBox_2)
        self.lineEdit_kmd_token.setObjectName(u"lineEdit_kmd_token")

        self.gridLayout_2.addWidget(self.lineEdit_kmd_token, 3, 0, 1, 2)

        self.gridLayout_2.setColumnStretch(0, 1)

        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(Settings)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setAlignment(Qt.AlignCenter)
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1)

        self.lineEdit_indexer_url = QLineEdit(self.groupBox_3)
        self.lineEdit_indexer_url.setObjectName(u"lineEdit_indexer_url")

        self.gridLayout_4.addWidget(self.lineEdit_indexer_url, 1, 0, 1, 1)

        self.label_13 = QLabel(self.groupBox_3)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_4.addWidget(self.label_12, 0, 1, 1, 1)

        self.lineEdit_indexer_port = QLineEdit(self.groupBox_3)
        self.lineEdit_indexer_port.setObjectName(u"lineEdit_indexer_port")

        self.gridLayout_4.addWidget(self.lineEdit_indexer_port, 1, 1, 1, 1)

        self.lineEdit_indexer_token = QLineEdit(self.groupBox_3)
        self.lineEdit_indexer_token.setObjectName(u"lineEdit_indexer_token")

        self.gridLayout_4.addWidget(self.lineEdit_indexer_token, 3, 0, 1, 2)

        self.gridLayout_4.setColumnStretch(0, 1)

        self.verticalLayout.addWidget(self.groupBox_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(Settings)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Settings", None))
        self.label.setText(QCoreApplication.translate("Settings", u"Select a method of connection to your Algorand node:", None))
        self.radioButton_local.setText(QCoreApplication.translate("Settings", u"Local node", None))
        self.pushButton_folder.setText(QCoreApplication.translate("Settings", u"Select folder", None))
        self.radioButton_remote.setText(QCoreApplication.translate("Settings", u"Remote node", None))
        self.groupBox.setTitle(QCoreApplication.translate("Settings", u"algod", None))
        self.label_3.setText(QCoreApplication.translate("Settings", u"Port", None))
        self.label_2.setText(QCoreApplication.translate("Settings", u"URL", None))
        self.label_4.setText(QCoreApplication.translate("Settings", u"Token", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Settings", u"kmd", None))
        self.label_7.setText(QCoreApplication.translate("Settings", u"Token", None))
        self.label_6.setText(QCoreApplication.translate("Settings", u"Port", None))
        self.label_5.setText(QCoreApplication.translate("Settings", u"URL", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Settings", u"indexer", None))
        self.label_11.setText(QCoreApplication.translate("Settings", u"URL", None))
        self.label_13.setText(QCoreApplication.translate("Settings", u"Token", None))
        self.label_12.setText(QCoreApplication.translate("Settings", u"Port", None))
    # retranslateUi

