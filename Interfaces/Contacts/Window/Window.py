"""
This file describes the contact window, its child widgets and some data structure needed.
"""


# PySide 2
from PySide2 import QtWidgets, QtGui, QtCore

# Local project
from misc.DataStructures import ListJsonContacts
from Interfaces.Contacts.Window.Ui_Window import Ui_ContactsWindow
from Interfaces.Contacts.ManageContact.ContactManaging import ContactManaging
from Interfaces.Contacts.Widgets import ContactListItem, ContactListWidget

# Python standard libraries
import os
from functools import partial


class ContactsWindow(QtWidgets.QDialog, Ui_ContactsWindow):
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

        self.setupUi(self)

        self.listWidget.set_item_type(ContactListItem)

        # Setup interface
        #   MenuBar
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBarAction = self.menuBar.addAction("New contact")
        self.verticalLayout.setMenuBar(self.menuBar)
        self.menuBar.setNativeMenuBar(False)

        #   Search bar
        self.lineEdit.addAction(self.icon_search, QtWidgets.QLineEdit.LeadingPosition)
        # End setup

        # Connections
        self.lineEdit.textChanged.connect(self.filter_contacts)
        self.listWidget.customContextMenuRequested.connect(self.show_context_menu)
        self.menuBarAction.triggered.connect(self.new_contact)

        QtCore.QTimer.singleShot(0, self.setup_logic)

    def setup_logic(self):
        # Populate contact_widgets with info from json file.
        if not ContactsWindow.contact_widgets:
            for contact in ContactsWindow.contacts_from_json_file.memory:
                ContactsWindow.contact_widgets.append(ContactListWidget(contact))

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
        item = self.listWidget.itemAt(pos)
        if item:
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
        new_contact_window = ContactManaging(self)

        if new_contact_window.exec_() == QtWidgets.QDialog.Accepted:
            new_widget = new_contact_window.return_value

            self.contacts_from_json_file.memory.append(new_widget.contact)
            self.contact_widgets.append(new_widget)
            self.listWidget.add_widget(new_widget)

        self.listWidget.sortItems()

    @QtCore.Slot(ContactListItem)
    def edit_contact(self, item: ContactListItem):
        edit_contact_window = ContactManaging(self, self.listWidget.itemWidget(item))

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

        self.listWidget.sortItems()

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
