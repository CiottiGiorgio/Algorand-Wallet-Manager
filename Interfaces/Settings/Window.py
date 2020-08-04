"""
This file contains the SettingsWindow class and related static attributes and methods.
"""


# PySide2
from PySide2 import QtWidgets, QtCore

# Local project
import misc.Constants as ProjectConstants
from misc.DataStructures import DictJsonSettings
from Interfaces.Settings.Ui_Settings import Ui_Settings

# Python standard libraries
from os import path
from sys import stderr


class SettingsWindow(QtWidgets.QDialog, Ui_Settings):
    settings_from_json_file = DictJsonSettings()

    rest_endpoints = {}

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setupUi(self)

        # Connections
        self.radioButton_local.toggled.connect(self.radiobutton_change_enabled)
        self.radioButton_remote.toggled.connect(self.radiobutton_change_enabled)
        self.pushButton_folder.clicked.connect(self.pushbutton_folder_dialog)

        # Initial states
        self.groupBox_3.setVisible(False)

        settings = SettingsWindow.settings_from_json_file.memory  # Shortened
        if settings["selected"] == 0:
            self.radioButton_local.setChecked(True)
        elif settings["selected"] == 1:
            self.radioButton_remote.setChecked(True)

        self.lineEdit_local.setText(settings["local"])

        self.lineEdit_algod_url.setText(settings["algod"]["url"])
        self.lineEdit_algod_port.setText(settings["algod"]["port"])
        self.lineEdit_algod_token.setText(settings["algod"]["token"])

        self.lineEdit_kmd_url.setText(settings["kmd"]["url"])
        self.lineEdit_kmd_port.setText(settings["kmd"]["port"])
        self.lineEdit_kmd_token.setText(settings["kmd"]["token"])

    @QtCore.Slot()
    def accept(self):
        settings = SettingsWindow.settings_from_json_file.memory

        if self.radioButton_local.isChecked():
            settings["selected"] = 0
        elif self.radioButton_remote.isChecked():
            settings["selected"] = 1
        else:
            print("This line is impossible to execute. If you see this the universe is collapsing.", file=stderr)

        settings["local"] = self.lineEdit_local.text()

        settings["algod"]["url"] = self.lineEdit_algod_url.text()
        settings["algod"]["port"] = self.lineEdit_algod_port.text()
        settings["algod"]["token"] = self.lineEdit_algod_token.text()

        settings["kmd"]["url"] = self.lineEdit_kmd_url.text()
        settings["kmd"]["port"] = self.lineEdit_kmd_port.text()
        settings["kmd"]["token"] = self.lineEdit_kmd_token.text()

        super().accept()

    @QtCore.Slot()
    def radiobutton_change_enabled(self):
        if self.radioButton_local.isChecked():
            for widget in [self.lineEdit_local, self.pushButton_folder]:
                widget.setEnabled(True)

            for widget in [self.lineEdit_algod_url, self.lineEdit_algod_port, self.lineEdit_algod_token,
                           self.lineEdit_kmd_url, self.lineEdit_kmd_port, self.lineEdit_kmd_token,
                           self.lineEdit_indexer_url, self.lineEdit_indexer_port, self.lineEdit_indexer_token]:
                widget.setEnabled(False)
        elif self.radioButton_remote.isChecked():
            for widget in [self.lineEdit_local, self.pushButton_folder]:
                widget.setEnabled(False)

            for widget in [self.lineEdit_algod_url, self.lineEdit_algod_port, self.lineEdit_algod_token,
                           self.lineEdit_kmd_url, self.lineEdit_kmd_port, self.lineEdit_kmd_token,
                           self.lineEdit_indexer_url, self.lineEdit_indexer_port, self.lineEdit_indexer_token]:
                widget.setEnabled(True)
        else:
            print("This line is impossible to execute. If you see this the universe is collapsing.", file=stderr)

    @QtCore.Slot()
    def pushbutton_folder_dialog(self):
        """
        This method updates the content of self.local_line after self.button_select_folder is clicked
        """
        dir_path = QtWidgets.QFileDialog.getExistingDirectory()
        if dir_path != "":
            self.lineEdit_local.setText(dir_path)

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
            except Exception as e:
                if "algod" in temp:
                    del temp["algod"]

            try:
                with open(path.join(settings["local"], ProjectConstants.filename_kmd_net)) as f3, \
                        open(path.join(settings["local"], ProjectConstants.filename_kmd_token)) as f4:
                    temp["kmd"] = {
                        "address": f3.readline(),
                        "token": f4.readline()
                    }
            except Exception as e:
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
