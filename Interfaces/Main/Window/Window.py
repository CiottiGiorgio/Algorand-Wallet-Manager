"""
This file declares the Main class subclassed from QMainWindow.

Main class is the fundamental interface from which the program offers its functionality
"""


# PySide2
from PySide2 import QtWidgets, QtGui, QtCore

# Local project
from graphics import resources

import misc.Constants as ProjectConstants
from misc.Functions import load_json_file, dump_json_file, find_main_window
from misc.Entities import AlgorandWorker
from misc.Widgets import LoadingWidget

from Interfaces.Transaction.Window.Window import TransactionWindow
from Interfaces.Main.Window.Ui_Window import Ui_MainWindow
from Interfaces.Main.Wallet.Frame.Frame import WalletsFrame
from Interfaces.Contacts.Window.Window import ContactsWindow, ListJsonContacts
from Interfaces.Settings.Window.Window import SettingsWindow, DictJsonSettings
from Interfaces.About.Window import InfoWindow, CreditsWindow

# Python standard libraries
from os import path, mkdir
from functools import partial
from typing import Type
import jsonpickle


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Algorand Wallet Manager main window.

    This window will host the menubar and the frames for wallets and addresses.
    """
    def __init__(self):
        super().__init__()

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # This thread pool will be used to issue blocking calls of algosdk.
        # If we want to setup a timeout timer for a algosdk blocking call, a technique could be to start thread A
        #  that starts a timer.
        #  Then thread A starts a thread B with the algosdk blocking call. Then only two things can happen:
        #   1. thread B responds to thread A within the timer timeout
        #   2. thread B does not respond to thread A within the timer timeout
        #  Either way we get an answer from thread A within some fixed time.
        self.thread_pool = QtCore.QThreadPool(self)

        self.setupUi(self)

        self.menuBar().setNativeMenuBar(False)

        self.wallet_frame = None

        self.setWindowIcon(QtGui.QIcon(":/icons/python.ico"))

        # This has to be done here because Qt Creator doesn't allow action on the menuBar itself.
        self.menuAction_NewTransaction = self.menuBar().addAction("New transaction")
        self.menuAction_Contacts = self.menuBar().addAction("Contacts")
        self.menuAction_Settings = self.menuBar().addAction("Settings")
        self.menu_About = self.menuBar().addMenu("About")
        self.menuAction_Info = self.menu_About.addAction("Info")
        self.menuAction_Credits = self.menu_About.addAction("Credits")

        # Initial state
        self.menuAction_NewTransaction.setEnabled(False)

        # Connections
        self.menuAction_NewTransaction.triggered.connect(
            self.exec_transaction
        )
        self.menuAction_Settings.triggered.connect(
            self.exec_settings
        )
        self.menuAction_Contacts.triggered.connect(
            partial(self.exec_dialog, ContactsWindow)
        )
        self.menuAction_Info.triggered.connect(
            partial(self.exec_dialog, InfoWindow)
        )
        self.menuAction_Credits.triggered.connect(
            partial(self.exec_dialog, CreditsWindow)
        )

        QtCore.QTimer.singleShot(0, self.restart)

    @QtCore.Slot()
    def exec_transaction(self):
        if not self.wallet_frame.algod_client:
            QtWidgets.QMessageBox.critical(self, "algod settings", "Please check algod settings.")
            return

        self.exec_dialog(TransactionWindow)

    @QtCore.Slot()
    def exec_settings(self):
        settings_window = SettingsWindow(self)
        if settings_window.exec_() == QtWidgets.QDialog.Accepted:
            self.restart()

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
        self.menuAction_NewTransaction.setEnabled(False)

        if self.queuedWidget.count() >= 1:
            self.queuedWidget.clear_queue()

        SettingsWindow.calculate_rest_endpoints()

        self.wallet_frame = WalletsFrame(self)
        self.queuedWidget.add_widget(self.wallet_frame)

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
        This overridden method gets called before actually destroying self.

        It's used to finalize some resources and then it passes the event up the chain to let PySide2 deal with it.
        """
        if ContactsWindow.contacts_from_json_file.has_changed():
            dump_json_file(
                ProjectConstants.fullpath_contacts_json,
                ContactsWindow.contacts_from_json_file
            )
        if SettingsWindow.saved_json_settings.has_changed():
            dump_json_file(
                ProjectConstants.fullpath_settings_json,
                SettingsWindow.saved_json_settings
            )

        # We have no choice but to do it this way because i have no control over how much time a call through algosdk
        #  could take and it's not possible to dirty kill a QRunnable.
        if self.thread_pool.activeThreadCount() > 0:
            self.setVisible(False)
            self.exec_dialog(ClosingWindow)

        event.accept()

    @staticmethod
    def initialize():
        """
        This method does some preparation work such as creating folders and files if they are not present in
        the filesystem.

        This method is meant to be called before Main instantiation however it's convenient that it is a method here
        because SettingsWindow and ContactsWindow needs to be imported.
        """
        # Create user data folders
        if not path.exists(ProjectConstants.path_user_data):
            mkdir(ProjectConstants.path_user_data)
        if not path.exists(ProjectConstants.fullpath_thumbnails):
            mkdir(ProjectConstants.fullpath_thumbnails)

        # Create json files
        file = ProjectConstants.fullpath_contacts_json
        if not path.exists(file):
            with open(file, 'w') as f:
                f.write(jsonpickle.encode(ListJsonContacts(), indent='\t'))
        file = ProjectConstants.fullpath_settings_json
        if not path.exists(file):
            with open(file, 'w') as f:
                f.write(jsonpickle.encode(DictJsonSettings(), indent='\t'))

        ContactsWindow.contacts_from_json_file = load_json_file(ProjectConstants.fullpath_contacts_json)
        ContactsWindow.contacts_from_json_file.save_state()

        SettingsWindow.saved_json_settings = load_json_file(ProjectConstants.fullpath_settings_json)
        SettingsWindow.saved_json_settings.save_state()


class ClosingWindow(QtWidgets.QDialog):
    """
    This class is a window that signals to the user that some tasks are still running and
    the application can't be closed right now.
    """
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent, QtCore.Qt.CustomizeWindowHint)

        self.setWindowTitle("Background tasks")
        self.setFixedSize(220, 70)

        main_layout = QtWidgets.QHBoxLayout(self)

        main_layout.addWidget(LoadingWidget(self, "Waiting for all tasks to close..."))

        closing_timer = QtCore.QTimer(self)
        closing_timer.timeout.connect(self.terminate)
        closing_timer.start(500)

    def terminate(self):
        if find_main_window().thread_pool.activeThreadCount() == 0:
            self.close()
