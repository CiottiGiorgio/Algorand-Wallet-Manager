"""
This file contains the SettingsWindow class and related static attributes and methods.
"""


# PySide2
from PySide2 import QtWidgets, QtGui, QtCore

# Local project
import misc.Constants as ProjectConstants
from misc.DataStructures import DictJsonSettings

# Python standard libraries
from os import path


class SettingsWindow(QtWidgets.QDialog):
    settings_from_json_file = DictJsonSettings()

    rest_endpoints = {}

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Setup interface
        self.setWindowTitle("Settings")
        self.setFixedSize(450, 600)

        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.addWidget(QtWidgets.QLabel("Select a method of connection with your Algorand node"))
        main_layout.addSpacing(15)

        self.local_radio = QtWidgets.QRadioButton("Local node")
        main_layout.addWidget(self.local_radio)

        local_layout = QtWidgets.QVBoxLayout()

        local_folder_layout = QtWidgets.QHBoxLayout()

        self.local_line = QtWidgets.QLineEdit()
        local_folder_layout.addWidget(self.local_line)

        self.local_button_select_folder = QtWidgets.QPushButton("Select folder")

        local_folder_layout.addWidget(self.local_button_select_folder)

        local_layout.addLayout(local_folder_layout)

        main_layout.addLayout(local_layout)
        main_layout.addSpacing(15)

        self.remote_radio = QtWidgets.QRadioButton("Remote node")
        main_layout.addWidget(self.remote_radio)

        remote_groupbox_algod = QtWidgets.QGroupBox("algod")
        remote_groupbox_algod.setAlignment(QtCore.Qt.AlignHCenter)
        main_layout.addWidget(remote_groupbox_algod)

        remote_layout_algod = QtWidgets.QGridLayout()

        remote_layout_algod.addWidget(QtWidgets.QLabel("URL"), 0, 0)
        self.remote_algod_line_url = QtWidgets.QLineEdit()
        remote_layout_algod.addWidget(self.remote_algod_line_url, 1, 0)

        remote_layout_algod.addWidget(QtWidgets.QLabel("Port"), 0, 1)
        self.remote_algod_line_port = QtWidgets.QLineEdit()
        # Even if i wrote (1, 65535) it would accept as far as 99999 so might as well write it myself.
        #  This is not a complete functional filter but at least limits the input to integers.
        self.remote_algod_line_port.setValidator(QtGui.QIntValidator(1, 99999))
        remote_layout_algod.addWidget(self.remote_algod_line_port, 1, 1)

        remote_layout_algod.addWidget(QtWidgets.QLabel("Token"), 2, 0)
        self.remote_algod_line_token = QtWidgets.QLineEdit()
        remote_layout_algod.addWidget(self.remote_algod_line_token, 3, 0, 1, 2)

        remote_layout_algod.setColumnStretch(0, 1)

        remote_groupbox_algod.setLayout(remote_layout_algod)

        remote_groupbox_kmd = QtWidgets.QGroupBox("kmd")
        remote_groupbox_kmd.setAlignment(QtCore.Qt.AlignHCenter)
        main_layout.addWidget(remote_groupbox_kmd)

        remote_layout_kmd = QtWidgets.QGridLayout()

        remote_layout_kmd.addWidget(QtWidgets.QLabel("URL"), 0, 0)
        self.remote_kmd_line_url = QtWidgets.QLineEdit()
        remote_layout_kmd.addWidget(self.remote_kmd_line_url, 1, 0)

        remote_layout_kmd.addWidget(QtWidgets.QLabel("Port"), 0, 1)
        self.remote_kmd_line_port = QtWidgets.QLineEdit()
        self.remote_kmd_line_port.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.remote_kmd_line_port.setValidator(QtGui.QIntValidator(1, 99999))
        remote_layout_kmd.addWidget(self.remote_kmd_line_port, 1, 1)

        remote_layout_kmd.addWidget(QtWidgets.QLabel("Token"), 2, 0)
        self.remote_kmd_line_token = QtWidgets.QLineEdit()
        remote_layout_kmd.addWidget(self.remote_kmd_line_token, 3, 0, 1, 2)

        remote_layout_kmd.setColumnStretch(0, 10)

        remote_groupbox_kmd.setLayout(remote_layout_kmd)

        remote_groupbox_indexer = QtWidgets.QGroupBox("indexer")
        remote_groupbox_indexer.setAlignment(QtCore.Qt.AlignHCenter)
        main_layout.addWidget(remote_groupbox_indexer)

        remote_layout_indexer = QtWidgets.QVBoxLayout()
        remote_groupbox_indexer.setLayout(remote_layout_indexer)

        main_layout.addStretch(1)

        self.button_confirm = QtWidgets.QPushButton("Confirm")
        self.button_confirm.clicked.connect(self.button_confirm_clicked)
        main_layout.addWidget(self.button_confirm, alignment=QtCore.Qt.AlignRight)

        self.button_confirm.setFocus()
        # End setup

        # Slot connect
        self.local_button_select_folder.clicked.connect(self.button_select_folder_clicked)

        # Restoring fields
        settings = SettingsWindow.settings_from_json_file.memory  # Shortened

        if settings["selected"] == 0:
            self.local_radio.setChecked(True)
        elif settings["selected"] == 1:
            self.remote_radio.setChecked(True)

        self.local_line.setText(settings["local"])

        self.remote_algod_line_url.setText(settings["algod"]["url"])
        self.remote_algod_line_port.setText(settings["algod"]["port"])
        self.remote_algod_line_token.setText(settings["algod"]["token"])

        self.remote_kmd_line_url.setText(settings["kmd"]["url"])
        self.remote_kmd_line_port.setText(settings["kmd"]["port"])
        self.remote_kmd_line_token.setText(settings["kmd"]["token"])

    @QtCore.Slot()
    def button_select_folder_clicked(self):
        """
        This method updates the content of self.local_line after self.button_select_folder is clicked
        """
        dir_path = QtWidgets.QFileDialog.getExistingDirectory()
        if dir_path != "":
            self.local_line.setText(dir_path)

    @QtCore.Slot()
    def button_confirm_clicked(self):
        settings = SettingsWindow.settings_from_json_file.memory

        if self.local_radio.isChecked():
            settings["selected"] = 0
        elif self.remote_radio.isChecked():
            settings["selected"] = 1

        settings["local"] = self.local_line.text()

        settings["algod"]["url"] = self.remote_algod_line_url.text()
        settings["algod"]["port"] = self.remote_algod_line_port.text()
        settings["algod"]["token"] = self.remote_algod_line_token.text()

        settings["kmd"]["url"] = self.remote_kmd_line_url.text()
        settings["kmd"]["port"] = self.remote_kmd_line_port.text()
        settings["kmd"]["token"] = self.remote_kmd_line_token.text()

        self.close()

        self.parent().restart()

    @staticmethod
    def calculate_rest_endpoints():
        """
        This static methods turns the user settings into REST connection points. Either by using manual mode or by
        reading it from algod.net, algod.token, kmd.net and kmd.token files.

        It's crucial that the pair (address, token) remains consistent. Meaning that either both exists or none does.
        """
        settings = SettingsWindow.settings_from_json_file.memory

        temp = dict()

        if settings["selected"] == 0:
            # Get the rest endpoints through local files.

            try:
                with open(path.join(settings["local"], ProjectConstants.filename_algod_net)) as f1, \
                        open(path.join(settings["local"], ProjectConstants.filename_algod_token)) as f2:
                    temp["algod"] = {
                        "address": f1.readline(),
                        "token": f2.readline()
                    }
            except:
                if "algod" in temp:
                    del temp["algod"]

            try:
                with open(path.join(settings["local"], ProjectConstants.filename_kmd_net)) as f3, \
                        open(path.join(settings["local"], ProjectConstants.filename_kmd_token)) as f4:
                    temp["kmd"] = {
                        "address": f3.readline(),
                        "token": f4.readline()
                    }
            except:
                if "kmd" in temp:
                    del temp["kmd"]

        elif settings["selected"] == 1:
            # Use rest endpoints directly.

            if settings["algod"]["url"] and settings["algod"]["port"] and settings["algod"]["token"]:
                temp["algod"] = {
                    "address": settings["algod"]["url"] + ':' + settings["algod"]["port"],
                    "token": settings["algod"]["token"]
                }

            if settings["kmd"]["url"] and settings["kmd"]["port"] and settings["kmd"]["token"]:
                temp["kmd"] = {
                    "address": settings["kmd"]["url"] + ':' + settings["kmd"]["port"],
                    "token": settings["kmd"]["token"]
                }

        SettingsWindow.rest_endpoints = temp
