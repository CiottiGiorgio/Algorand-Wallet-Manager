"""
This file declares the MainWindow class subclassed from QMainWindow.

MainWindow class is the fundamental interface from which the program offers its functionality
"""


# PySide2
from PySide2 import QtWidgets, QtGui, QtCore

# Local project
import resources.Constants as ProjectConstants
from resources.MiscFunctions import dump_json_file
from resources.Entities import AlgorandWorker
from resources.WalletAddressFrames import WalletsFrame
from resources.ContactsWindow import ContactsWindow, ListJsonContacts
from resources.SettingsWindow import SettingsWindow, DictJsonSettings
from resources.AboutMenu import InfoWindow, CreditsWindow

# Python standard libraries
from sys import stderr
from os import path, mkdir
from functools import partial
from typing import Type
import jsonpickle


class MainWindow(QtWidgets.QMainWindow):
    """
    Algorand Wallet Manager main window.

    This window will host the menubar and the frames for wallets and addresses.
    """
    def __init__(self):
        super().__init__()

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # This thread pool will be used to issue blocking calls of algosdk.
        self.thread_pool = QtCore.QThreadPool(self)

        # Setup interface
        #   Window icon, title & size
        self.setWindowIcon(QtGui.QIcon(path.abspath("graphics/python_icon.ico")))
        self.setWindowTitle("Algorand Wallet Manager")
        self.setFixedSize(500, 300)

        #   MenuBar initialization
        self.menu_action_new_transaction = self.menuBar().addAction("New transaction")
        self.menu_action_contacts = self.menuBar().addAction("Contacts")
        self.menu_action_settings = self.menuBar().addAction("Settings")
        self.menu_about = self.menuBar().addMenu("About")
        self.menu_action_info = self.menu_about.addAction("Info")
        self.menu_action_credits = self.menu_about.addAction("Credits")

        #   The first wallet will be initialized by self.restart
        self.wallet_frame = None
        # End setup

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

        # We hijack this method to do the first start.
        self.restart()

    @staticmethod
    def initialize():
        """
        This method does some preparation work such as creating folders and files if they are not present in
        the filesystem.

        This method is meant to be called before MainWindow instantiation.
        """
        # Create user data folders
        if not path.exists(ProjectConstants.path_user_data):
            mkdir(ProjectConstants.path_user_data)
        if not path.exists(ProjectConstants.fullpath_thumbnails):
            mkdir(ProjectConstants.fullpath_thumbnails)

        # Create json files
        if not path.exists(file := ProjectConstants.fullpath_contacts_json):
            with open(file, 'w') as f:
                f.write(jsonpickle.encode(ListJsonContacts(), indent='\t'))
        if not path.exists(file := ProjectConstants.fullpath_settings_json):
            with open(file, 'w') as f:
                f.write(jsonpickle.encode(DictJsonSettings(), indent='\t'))

    def exec_dialog(self, dialog: Type[QtWidgets.QDialog]):
        """
        This method executes a QDialog window.
        """
        child_dialog = dialog(self)
        child_dialog.exec_()

    def restart(self):
        """
        This method restart the application from the point when it tries to connect to a node to display wallets.
        This method can also be used to do the first start.

        This is done by deleting any existing WalletFrame and creating a new one.
        This method also makes sure that new settings are refreshed into new rest endpoints.
        """
        # This will be enabled in the future when it can be called. (i.e.: there exists at least one wallet)
        for menu_action in [self.menu_action_new_transaction]:
            menu_action.setEnabled(False)

        if self.wallet_frame:
            self.wallet_frame.destroy()

        SettingsWindow.calculate_rest_endpoints()

        self.wallet_frame = WalletsFrame(self)
        self.setCentralWidget(self.wallet_frame)

    def start_worker(self, fn: callable, fn_success: callable, fn_error: callable) -> AlgorandWorker:
        worker = AlgorandWorker(fn)

        if fn_success:
            worker.signals.success.connect(fn_success)

        if fn_error:
            worker.signals.error.connect(fn_error)

        self.thread_pool.start(worker)

        return worker

    def closeEvent(self, event: QtGui.QCloseEvent):
        """
        This overloaded method gets called before actually destroying self.

        It's used to finalize some resources and then it passes the event up the chain to let PySide2 deal with it.
        """
        if ContactsWindow.contacts_from_json_file.has_changed():
            dump_json_file(
                ProjectConstants.fullpath_contacts_json,
                ContactsWindow.contacts_from_json_file
            )
        if SettingsWindow.settings_from_json_file.has_changed():
            dump_json_file(
                ProjectConstants.fullpath_settings_json,
                SettingsWindow.settings_from_json_file
            )

        event.accept()

