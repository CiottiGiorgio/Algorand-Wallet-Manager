"""
This file declares the MainWindow class subclassed from QMainWindow.

MainWindow class is the fundamental interface from which the program offers its functionality
"""


# PySide2
from PySide2 import QtWidgets, QtGui, QtCore

# Algorand
import algosdk

# Local project
import resources.Constants as ProjectConstants
from resources.ContactsWindow import ContactsWindow
from resources.SettingsWindow import SettingsWindow
from resources.AboutMenu import InfoWindow, CreditsWindow

# Python standard libraries
from os import path, mkdir
from functools import partial
from typing import Type


class MainWindow(QtWidgets.QMainWindow):
    """
    Algorand Wallet Manager main window.

    This window will host the menubar and the frames for wallets and addresses.
    """
    def __init__(self):
        super().__init__()

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Window icon, title & size
        self.setWindowIcon(QtGui.QIcon(path.abspath("graphics/python_icon.ico")))
        self.setWindowTitle("Algorand Wallet Manager")
        self.setFixedSize(500, 300)

        # MenuBar initialization
        self.menu_action_new_transaction = self.menuBar().addAction("New transaction")
        self.menu_action_contacts = self.menuBar().addAction("Contacts")
        self.menu_action_settings = self.menuBar().addAction("Settings")

        self.menu_about = self.menuBar().addMenu("About")
        self.menu_action_info = self.menu_about.addAction("Info")
        self.menu_action_credits = self.menu_about.addAction("Credits")

        for menu_action in [self.menu_action_new_transaction]:
            menu_action.setEnabled(False)

        # MenuBar signal connection.
        # Using partial could be troubling because of circular dependency between memory in python.
        #  It's ok for now because there are no multiple instances of MainWindow and those partial get destroyed when
        #  application closes.
        self.menu_action_contacts.triggered.connect(
            partial(self.exec_dialog, ContactsWindow)
        )
        self.menu_action_settings.triggered.connect(
            partial(self.exec_dialog, SettingsWindow)
        )
        self.menu_action_info.triggered.connect(
            partial(self.exec_dialog, InfoWindow)
        )
        self.menu_action_credits.triggered.connect(
            partial(self.exec_dialog, CreditsWindow)
        )

        self.setCentralWidget(wallet_frame := WalletFrame())

    @staticmethod
    def initialize():
        # Create user data folders
        if not path.exists(ProjectConstants.path_user_data):
            mkdir(ProjectConstants.path_user_data)
        if not path.exists(ProjectConstants.fullpath_thumbnails):
            mkdir(ProjectConstants.fullpath_thumbnails)

        ContactsWindow.load_contacts_json_file()
        SettingsWindow.load_settings_json_file()

    def exec_dialog(self, dialog: Type[QtWidgets.QDialog]):
        child_dialog = dialog(self)
        child_dialog.exec_()

    def closeEvent(self, event: QtGui.QCloseEvent):
        # I don't know if there is a reasonable chance that two different list give out the same hash.
        #  Usually output space is much larger than input space but haven't checked.
        if ContactsWindow.contacts_from_json_file.has_changed():
            ContactsWindow.dump_contacts_json_file()

        if SettingsWindow.settings_from_json_file.has_changed():
            SettingsWindow.dump_settings_json_file()

        event.accept()


# The idea of using a frame is that the content of the MainWindow will change and it will be really
#  easy to do because all it will take is hide one frame and show the other.
class WalletFrame(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        # Main Horizontal Layout
        main_layout = QtWidgets.QHBoxLayout()

        # List of wallet in the connected Algorand node
        #  scrolling is PerPixel because otherwise the list scrolls PerItem and it's not desirable.
        self.list_wallet = QtWidgets.QListWidget()
        self.list_wallet.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        main_layout.addWidget(self.list_wallet)

        # Button Layout on the right
        wallet_button_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(wallet_button_layout)

        # Button creation, styling & add to Layout
        self.button_manage = QtWidgets.QPushButton("Manage\nAddresses")
        self.button_rename = QtWidgets.QPushButton("Rename")
        self.button_new = QtWidgets.QPushButton("New")
        self.button_import = QtWidgets.QPushButton("Import")
        self.button_delete = QtWidgets.QPushButton("Delete")
        self.button_export = QtWidgets.QPushButton("Export")

        button_fixed_width = 65
        self.button_manage.setFixedWidth(button_fixed_width)
        self.button_rename.setFixedWidth(button_fixed_width)
        self.button_new.setFixedWidth(button_fixed_width)
        self.button_import.setFixedWidth(button_fixed_width)
        self.button_delete.setFixedWidth(button_fixed_width)
        self.button_export.setFixedWidth(button_fixed_width)

        wallet_button_layout.addWidget(self.button_manage)
        wallet_button_layout.addStretch(1)
        wallet_button_layout.addWidget(self.button_rename)
        wallet_button_layout.addWidget(self.button_new)
        wallet_button_layout.addWidget(self.button_import)
        wallet_button_layout.addWidget(self.button_delete)
        wallet_button_layout.addWidget(self.button_export)

        for button in [self.button_manage, self.button_rename, self.button_new,
                       self.button_import, self.button_delete, self.button_export]:
            button.setEnabled(False)

        # Setting the frame main layout
        self.setLayout(main_layout)
