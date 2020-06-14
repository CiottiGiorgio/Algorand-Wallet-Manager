from PyQt5 import QtWidgets, QtGui, QtCore
from resources.CustomListWidgetItem import ContactListItem, ContactListWidget
from algosdk.encoding import is_valid_address
from os import path, remove
from functools import partial


class ContactsWindow(QtWidgets.QWidget):
    # Static loading of graphic resources
    # This is not done because there will be multiple instances of this class but rather to avoid loading
    #  this icon every time the user opens Contacts window
    icon_search = QtGui.QIcon(path.abspath("graphics/search.png"))
    icon_edit = QtGui.QIcon(path.abspath("graphics/edit.png"))
    icon_delete = QtGui.QIcon(path.abspath("graphics/delete.png"))

    # We make a list of ContactListItem static because each item has an image that could create IO bottleneck
    #  if it has to be loaded each time the window starts for every contact in the list
    contact_widgets = list()

    def __init__(self, parent):
        # This line is necessary because a widget gets it's own window if it doesn't have a parent OR
        #  if it has a parent but has QtCore.Qt.Window flag set
        super().__init__(parent, QtCore.Qt.Window)

        # Initialize list of ContactListItem
        if not self.contact_widgets:
            for contact in self.parent().contacts_from_json_file:
                widget = ContactListWidget(*contact)
                self.contact_widgets.append(widget)

        # Title, window size & position
        self.setWindowTitle("Contacts")
        width, height = 350, 550
        parent_size = self.parent().size()
        self.setFixedSize(width, height)
        # With this next line we spawn the ContactWindow 50 pixels distant from parent in x axis and
        #  we align the centers of the two window losing half of the difference in height on the longer window.
        self.move(self.parent().pos() +
                  QtCore.QPoint(parent_size.width() + 50, -1 * (height - parent_size.height())//2))

        # Main Layout
        main_layout = QtWidgets.QVBoxLayout(self)

        # MenuBar
        self.menu_bar = QtWidgets.QMenuBar()
        self.menu_new_contact = self.menu_bar.addAction("New contact", partial(self.new_contact))

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

        # Contacts "list" (more like a vertical layout scrollable)
        self.list_contacts = QtWidgets.QListWidget()
        self.list_contacts.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.list_contacts.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_contacts.customContextMenuRequested.connect(self.show_context_menu)

        self.add_contact(self.contact_widgets)

        # If we enable sorting it gets an error when we add an item without widget yet because list doesn't know
        #  how to compare items without a widget. You can't insert the widget inside the item and then insert item
        #  inside list. Qt is dumb. I'm so disappointed in this library to the point i'm questioning
        #  all my life choices that led to this moment.
        self.list_contacts.sortItems()

        main_layout.addWidget(self.list_contacts)
        main_layout.setStretch(3, 1)

        self.setLayout(main_layout)

    # We capture the closing event of the window to restore the enabled status of contact menu action.
    #  Then we propagate the event upward to the parent.
    def closeEvent(self, a0):
        self.parent().menu_contacts.setEnabled(True)
        a0.accept()

    # PyQt5 slot to create a custom context menu on an item in self.contacts_list
    @QtCore.pyqtSlot(QtCore.QPoint)
    def show_context_menu(self, pos):
        if item := self.list_contacts.itemAt(pos):
            menu = QtWidgets.QMenu()
            menu.addAction(self.icon_edit, "Edit", partial(self.edit_contact, item))
            menu.addAction(self.icon_delete, "Delete", partial(self.delete_contact, item))

            global_pos = self.list_contacts.mapToGlobal(pos)
            menu.exec(global_pos)

    # PyQt5 slot to hide and show items that are filtered through search bar
    @QtCore.pyqtSlot(str)
    def filter_contacts(self, new_text):
        for i in range(self.list_contacts.count()):
            # We do matching this way because "in" operator search for exact correspondence. Instead we would like to
            #  filter all the item for with every single word matches against some part of label_name. This is because
            #  the user might look for a contact using a string that doesnt exists in any label_name.
            #  Eg.: search_text="py mo" label_name="Monty Python"
            if all([
                match.lower() in self.list_contacts.item(i).label_name.lower() for match in new_text.split(" ")
            ]):
                self.list_contacts.item(i).setHidden(False)
            else:
                self.list_contacts.item(i).setHidden(True)

    def new_contact(self):
        edit_window = ContactsEditing(self)
        edit_window.exec()
        if edit_window.return_value:
            self.contact_widgets.append(edit_window.return_value)
            self.add_contact(edit_window.return_value)

    def edit_contact(self, item):
        edit_window = ContactsEditing(self, item)
        edit_window.exec()
        if edit_window.return_value:
            self.delete_contact(item)
            self.contact_widgets.append(edit_window.return_value)
            self.add_contact(edit_window.return_value)

    # Adds a list of widgets in order to do bulk insert and call self.update_json_contacts just one time
    def add_contact(self, widgets):
        if not isinstance(widgets, list):
            widgets = [widgets]

        for widget in widgets:
            item = ContactListItem()
            item.setSizeHint(widget.minimumSizeHint())
            self.list_contacts.addItem(item)
            self.list_contacts.setItemWidget(item, widget)

        self.update_json_contacts()

        # In this case we need to re-sort the list
        self.list_contacts.sortItems()

    # We remove the item from the list and we delete the widget contained inside from self.contact_widgets
    def delete_contact(self, item):
        # Saving internally reference to item in list and to widget in item
        row = self.list_contacts.row(item)
        widget = item.child_widget

        # Saving pic_name before deleting widget to delete pic from hard disk
        pic_name = widget.extrapolate()[0]

        # Deleting item from list and deleting widget from contact_widgets
        self.list_contacts.takeItem(row)
        self.contact_widgets.remove(widget)
        if pic_name:
            remove(path.join(path.expanduser("~"), ".Algorand Wallet Manager/thumbnails", pic_name))

        # Update json inside parent memory
        self.update_json_contacts()

        # We don't need to re-sort the list because a delete doesn't change a correct sorting

    # This method makes sure that any change in self.contact_widgets is reflected in parent().contacts_from_json
    def update_json_contacts(self):
        temp_list = list()

        for i in range(self.list_contacts.count()):
            temp_list.append(
                self.list_contacts.itemWidget(self.list_contacts.item(i)).extrapolate()
            )

        self.parent().contacts_from_json_file = temp_list


class ContactsEditing(QtWidgets.QDialog):
    icon_valid = QtGui.QPixmap(path.abspath("graphics/valid.png"))
    icon_not_valid = QtGui.QPixmap(path.abspath("graphics/not valid.png"))

    def __init__(self, parent, pre_filled=None):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.return_value = None

        self.setWindowTitle(
            "Edit contact" if pre_filled else "New contact"
        )
        self.setFixedSize(300, 300)

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addWidget(QtWidgets.QLabel("Name:"))
        self.edit_name = QtWidgets.QLineEdit()
        self.edit_name.setFixedHeight(25)
        self.edit_name_action = self.edit_name.addAction(QtGui.QIcon(), QtWidgets.QLineEdit.TrailingPosition)
        main_layout.addWidget(self.edit_name)

        main_layout.addSpacing(10)

        main_layout.addWidget(QtWidgets.QLabel("Address:"))
        self.edit_address = QtWidgets.QLineEdit()
        self.edit_address.setFixedHeight(25)
        self.edit_address_action = self.edit_name.addAction(QtGui.QIcon(), QtWidgets.QLineEdit.TrailingPosition)
        main_layout.addWidget(self.edit_address)

        main_layout.addSpacing(10)

        main_layout.addWidget(QtWidgets.QLabel("Photo:"))
        self.label_pic = QtWidgets.QLabel()
        main_layout.addWidget(self.label_pic)

        main_layout.addStretch(1)

        self.button_ok = QtWidgets.QPushButton("OK")
        self.button_ok.clicked.connect(self.button_ok_clicked)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.button_ok)

        main_layout.addLayout(button_layout)

        if pre_filled:
            self.edit_name.setText(pre_filled.widget_name)
            self.edit_address.setText(pre_filled.widget_info)
            self.label_pic.setPixmap(pre_filled.widget_pixmap)
        else:
            self.label_pic.setPixmap(ContactListWidget.pixmap_generic_user)

        self.edit_name.textChanged.connect(self.validate_inputs)
        self.edit_address.textChanged.connect(self.validate_inputs)
        self.validate_inputs()

        self.setLayout(main_layout)

    @QtCore.pyqtSlot(str)
    def validate_inputs(self):
        name_state = self.edit_name.text() != ""
        address_state = is_valid_address(self.edit_address.text())

        self.edit_name.removeAction(self.edit_name_action)
        if name_state:
            self.edit_name_action = self.edit_name.addAction(
                QtGui.QIcon(self.icon_valid), QtWidgets.QLineEdit.LeadingPosition
            )
        else:
            self.edit_name_action = self.edit_name.addAction(
                QtGui.QIcon(self.icon_not_valid), QtWidgets.QLineEdit.LeadingPosition
            )

        self.edit_address.removeAction(self.edit_address_action)
        if address_state:
            self.edit_address_action = self.edit_address.addAction(
                QtGui.QIcon(self.icon_valid), QtWidgets.QLineEdit.LeadingPosition
            )
        else:
            self.edit_address_action = self.edit_address.addAction(
                QtGui.QIcon(self.icon_not_valid), QtWidgets.QLineEdit.LeadingPosition
            )

        if name_state and address_state:
            self.button_ok.setEnabled(True)
        else:
            self.button_ok.setEnabled(False)

    @QtCore.pyqtSlot()
    def button_ok_clicked(self):
        self.return_value = ContactListWidget(None, self.edit_name.text(), self.edit_address.text())
        self.close()
