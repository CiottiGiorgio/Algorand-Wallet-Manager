"""
This file declares the MainWindow class subclassed from QMainWindow.

MainWindow class is the fundamental interface from which the program offers its functionality
"""


# PySide2
from PySide2 import QtWidgets, QtGui

# Algorand
import algosdk

# Local project
from resources.ContactsWindow import ContactsWindow

# Python standard libraries
from os import path


class MainWindow(QtWidgets.QMainWindow):
    """
    Algorand Wallet Manager main window.

    This window will host the menubar and the frames for wallets and addresses.
    """
    def __init__(self):
        super().__init__()

        # Window icon, title & size
        self.setWindowIcon(QtGui.QIcon(path.abspath("graphics/python_icon.ico")))
        self.setWindowTitle("Algorand Wallet Manager")
        self.setFixedSize(500, 300)

        # MenuBar initialization
        self.menu_new_transaction = self.menuBar().addAction("New transaction")
        self.menu_contacts = self.menuBar().addAction("Contacts")
        self.menu_settings = self.menuBar().addAction("Settings")
        self.menu_info = self.menuBar().addAction("Info")

        for menu_action in [self.menu_new_transaction, self.menu_settings, self.menu_info]:
            menu_action.setDisabled(True)

        # MenuBar signal connection
        self.menu_contacts.triggered.connect(self.show_contacts)

        wallet_frame = WalletFrame()
        self.setCentralWidget(wallet_frame)

    @staticmethod
    def initialize():
        ContactsWindow.load_contacts_json_file()

    def show_contacts(self):
        # We disable the action on the menu of the main window to prevent the user from opening
        #  multiple contacts window. With QWidget the main window stays active and firing multiple times
        #  is not desirable.
        self.menu_contacts.setEnabled(False)
        contacts_window = ContactsWindow(self)
        contacts_window.show()
        # Menu is reactivated in the destruction of contacts_window inside overloading of closeEvent()

    def closeEvent(self, event: QtGui.QCloseEvent):
        # I don't know if there is a reasonable chance that two different list give out the same hash.
        if ContactsWindow.contacts_from_json_file.has_changed():
            ContactsWindow.dump_contacts_json_file()
        event.accept()


# The idea of using a frame is that the content of the MainWindow will change and it will be really
#  easy to do because all it will take is hide one frame and show the other
class WalletFrame(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        # Main Horizontal Layout
        main_layout = QtWidgets.QHBoxLayout()

        # List of wallet in the connected Algorand node
        #  scrolling is PerPixel because otherwise the list scrolls PerItem and it's not desirable
        self.list_wallet = QtWidgets.QListWidget()
        self.list_wallet.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        # for wallet in ["Wallets will be", "displayed in this list"]:
        #     widget = WalletListWidget(wallet, "Locked")
        #     item = WalletListItem()
        #     item.setSizeHint(widget.minimumSizeHint())
        #     self.list_wallet.addItem(item)
        #     self.list_wallet.setItemWidget(item, widget)

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
        wallet_button_layout.addStretch(1)  # There is a spacing here.
        wallet_button_layout.addWidget(self.button_rename)
        wallet_button_layout.addWidget(self.button_new)
        wallet_button_layout.addWidget(self.button_import)
        wallet_button_layout.addWidget(self.button_delete)
        wallet_button_layout.addWidget(self.button_export)

        for button in [self.button_manage, self.button_rename, self.button_new, self.button_import, self.button_delete, self.button_export]:
            button.setEnabled(False)

        # Setting the frame main layout
        self.setLayout(main_layout)
