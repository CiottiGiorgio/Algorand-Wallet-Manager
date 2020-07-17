"""
This file declares the Main class subclassed from QMainWindow.

Main class is the fundamental interface from which the program offers its functionality
"""


# PySide2
from PySide2 import QtWidgets, QtGui, QtCore

# Local project
import misc.Constants as ProjectConstants
from misc.Functions import load_json_file, dump_json_file
from misc.Entities import AlgorandWorker
from misc.Widgets import LoadingWidget
from misc.Widgets import StackedQueuedWidget
from Interfaces.Main.WalletFrame import WalletsFrame
from Interfaces.Contacts.Windows import ContactsWindow, ListJsonContacts
from Interfaces.Settings.Windows import SettingsWindow, DictJsonSettings
from Interfaces.About.Windows import InfoWindow, CreditsWindow

# Python standard libraries
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
        # If we want to setup a timeout timer for a algosdk blocking call, a technique could be to start thread A
        #  that starts a timer.
        #  Then thread A starts a thread B with the algosdk blocking call. Then only two things can happen:
        #   1. thread B responds to thread A within the timer timeout
        #   2. thread B does not respond to thread A within the timer timeout
        #  Either way we get an answer from thread A within some fixed time.
        self.thread_pool = QtCore.QThreadPool(self)

        # Setup interface
        #   Window icon, title & size
        self.setWindowIcon(QtGui.QIcon(path.abspath("graphics/python_icon.ico")))
        self.setWindowTitle("Algorand Wallet Manager")
        self.setFixedSize(550, 300)

        #   MenuBar initialization
        self.menu_action_new_transaction = self.menuBar().addAction("New transaction")
        self.menu_action_contacts = self.menuBar().addAction("Contacts")
        self.menu_action_settings = self.menuBar().addAction("Settings")
        self.menu_about = self.menuBar().addMenu("About")
        self.menu_action_info = self.menu_about.addAction("Info")
        self.menu_action_credits = self.menu_about.addAction("Credits")

        # This layout will be used to display the single WalletFrame and multiple AddressFrame one at a time.
        self.main_widget = StackedQueuedWidget(self)
        self.setCentralWidget(self.main_widget)
        # End setup

        # MenuBar signal connection.
        # Using partial could be troubling because of circular dependency between memory in python.
        #  It's ok for now because there are no multiple instances of Main and those partial get destroyed when
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

        This method is meant to be called before Main instantiation.
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

        ContactsWindow.contacts_from_json_file = load_json_file(ProjectConstants.fullpath_contacts_json)
        ContactsWindow.contacts_from_json_file.save_state()
        SettingsWindow.settings_from_json_file = load_json_file(ProjectConstants.fullpath_settings_json)
        SettingsWindow.settings_from_json_file.save_state()

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

        if self.main_widget.count() >= 1:
            self.main_widget.clear_queue()

        SettingsWindow.calculate_rest_endpoints()

        self.main_widget.add_widget(wallet_frame := WalletsFrame(self))
        ProjectConstants.wallet_frame = wallet_frame

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
        if SettingsWindow.settings_from_json_file.has_changed():
            dump_json_file(
                ProjectConstants.fullpath_settings_json,
                SettingsWindow.settings_from_json_file
            )

        # We have no choice but to do it this way because i have no control over how much time a call through algosdk
        #  could take and it's not possible to dirty kill a QRunnable.
        if self.thread_pool.activeThreadCount() > 0:
            self.setVisible(False)
            self.exec_dialog(ClosingWindow)

        event.accept()


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

        main_layout.addWidget(LoadingWidget("Waiting for all tasks to close..."))

        closing_timer = QtCore.QTimer(self)
        closing_timer.timeout.connect(self.terminate)
        closing_timer.start(500)

    def terminate(self):
        if self.parent().thread_pool.activeThreadCount() == 0:
            self.close()
