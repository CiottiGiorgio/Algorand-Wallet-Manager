"""
This file describes the contact window, its child widgets and some data structure needed.
"""


# PySide 2
from PySide2 import QtWidgets, QtGui, QtCore

# Algorand
from algosdk.encoding import is_valid_address

# Local project
import misc.Constants as ProjectConstants
from misc.DataStructures import ListJsonContacts
from misc.Entities import Contact
from Interfaces.Contacts.Ui_Contacts import Ui_Contacts
from Interfaces.Contacts.Ui_ContactsCreating import Ui_ContactsCreating
from Interfaces.Contacts.Widgets import ContactListItem, ContactListWidget

# Python standard libraries
import os
from os import path
from shutil import copyfile
from string import ascii_letters, digits
from random import sample
from functools import partial


class ContactsWindow(QtWidgets.QDialog, Ui_Contacts):
    """
    This class is the contact window.

    This class also manage all information about contacts. It will load at the start of the program all permanent
    information about user contacts so that other classes that need those information will find it here.
    """
    # These icons are static because we want to avoid having to reload them from the disk each time this class is
    #  instantiated.
    icon_search = QtGui.QIcon(os.path.abspath("graphics/search.png"))
    icon_edit = QtGui.QIcon(os.path.abspath("graphics/edit.png"))
    icon_delete = QtGui.QIcon(os.path.abspath("graphics/delete.png"))

    # This list will host the content of the contacts.json file. This is static because other classes might need to
    #  read contacts and create their own widgets.
    #  However this class will be the only one to load it and change it. Other classes shall only read from it.
    # A crucial point is that this list gets loaded with the static method load_contacts_json_file as soon as this
    #  class is done with the definition because other class might need its data even if this class never
    #  gets instantiated.
    contacts_from_json_file = ListJsonContacts()

    # We make a list of ContactListWidget static because each item has a profile pic that could create IO bottleneck
    #  if it has to be loaded each time this class is instantiated.
    # However we create the list of widget for Contacts only the first time that this class is
    #  instantiated because only this class needs its ContactListWidget.
    # This list remains coherent with contacts_from_json_file and DOES NOT need to be fully updated as long as
    #  contacts are managed through this class methods.
    contact_widgets = list()

    def __init__(self, parent: QtWidgets.QWidget):
        # This line is necessary because a widget gets it's own window if it doesn't have a parent OR
        #  if it has a parent but has QtCore.Qt.Window flag set.
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Populate contact_widgets with info from json file.
        if not self.contact_widgets:
            for contact in self.contacts_from_json_file.memory:
                self.contact_widgets.append(ContactListWidget(contact))

        self.setupUi(self)

        self.listWidget.set_item_type(ContactListItem)

        # Setup interface
        #   MenuBar
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBarAction = self.menuBar.addAction("New contact")
        self.verticalLayout.setMenuBar(self.menuBar)

        #   Search bar
        self.lineEdit.addAction(self.icon_search, QtWidgets.QLineEdit.LeadingPosition)
        # End setup

        # Connections
        self.lineEdit.textChanged.connect(self.filter_contacts)
        self.listWidget.customContextMenuRequested.connect(self.show_context_menu)
        self.menuBarAction.triggered.connect(self.new_contact)

        # Populate list
        for widget in self.contact_widgets:
            self.listWidget.add_widget(widget)

        # If we enable sorting we get an error when we add an item without widget because list doesn't know
        #  how to compare ContactsListItem without a ContactsListWidget inside.
        #  You can't insert the widget inside the item and then insert item inside the list.
        self.listWidget.sortItems()

    def closeEvent(self, arg__1: QtGui.QCloseEvent):
        # If we don't do this the widgets get deleted from their parent when the window closes.
        #  Typically this would be fine but since we are storing the widgets statically we don't want them deleted.
        for contact in ContactsWindow.contact_widgets:
            contact.setParent(None)

        arg__1.accept()

    @QtCore.Slot(QtCore.QPoint)
    def show_context_menu(self, pos: QtCore.QPoint):
        if item := self.listWidget.itemAt(pos):
            widget = self.listWidget.itemWidget(item)

            menu = QtWidgets.QMenu(self)
            menu.addAction(self.icon_edit, "Edit", partial(self.edit_contact, item))
            menu.addAction(self.icon_delete, "Delete", partial(self.delete_contact, item))
            menu.addAction("Copy address to clipboard", partial(
                QtGui.QGuiApplication.clipboard().setText, widget.contact.info)
            )

            global_pos = self.listWidget.mapToGlobal(pos)
            menu.exec_(global_pos)

            # This should get rid of the whole object along with the partial.
            menu.deleteLater()

    @QtCore.Slot(str)
    def filter_contacts(self, new_text: str):
        """
        This method show only those ContactListItems that fit the new search bar content. Hides the rest.
        """
        new_text_splitted = new_text.split(' ')

        # TODO right now if the user inputs the same word twice it gets mapped to the same word in the contact
        #  This makes no sense. There should be a bijection between the word typed and substrings in the name.
        for i in range(self.listWidget.count()):
            # We do matching this way because "in" operator search for exact correspondence. Instead we would like to
            #  filter all the item for which every single word matches against some part of label_name. This is because
            #  the user might look for a contact using a string that doesnt exists in any label_name.
            #  Eg.: search_text="py mo" label_name="Monty Python"
            # This is a slightly convoluted way to split the search text into bits separated by space then math each
            #  of these bits against the widget name. (Both strings get lowered of course)
            #  Then if every bit matches the item is shown otherwise is hidden.
            widget = self.listWidget.itemWidget(self.listWidget.item(i))
            if all([
                match.lower() in widget.contact.name.lower() for match in new_text_splitted
            ]):
                self.listWidget.item(i).setHidden(False)
            else:
                self.listWidget.item(i).setHidden(True)

    @QtCore.Slot()
    def new_contact(self):
        new_contact_window = ContactsCreating(self)

        if new_contact_window.exec_() == QtWidgets.QDialog.Accepted:
            new_widget = new_contact_window.return_value

            self.contacts_from_json_file.memory.append(new_widget.contact)
            self.contact_widgets.append(new_widget)
            self.listWidget.add_widget(new_widget)

    @QtCore.Slot(ContactListItem)
    def edit_contact(self, item: ContactListItem):
        edit_contact_window = ContactsCreating(self, self.listWidget.itemWidget(item))

        if edit_contact_window.exec_() == QtWidgets.QDialog.Accepted:
            old_widget, new_widget = self.listWidget.itemWidget(item), edit_contact_window.return_value
            old_contact, new_contact = old_widget.contact, new_widget.contact

            self.remove_item(item)
            self.contacts_from_json_file.memory.remove(old_contact)
            if old_contact.pic_name != new_contact.pic_name:
                old_contact.release()
            self.contacts_from_json_file.memory.append(new_contact)
            ContactsWindow.contact_widgets.append(new_widget)
            self.listWidget.add_widget(new_widget)

    @QtCore.Slot(ContactListItem)
    def delete_contact(self, item: ContactListItem):
        contact = self.listWidget.itemWidget(item).contact

        self.remove_item(item)
        self.contacts_from_json_file.memory.remove(contact)
        contact.release()

    # N.B.: The next method that end in "_item" is only "macro" to manage items in the list
    #  to really delete a contact from persistent memory use methods that end in "_contact".
    def remove_item(self, item: ContactListItem):
        widget = self.listWidget.itemWidget(item)

        self.listWidget.takeItem(self.listWidget.row(item))
        ContactsWindow.contact_widgets.remove(widget)


class ContactsCreating(QtWidgets.QDialog, Ui_ContactsCreating):
    """
    This class implements the window to edit / create a contact.
    """
    character_pool = frozenset(ascii_letters + digits)

    @staticmethod
    def random_file_name(length: int = 16):
        """
        Returns a random string of default length = 16 with characters contained inside character_pool.
        """
        return "".join(sample(ContactsCreating.character_pool, length))

    # Static images to avoid IO bottleneck
    icon_valid = QtGui.QPixmap(os.path.abspath("graphics/valid.png"))
    icon_not_valid = QtGui.QPixmap(os.path.abspath("graphics/not_valid.png"))

    def __init__(self, parent: QtWidgets.QWidget, pre_filled: ContactListWidget = None):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # This value is set if the user selects a new picture.
        self.external_pic_full_path = None

        # This value holds the new ContactListWidget that will be read from ContactsWindow.
        self.return_value = None

        self.setupUi(self)

        # Setup interface
        self.lineEditAction_name = self.lineEdit_name.addAction(
            QtGui.QIcon(), QtWidgets.QLineEdit.TrailingPosition
        )
        self.lineEditAction_address = self.lineEdit_address.addAction(
            QtGui.QIcon(), QtWidgets.QLineEdit.TrailingPosition
        )
        self.set_label_pixmap(ContactListWidget.pixmap_generic_user)

        # Initial state
        if pre_filled:
            self.setWindowTitle("Edit contact")
            self.lineEdit_name.setText(pre_filled.contact.name)
            self.lineEdit_address.setText(pre_filled.contact.info)
            if pre_filled.contact.pic_name:
                self.set_label_pixmap(
                    QtGui.QPixmap(path.join(ProjectConstants.fullpath_thumbnails, pre_filled.contact.pic_name))
                )
                self.pushButton_delete.setEnabled(True)

        # Connections
        self.pushButton_change.clicked.connect(self.pushbutton_modify)
        self.pushButton_delete.clicked.connect(self.pushbutton_delete)
        self.lineEdit_name.textChanged.connect(self.validate_inputs)
        self.lineEdit_address.textChanged.connect(self.validate_inputs)

        self.validate_inputs()

    @QtCore.Slot()
    def accept(self):
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
            new_pic_name = rnd_file_name
        else:
            new_pic_name = self.contact.pic_name
        self.return_value = ContactListWidget(
            Contact(new_pic_name, self.lineEdit_name.text(), self.lineEdit_address.text())
        )

        super().accept()

    @QtCore.Slot()
    def validate_inputs(self):
        """
        This method makes sure inputs are valid.

        Action icon on each QLineEdit is changed accordingly and Ok button is enabled accordingly.
        """
        name_state = self.lineEdit_name.text() != ""
        address_state = is_valid_address(self.lineEdit_address.text())

        self.lineEditAction_name.setIcon(
            self.icon_valid if name_state else self.icon_not_valid
        )

        self.lineEditAction_address.setIcon(
            self.icon_valid if address_state else self.icon_not_valid
        )

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(
            name_state and address_state
        )

    @QtCore.Slot()
    def pushbutton_modify(self):
        # This static function always return a pair (file name, file type). If the operation is aborted both are == "".
        #  They are non empty otherwise.
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Choose a picture for contact thumbnail",
            os.path.join(os.path.expanduser("~"), "Pictures"),
            "Image Files (*.png *.jpg *.bmp)"
        )
        if file_name[0] != "":
            self.external_pic_full_path = file_name[0]
            self.set_label_pixmap(QtGui.QPixmap(file_name[0]))

            self.pushButton_delete.setEnabled(True)

    @QtCore.Slot()
    def pushbutton_delete(self):
        self.external_pic_full_path = None
        self.set_label_pixmap(ContactListWidget.pixmap_generic_user)
        self.pushButton_delete.setEnabled(False)

    def set_label_pixmap(self, pixmap: QtGui.QPixmap):
        picture_size = pixmap.size()
        label_max_size = self.label_picture.maximumSize()

        self.label_picture.setPixmap(
            pixmap
            if picture_size.width() < label_max_size.width() and picture_size.height() < label_max_size.height() else
            pixmap.scaled(
                label_max_size,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
        )
