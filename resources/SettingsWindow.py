"""
This file contains the setting window class and related static attributes and methods
"""


# PySide2
from PySide2 import QtWidgets, QtCore

# Local project
from resources.DataStructures import ChangeContainer


class DictJsonSettings(ChangeContainer):
    def __init__(self):
        super().__init__()
        self.memory = dict()

        self.memory["selected"] = 0

        self.memory["local"] = ""

        self.memory["algod"] = {"url": "", "port": "", "token": ""}
        self.memory["kmd"] = {"url": "", "port": "", "token": ""}
        self.memory["indexer"] = {"url": "", "port": "", "token": ""}


class SettingsWindow(QtWidgets.QDialog):
    settings_from_json_file = DictJsonSettings()

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

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
        self.local_line.setPlaceholderText("Algorand node folder")
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
        remote_layout_algod.addWidget(self.remote_algod_line_port, 1, 1)

        remote_layout_algod.addWidget(QtWidgets.QLabel("Token"), 2, 0)
        self.remote_algod_line_token = QtWidgets.QLineEdit()
        remote_layout_algod.addWidget(self.remote_algod_line_token, 3, 0, 1, 2)

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
        remote_layout_kmd.addWidget(self.remote_kmd_line_port, 1, 1)

        remote_layout_kmd.addWidget(QtWidgets.QLabel("Token"), 2, 0)
        self.remote_kmd_line_token = QtWidgets.QLineEdit()
        remote_layout_kmd.addWidget(self.remote_kmd_line_token, 3, 0, 1, 2)

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

        # Restoring fields
        settings = SettingsWindow.settings_from_json_file.memory  # This is just to make code look shorter

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
