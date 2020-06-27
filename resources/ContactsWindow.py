"""
This file describes the main contact window, its child widgets and some data structure needed.

ContactsWindow class is the main purpose of this file.
"""


# PySide 2
from PySide2 import QtWidgets, QtGui, QtCore

# Algorand
from algosdk.encoding import is_valid_address

# Local project
import resources.Constants as ProjectConstants
from resources.Entities import Contact
from resources.CustomListWidgetItem import ContactListItem, ContactListWidget

# Python standard libraries
import os
from sys import stderr
from shutil import copyfile
from string import ascii_letters, digits
from random import sample
from functools import partial
from typing import Union, List
import jsonpickle


# TODO .old_hash appears in json serialization. We don't need to save its state so make sure that only the list appears
#  in serialization
# There probably is a more efficient way of doing this. This is the faster way to code this functionality right now.
#  An alternative could be overriding writing methods to the list and making sure that a bool flag starts at False
#  and becomes True at the first change. .save_state() then becomes just resetting this flag with False again.
class ListJsonContacts(list):
    """
    Subclass of standard python list

    This class is useful for taking a snapshot of itself in time A and then checking if the content has changed in
    time B with A <= B.
    """
    def __init__(self):
        super().__init__()

        self.old_hash = None

    def save_state(self):
        self.old_hash = str(self).__hash__()

    def has_changed(self) -> bool:
        return str(self).__hash__() != self.old_hash


class ContactsWindow(QtWidgets.QWidget):
    """
    Contact list window.

    This subclass of QWidget spawn a new window with the functionality to manage a contact list.
    I have decided that this class will also host static information about contacts. Other classes might need this
    info such as the transaction window (e.g.: when sending algos or assets you get suggestions when typing in the
    receiver of such transaction).
    """
    # These icons are static because we want to avoid having to reload them from the disk each time this class is
    #  instantiated
    icon_search = QtGui.QIcon(os.path.abspath("graphics/search.png"))
    icon_edit = QtGui.QIcon(os.path.abspath("graphics/edit.png"))
    icon_delete = QtGui.QIcon(os.path.abspath("graphics/delete.png"))

    # This list will host the content of the contacts.json file. This is static because other classes might need to
    #  read contacts and create their own widgets.
    #  However this class will be the only one to load it and change it. Other classes shall only read from it.
    # A crucial point is that this list gets loaded with the static method load_contacts_json_file as soon as this
    #  class is done with the definition because other class might need its data even if this class never
    #  gets instantiated
    contacts_from_json_file = ListJsonContacts()

    # We make a list of ContactListItem static because each item has a profile pic that could create IO bottleneck
    #  if it has to be loaded each time this class is instantiated.
    # However we create the list of widget for ContactsWindow only the first time that this class is
    #  instantiated because only this class needs its ContactListWidget.
    contact_widgets = list()

    def __init__(self, parent: QtWidgets.QWidget):
        # This line is necessary because a widget gets it's own window if it doesn't have a parent OR
        #  if it has a parent but has QtCore.Qt.Window flag set.
        super().__init__(parent, QtCore.Qt.Window)

        # Populate contact_widgets with info from json file.
        if not self.contact_widgets:
            for contact in self.contacts_from_json_file:
                self.contact_widgets.append(ContactListWidget(contact))

        # Title, window size & position
        self.setWindowTitle("Contacts")
        width, height = 350, 550
        parent_size = self.parent().size()
        self.setFixedSize(width, height)
        # With this next line we spawn the ContactWindow 50 pixels distant from parent in x axis and
        #  we align the centers of the two window losing half of the difference in height on the longer window.
        self.move(self.parent().pos() +
                  QtCore.QPoint(parent_size.width() + 50, -1 * (height - parent_size.height()) // 2))

        main_layout = QtWidgets.QVBoxLayout(self)

        # MenuBar
        self.menu_bar = QtWidgets.QMenuBar()
        self.menu_new_contact = self.menu_bar.addAction("New contact", self.new_contact)
        main_layout.setMenuBar(self.menu_bar)

        # Search input
        # As usual we thank the gods for sending us the answer
        #  http://saurabhg.com/programming/search-box-using-qlineedit/
        self.line_search = QtWidgets.QLineEdit()
        self.line_search.setFixedHeight(30)
        self.line_search.setClearButtonEnabled(True)
        self.line_search.addAction(self.icon_search, QtWidgets.QLineEdit.LeadingPosition)
        self.line_search.setPlaceholderText("Search...")
        self.line_search.textChanged.connect(self.filter_contacts)
        main_layout.addWidget(self.line_search)

        # List of contacts
        self.list_contacts = QtWidgets.QListWidget()
        self.list_contacts.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.list_contacts.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_contacts.customContextMenuRequested.connect(self.show_context_menu)

        # Populate list
        for widget in self.contact_widgets:
            self.add_item(widget)

        # If we enable sorting we get an error when we add an item without widget because list doesn't know
        #  how to compare ContactsListItem without a ContactsListWidget inside.
        #  You can't insert the widget inside the item and then insert item inside the list.
        # Qt is dumb. I'm so disappointed in this library to the point i'm questioning
        #  all my life choices that led to this moment.
        self.list_contacts.sortItems()

        main_layout.addWidget(self.list_contacts)
        main_layout.setStretch(3, 1)

        self.setLayout(main_layout)

    # We capture the closing event of the window to restore the enabled status of contact menu action.
    #  Then we propagate the event upward to the superclass.
    def closeEvent(self, event: QtGui.QCloseEvent):
        self.parent().menu_action_contacts.setEnabled(True)
        event.accept()

    @QtCore.Slot(QtCore.QPoint)
    def show_context_menu(self, pos: QtCore.QPoint):
        if item := self.list_contacts.itemAt(pos):
            menu = QtWidgets.QMenu()
            menu.addAction(self.icon_edit, "Edit", partial(self.edit_contact, item))
            menu.addAction(self.icon_delete, "Delete", partial(self.delete_contact, item))

            global_pos = self.list_contacts.mapToGlobal(pos)
            menu.exec_(global_pos)

    @QtCore.Slot(str)
    def filter_contacts(self, new_text: str):
        """
        This method show only those ContactListItems that fit the new search bar content. Hides the rest.
        """
        # I suspect this code runs in O(n^2) but haven't checked. Meh. As long as it is fast in practice there is no
        #  reason to think of a better solution.
        for i in range(self.list_contacts.count()):
            # We do matching this way because "in" operator search for exact correspondence. Instead we would like to
            #  filter all the item for with every single word matches against some part of label_name. This is because
            #  the user might look for a contact using a string that doesnt exists in any label_name.
            #  Eg.: search_text="py mo" label_name="Monty Python"
            if all([
                match.lower() in self.list_contacts.item(i).widget_name.lower() for match in new_text.split(" ")
            ]):
                self.list_contacts.item(i).setHidden(False)
            else:
                self.list_contacts.item(i).setHidden(True)

    # N.B.: The next methods that end in "_item" are only "macros" to manage items in the list
    #  to really delete a contact from persistent memory use methods that end in "_contact"

    # I know this is confusing but it makes sense to add an item but only pass a widget because the item is
    #  the same every time.
    def add_item(self, widget: ContactListWidget):
        item = ContactListItem()
        item.setSizeHint(widget.minimumSizeHint())
        self.list_contacts.addItem(item)
        self.list_contacts.setItemWidget(item, widget)

    # N.B.: Keep in mind that this method removes the widget from self.contact_widgets
    def remove_item(self, item: ContactListItem):
        self.list_contacts.takeItem(self.list_contacts.row(item))
        self.contact_widgets.remove(item.child_widget)

    @QtCore.Slot()
    def new_contact(self):
        new_contact_window = ContactsEditing(self)
        new_contact_window.exec_()
        if new_contact_window.return_value:
            new_widget = new_contact_window.return_value

            self.contacts_from_json_file.append(new_widget.contact)
            self.contact_widgets.append(new_widget)
            self.add_item(new_widget)

    @QtCore.Slot(ContactListItem)
    def edit_contact(self, item: ContactListItem):
        edit_contact_window = ContactsEditing(self, item.child_widget)
        edit_contact_window.exec_()
        if edit_contact_window.return_value:
            new_widget = edit_contact_window.return_value
            old_contact, new_contact = item.child_widget.contact, new_widget.contact

            self.remove_item(item)
            self.contacts_from_json_file.remove(item.child_widget.contact)
            if old_contact.pic_name != new_contact.pic_name:
                old_contact.release()
            self.contacts_from_json_file.append(new_contact)
            self.add_item(new_widget)

    @QtCore.Slot(ContactListItem)
    def delete_contact(self, item: ContactListItem):
        contact = item.child_widget.contact

        self.remove_item(item)
        self.contacts_from_json_file.remove(contact)
        contact.release()

    @staticmethod
    def load_contacts_json_file():
        """
        This method loads contacts.json into memory through jsonpickle parser.
        """
        try:
            if not os.path.exists(ProjectConstants.fullpath_contacts_json):
                with open(ProjectConstants.fullpath_contacts_json, 'w') as f:
                    # Create a file with an empty list that is an instance of ListJsonContacts)
                    f.write(jsonpickle.encode(ListJsonContacts(), indent='\t'))
            with open(ProjectConstants.fullpath_contacts_json) as f:
                # ContactJSONDecoder is subclassing the default JSONDecoder because it doesn't automatically
                #  know how to create a Contact instance from a dictionary
                ContactsWindow.contacts_from_json_file = jsonpickle.decode(f.read())
        except Exception as e:
            print("Could not load contacts from json file", file=stderr)
            print(e, file=stderr)
            quit()
        # Saving the hash of the list when is equal to the correspondent json file. If new hash != old hash
        #  the content gets dumped back in the disk.
        ContactsWindow.contacts_from_json_file.save_state()

    @staticmethod
    def dump_contacts_json_file():
        """
        This method dumps memory content into disk through jsonpickle parser.
        """
        try:
            with open(ProjectConstants.fullpath_contacts_json, "w") as f:
                # To encode Contact class into json object we just output the dictionary of the instance instead of
                #  the whole instance
                f.write(jsonpickle.encode(ContactsWindow.contacts_from_json_file, indent="\t"))
        except Exception as e:
            print("Could not save contacts to json file", file=stderr)
            print(e, file=stderr)


class ContactsEditing(QtWidgets.QDialog):
    """
    This class implements the window to edit / create a contact
    """
    character_pool = frozenset(ascii_letters + digits)

    @staticmethod
    def random_file_name(length: int = 16):
        """
        Returns a random string of default length = 16 with characters contained inside character_pool.
        """
        return "".join(sample(ContactsEditing.character_pool, length))

    icon_valid = QtGui.QPixmap(os.path.abspath("graphics/valid.png"))
    icon_not_valid = QtGui.QPixmap(os.path.abspath("graphics/not valid.png"))

    def __init__(self, parent: QtWidgets.QWidget, pre_filled: ContactListWidget = None):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.external_pic_full_path = None
        self.return_value = None

        self.setWindowTitle(
            "Edit contact" if pre_filled else "New contact"
        )
        self.setFixedSize(350, 320)

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addWidget(QtWidgets.QLabel("Name:"))
        self.edit_name = QtWidgets.QLineEdit()
        self.edit_name.setFixedHeight(25)
        self.edit_name.setPlaceholderText("Insert a name for your contact")
        self.edit_name_action = self.edit_name.addAction(QtGui.QIcon(), QtWidgets.QLineEdit.TrailingPosition)
        main_layout.addWidget(self.edit_name)

        main_layout.addSpacing(10)

        main_layout.addWidget(QtWidgets.QLabel("Address:"))
        self.edit_address = QtWidgets.QLineEdit()
        self.edit_address.setFixedHeight(25)
        self.edit_address.setPlaceholderText("Insert a valid Algorand address")
        self.edit_address_action = self.edit_address.addAction(QtGui.QIcon(), QtWidgets.QLineEdit.TrailingPosition)
        main_layout.addWidget(self.edit_address)

        main_layout.addSpacing(10)

        main_layout.addWidget(QtWidgets.QLabel("Photo:"))
        self.pic_name = None
        photo_layout = QtWidgets.QHBoxLayout()
        self.label_pic = QtWidgets.QLabel()
        photo_layout.addWidget(self.label_pic)

        photo_button_layout = QtWidgets.QVBoxLayout()

        self.button_pic_modify = QtWidgets.QPushButton("Change")
        self.button_pic_modify.clicked.connect(self.button_pic_modify_clicked)
        photo_button_layout.addWidget(self.button_pic_modify)

        self.button_pic_delete = QtWidgets.QPushButton("Delete")
        self.button_pic_delete.clicked.connect(self.button_pic_delete_clicked)
        photo_button_layout.addWidget(self.button_pic_delete)

        photo_layout.addLayout(photo_button_layout)

        photo_layout.addStretch(1)

        main_layout.addLayout(photo_layout)

        main_layout.addStretch(1)

        self.button_confirm = QtWidgets.QPushButton("Confirm")
        self.button_confirm.clicked.connect(self.button_confirm_clicked)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.button_confirm)

        main_layout.addLayout(button_layout)

        if pre_filled:
            self.edit_name.setText(pre_filled.name)
            self.edit_address.setText(pre_filled.info)
            self.pic_name = pre_filled.pic_name
            self.label_pic.setPixmap(pre_filled.pixmap.scaled(
                128, 128,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            ))
        else:
            self.label_pic.setPixmap(ContactListWidget.pixmap_generic_user.scaled(
                128, 128,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            ))

        if not self.pic_name:
            self.button_pic_delete.setEnabled(False)

        self.edit_name.textChanged.connect(self.validate_inputs)
        self.edit_address.textChanged.connect(self.validate_inputs)
        self.validate_inputs()

        self.setLayout(main_layout)

    @QtCore.Slot()
    def validate_inputs(self):
        """
        This method makes sure inputs are valid. Otherwise confirm button is disabled.
        """
        name_state = self.edit_name.text() != ""
        address_state = is_valid_address(self.edit_address.text())

        name_state, address_state = True, True

        self.edit_name.removeAction(self.edit_name_action)
        if name_state:
            self.edit_name_action = self.edit_name.addAction(
                QtGui.QIcon(self.icon_valid), QtWidgets.QLineEdit.TrailingPosition
            )
        else:
            self.edit_name_action = self.edit_name.addAction(
                QtGui.QIcon(self.icon_not_valid), QtWidgets.QLineEdit.TrailingPosition
            )

        self.edit_address.removeAction(self.edit_address_action)
        if address_state:
            self.edit_address_action = self.edit_address.addAction(
                QtGui.QIcon(self.icon_valid), QtWidgets.QLineEdit.TrailingPosition
            )
        else:
            self.edit_address_action = self.edit_address.addAction(
                QtGui.QIcon(self.icon_not_valid), QtWidgets.QLineEdit.TrailingPosition
            )

        # Disable button if any of those two conditions is False. Enable otherwise.
        self.button_confirm.setEnabled(name_state and address_state)

    @QtCore.Slot()
    def button_pic_modify_clicked(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Choose a picture for contact thumbnail",
            os.path.join(os.path.expanduser("~"), "Pictures"),
            "Image Files (*.png *.jpg *.bmp)"
        )
        if file_name[0] != "":
            self.external_pic_full_path = file_name[0]
            self.label_pic.setPixmap(QtGui.QPixmap(file_name[0]).scaled(
                128, 128,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            ))

            self.button_pic_delete.setEnabled(True)

    @QtCore.Slot()
    def button_pic_delete_clicked(self):
        self.external_pic_full_path = None
        self.pic_name = None
        self.label_pic.setPixmap(ContactListWidget.pixmap_generic_user.scaled(
            128, 128,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        ))
        self.button_pic_delete.setEnabled(False)

    @QtCore.Slot()
    def button_confirm_clicked(self):
        if self.external_pic_full_path:
            old_extension = "." + self.external_pic_full_path.split(".")[-1]
            while True:
                rnd_file_name = self.random_file_name() + old_extension
                if not os.path.exists(os.path.join(ProjectConstants.fullpath_thumbnails, rnd_file_name)):
                    break
            copyfile(
                self.external_pic_full_path,
                os.path.join(ProjectConstants.fullpath_thumbnails, rnd_file_name)
            )
            pic_name = rnd_file_name
        else:
            pic_name = self.pic_name
        self.return_value = ContactListWidget(Contact(pic_name, self.edit_name.text(), self.edit_address.text()))
        self.close()
