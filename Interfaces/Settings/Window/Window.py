"""
This file contains the SettingsWindow class and related static attributes and methods.
"""


# PySide2
from PySide2 import QtWidgets, QtCore

# Local project
from misc.Functions import ProjectException
import misc.Constants as ProjectConstants
from misc.DataStructures import DictJsonSettings
from Interfaces.Settings.Window.Ui_Window import Ui_SettingsWindow

# Python standard libraries
from os import path, environ
from sys import stderr


class SettingsWindow(QtWidgets.QDialog, Ui_SettingsWindow):
    saved_json_settings = DictJsonSettings()

    rest_endpoints = {}

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setupUi(self)

        # Setup interface
        self.groupBox_3.setVisible(False)

        # Connections
        self.radioButton_Local.toggled.connect(self.radiobutton_change_enabled)
        self.radioButton_Remote.toggled.connect(self.radiobutton_change_enabled)
        self.pushButton_Folder.clicked.connect(self.pushbutton_folder_dialog)

        # Shorthand for groups of widgets.
        #   These will come in handy when enabling or disabling the respective groups.
        self.local_widgets = [self.lineEdit_Local, self.pushButton_Folder]
        self.envvar_widgets = [self.lineEdit_EnvVar]
        self.remote_widgets = [self.lineEdit_AlgodUrl, self.lineEdit_AlgodPort, self.lineEdit_AlgodToken,
                               self.lineEdit_KmdUrl, self.lineEdit_KmdPort, self.lineEdit_KmdToken,
                               self.lineEdit_IndexerUrl, self.lineEdit_IndexerPort, self.lineEdit_IndexerToken]

        QtCore.QTimer.singleShot(0, self.setup_logic)

    def setup_logic(self):
        settings = SettingsWindow.saved_json_settings.memory  # Shortened
        if settings["selected"] == 0:
            self.radioButton_Local.setChecked(True)
        elif settings["selected"] == 1:
            self.radioButton_EnvVar.setChecked(True)
        elif settings["selected"] == 2:
            self.radioButton_Remote.setChecked(True)
        else:
            raise ProjectException(
                f"settings['selected'] has unexpected value {settings['selected']}"
            )

        self.lineEdit_Local.setText(settings["local"])

        self.lineEdit_EnvVar.setText(environ["ALGORAND_DATA"] if "ALGORAND_DATA" in environ else "")

        self.lineEdit_AlgodUrl.setText(settings["algod"]["url"])
        self.lineEdit_AlgodPort.setText(settings["algod"]["port"])
        self.lineEdit_AlgodToken.setText(settings["algod"]["token"])

        self.lineEdit_KmdUrl.setText(settings["kmd"]["url"])
        self.lineEdit_KmdPort.setText(settings["kmd"]["port"])
        self.lineEdit_KmdToken.setText(settings["kmd"]["token"])

    @QtCore.Slot()
    def accept(self):
        settings = SettingsWindow.saved_json_settings.memory

        if self.radioButton_Local.isChecked():
            settings["selected"] = 0
        elif self.radioButton_EnvVar.isChecked():
            settings["selected"] = 1
        elif self.radioButton_Remote.isChecked():
            settings["selected"] = 2
        else:
            raise ProjectException(
                "No radioButton seems to be selected inside SettingsWindow"
            )

        settings["local"] = self.lineEdit_Local.text()

        settings["algod"]["url"] = self.lineEdit_AlgodUrl.text()
        settings["algod"]["port"] = self.lineEdit_AlgodPort.text()
        settings["algod"]["token"] = self.lineEdit_AlgodToken.text()

        settings["kmd"]["url"] = self.lineEdit_KmdUrl.text()
        settings["kmd"]["port"] = self.lineEdit_KmdPort.text()
        settings["kmd"]["token"] = self.lineEdit_KmdToken.text()

        super().accept()

    @QtCore.Slot()
    def radiobutton_change_enabled(self):
        if self.radioButton_Local.isChecked():
            for widget in self.local_widgets:
                widget.setEnabled(True)

            for widget in self.envvar_widgets + self.remote_widgets:
                widget.setEnabled(False)

        elif self.radioButton_EnvVar.isChecked():
            for widget in self.envvar_widgets:
                widget.setEnabled(True)

            for widget in self.local_widgets + self.remote_widgets:
                widget.setEnabled(False)

        elif self.radioButton_Remote.isChecked():
            for widget in self.remote_widgets:
                widget.setEnabled(True)

            for widget in self.local_widgets + self.envvar_widgets:
                widget.setEnabled(False)

        else:
            raise ProjectException(
                f"self.RadioButton_local.isChecked() has unexpected value - {self.radioButton_Local.isChecked()}"
            )

    @QtCore.Slot()
    def pushbutton_folder_dialog(self):
        """
        This method updates the content of self.local_line after self.button_select_folder is clicked
        """
        dir_path = QtWidgets.QFileDialog.getExistingDirectory()
        if dir_path != "":
            self.lineEdit_Local.setText(dir_path)

    @staticmethod
    def calculate_rest_endpoints():
        """
        This static methods turns the user settings into REST connection points. Either by using manual mode or by
        reading it from algod.net, algod.token, kmd.net and kmd.token files.

        It's crucial that the pair (address, token) remains consistent. Meaning that either both exists or none does.
        """
        settings = SettingsWindow.saved_json_settings.memory

        temp = dict()

        if settings["selected"] == 0 or settings["selected"] == 1:
            # Get the rest endpoints through local files or environment variable.
            node_path = settings["local"] if settings["selected"] == 0 else (
                environ["ALGORAND_DATA"] if "ALGORAND_DATA" in environ else ""
            )
            
            try:
                with open(path.join(node_path, ProjectConstants.filename_algod_net)) as f1, \
                        open(path.join(node_path, ProjectConstants.filename_algod_token)) as f2:
                    temp["algod"] = {
                        "address": "http://" + f1.readline().strip("\n"),
                        "token": f2.readline().strip("\n")
                    }
            except Exception as e:
                print(str(e), file=stderr)
                if "algod" in temp:
                    del temp["algod"]

            try:
                with open(path.join(node_path, ProjectConstants.filename_kmd_net)) as f3, \
                        open(path.join(node_path, ProjectConstants.filename_kmd_token)) as f4:
                    temp["kmd"] = {
                        "address": "http://" + f3.readline().strip("\n"),
                        "token": f4.readline().strip("\n")
                    }
            except Exception as e:
                print(str(e), file=stderr)
                if "kmd" in temp:
                    del temp["kmd"]

        elif settings["selected"] == 2:
            # Use rest endpoints directly.
            if settings["algod"]["url"] and settings["algod"]["port"] and settings["algod"]["token"]:
                temp["algod"] = {
                    "address": "http://" + settings["algod"]["url"] + ':' + settings["algod"]["port"],
                    "token": settings["algod"]["token"]
                }

            if settings["kmd"]["url"] and settings["kmd"]["port"] and settings["kmd"]["token"]:
                temp["kmd"] = {
                    "address": "http://" + settings["kmd"]["url"] + ':' + settings["kmd"]["port"],
                    "token": settings["kmd"]["token"]
                }

        else:
            raise ProjectException(f"settings['selected'] has unexpected value: {settings['selected']}")

        SettingsWindow.rest_endpoints = temp
