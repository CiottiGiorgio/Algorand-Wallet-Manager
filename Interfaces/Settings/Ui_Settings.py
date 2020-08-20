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
        Settings.resize(550, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Settings.sizePolicy().hasHeightForWidth())
        Settings.setSizePolicy(sizePolicy)
        Settings.setMinimumSize(QSize(550, 700))
        Settings.setMaximumSize(QSize(550, 700))
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

        self.radioButton_Local = QRadioButton(Settings)
        self.radioButton_Local.setObjectName(u"radioButton_Local")

        self.verticalLayout.addWidget(self.radioButton_Local)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_Local = QLineEdit(Settings)
        self.lineEdit_Local.setObjectName(u"lineEdit_Local")

        self.horizontalLayout.addWidget(self.lineEdit_Local)

        self.pushButton_Folder = QPushButton(Settings)
        self.pushButton_Folder.setObjectName(u"pushButton_Folder")

        self.horizontalLayout.addWidget(self.pushButton_Folder)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.radioButton_EnvVar = QRadioButton(Settings)
        self.radioButton_EnvVar.setObjectName(u"radioButton_EnvVar")

        self.verticalLayout.addWidget(self.radioButton_EnvVar)

        self.lineEdit_EnvVar = QLineEdit(Settings)
        self.lineEdit_EnvVar.setObjectName(u"lineEdit_EnvVar")
        self.lineEdit_EnvVar.setEnabled(True)
        self.lineEdit_EnvVar.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit_EnvVar)

        self.verticalSpacer_6 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.radioButton_Remote = QRadioButton(Settings)
        self.radioButton_Remote.setObjectName(u"radioButton_Remote")

        self.verticalLayout.addWidget(self.radioButton_Remote)

        self.groupBox = QGroupBox(Settings)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_AlgodPort = QLineEdit(self.groupBox)
        self.lineEdit_AlgodPort.setObjectName(u"lineEdit_AlgodPort")

        self.gridLayout.addWidget(self.lineEdit_AlgodPort, 1, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.lineEdit_AlgodToken = QLineEdit(self.groupBox)
        self.lineEdit_AlgodToken.setObjectName(u"lineEdit_AlgodToken")

        self.gridLayout.addWidget(self.lineEdit_AlgodToken, 3, 0, 1, 2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_3.addWidget(self.label_8)

        self.lineEdit_AlgodUrl = QLineEdit(self.groupBox)
        self.lineEdit_AlgodUrl.setObjectName(u"lineEdit_AlgodUrl")

        self.horizontalLayout_3.addWidget(self.lineEdit_AlgodUrl)


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)

        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer_4 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.groupBox_2 = QGroupBox(Settings)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setAlignment(Qt.AlignCenter)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 1, 1, 1)

        self.lineEdit_KmdPort = QLineEdit(self.groupBox_2)
        self.lineEdit_KmdPort.setObjectName(u"lineEdit_KmdPort")

        self.gridLayout_2.addWidget(self.lineEdit_KmdPort, 1, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)

        self.lineEdit_KmdToken = QLineEdit(self.groupBox_2)
        self.lineEdit_KmdToken.setObjectName(u"lineEdit_KmdToken")

        self.gridLayout_2.addWidget(self.lineEdit_KmdToken, 3, 0, 1, 2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_4.addWidget(self.label_9)

        self.lineEdit_KmdUrl = QLineEdit(self.groupBox_2)
        self.lineEdit_KmdUrl.setObjectName(u"lineEdit_KmdUrl")

        self.horizontalLayout_4.addWidget(self.lineEdit_KmdUrl)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 1)

        self.verticalLayout.addWidget(self.groupBox_2)

        self.verticalSpacer_5 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_5)

        self.groupBox_3 = QGroupBox(Settings)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setAlignment(Qt.AlignCenter)
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1)

        self.label_13 = QLabel(self.groupBox_3)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_4.addWidget(self.label_12, 0, 1, 1, 1)

        self.lineEdit_IndexerPort = QLineEdit(self.groupBox_3)
        self.lineEdit_IndexerPort.setObjectName(u"lineEdit_IndexerPort")

        self.gridLayout_4.addWidget(self.lineEdit_IndexerPort, 1, 1, 1, 1)

        self.lineEdit_IndexerToken = QLineEdit(self.groupBox_3)
        self.lineEdit_IndexerToken.setObjectName(u"lineEdit_IndexerToken")

        self.gridLayout_4.addWidget(self.lineEdit_IndexerToken, 3, 0, 1, 2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_5.addWidget(self.label_10)

        self.lineEdit_IndexerUrl = QLineEdit(self.groupBox_3)
        self.lineEdit_IndexerUrl.setObjectName(u"lineEdit_IndexerUrl")

        self.horizontalLayout_5.addWidget(self.lineEdit_IndexerUrl)


        self.gridLayout_4.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)

        self.gridLayout_4.setColumnStretch(0, 1)

        self.verticalLayout.addWidget(self.groupBox_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(Settings)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.lineEdit_Local, self.pushButton_Folder)
        QWidget.setTabOrder(self.pushButton_Folder, self.lineEdit_EnvVar)
        QWidget.setTabOrder(self.lineEdit_EnvVar, self.lineEdit_AlgodUrl)
        QWidget.setTabOrder(self.lineEdit_AlgodUrl, self.lineEdit_AlgodPort)
        QWidget.setTabOrder(self.lineEdit_AlgodPort, self.lineEdit_AlgodToken)
        QWidget.setTabOrder(self.lineEdit_AlgodToken, self.lineEdit_KmdUrl)
        QWidget.setTabOrder(self.lineEdit_KmdUrl, self.lineEdit_KmdPort)
        QWidget.setTabOrder(self.lineEdit_KmdPort, self.lineEdit_KmdToken)
        QWidget.setTabOrder(self.lineEdit_KmdToken, self.lineEdit_IndexerUrl)
        QWidget.setTabOrder(self.lineEdit_IndexerUrl, self.lineEdit_IndexerPort)
        QWidget.setTabOrder(self.lineEdit_IndexerPort, self.lineEdit_IndexerToken)
        QWidget.setTabOrder(self.lineEdit_IndexerToken, self.radioButton_Local)
        QWidget.setTabOrder(self.radioButton_Local, self.radioButton_EnvVar)
        QWidget.setTabOrder(self.radioButton_EnvVar, self.radioButton_Remote)

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Settings", None))
        self.label.setText(QCoreApplication.translate("Settings", u"Select a method of connection to your Algorand node:", None))
        self.radioButton_Local.setText(QCoreApplication.translate("Settings", u"Local node", None))
        self.pushButton_Folder.setText(QCoreApplication.translate("Settings", u"Select folder", None))
        self.radioButton_EnvVar.setText(QCoreApplication.translate("Settings", u"Environment variable \"ALGORAND_DATA\"", None))
        self.radioButton_Remote.setText(QCoreApplication.translate("Settings", u"Remote node", None))
        self.groupBox.setTitle(QCoreApplication.translate("Settings", u"algod", None))
        self.label_3.setText(QCoreApplication.translate("Settings", u"Port", None))
        self.label_4.setText(QCoreApplication.translate("Settings", u"Token", None))
        self.label_2.setText(QCoreApplication.translate("Settings", u"URL", None))
        self.label_8.setText(QCoreApplication.translate("Settings", u"http://", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Settings", u"kmd", None))
        self.label_7.setText(QCoreApplication.translate("Settings", u"Token", None))
        self.label_6.setText(QCoreApplication.translate("Settings", u"Port", None))
        self.label_5.setText(QCoreApplication.translate("Settings", u"URL", None))
        self.label_9.setText(QCoreApplication.translate("Settings", u"http://", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Settings", u"indexer", None))
        self.label_11.setText(QCoreApplication.translate("Settings", u"URL", None))
        self.label_13.setText(QCoreApplication.translate("Settings", u"Token", None))
        self.label_12.setText(QCoreApplication.translate("Settings", u"Port", None))
        self.label_10.setText(QCoreApplication.translate("Settings", u"http://", None))
    # retranslateUi

