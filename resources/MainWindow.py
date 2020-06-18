from PySide2 import QtWidgets, QtGui
import algosdk
from resources.ContactsWindow import ContactsWindow
from os import path, mkdir
import json


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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_path_contacts_json = path.abspath(
            path.join(path.expanduser("~"), ".Algorand Wallet Manager")
        )

        self.file_name_contacts_json = "contacts.json"

        # Window icon, title & size
        self.setWindowIcon(QtGui.QIcon(path.abspath("graphics/python_icon.ico")))
        self.setWindowTitle("Algorand Wallet Manager")
        self.setFixedSize(500, 300)

        # Reading contacts information that both ContactsWindow and TransactionWindow will use to create their
        #  CustomListWidgetItem. Only ContactsWindow will be able to change the content of this list through
        #  modifications in its ContactListItem (static contacts_widget)
        self.contacts_from_json_file = list()
        try:
            if not path.exists(self.file_path_contacts_json):
                mkdir(self.file_path_contacts_json)
            with open(path.join(self.file_path_contacts_json, self.file_name_contacts_json)) as fp:
                self.contacts_from_json_file = json.load(fp)
        except:
            print("Could not load contacts from json file")
            quit()

        # We take the hash of the list at this point in time because we want to compare later when closing
        #  application in order to decide if we should dump the content on disk or not
        self.contacts_from_json_file_hash = str(self.contacts_from_json_file).__hash__()

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

    def show_contacts(self):
        # We disable the action on the menu of the main window to prevent the user from opening
        #  multiple contacts window. With QWidget the main window stays active and firing multiple times
        #  is not desirable
        self.menu_contacts.setEnabled(False)
        contacts_window = ContactsWindow(self)
        contacts_window.show()
        # self.menu_contacts.setEnabled(True) can't be called here because .show() is not blocking
        #  but the menu is reactivated in the destruction of contacts_window inside overloading of closeEvent()

    def closeEvent(self, event: QtGui.QCloseEvent):
        # I don't know if there is a reasonable chance that two different list give out the same hash.
        if self.contacts_from_json_file_hash != str(self.contacts_from_json_file).__hash__():
            self.dump_memory_contacts_to_json()
        event.accept()

    def dump_memory_contacts_to_json(self):
        try:
            with open(path.join(self.file_path_contacts_json, self.file_name_contacts_json), "w") as fp:
                json.dump(self.contacts_from_json_file, fp, indent='\t')
        except:
            print("Could not save contacts to json file")
