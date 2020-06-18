from PySide2 import QtWidgets, QtGui, QtCore
from resources.CustomListWidgetItem import ContactListItem, ContactListWidget
from algosdk.encoding import is_valid_address
from os import path, remove
from shutil import copyfile
from string import ascii_letters, digits
from random import sample
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
    @QtCore.Slot(QtCore.QPoint)
    def show_context_menu(self, pos):
        if item := self.list_contacts.itemAt(pos):
            menu = QtWidgets.QMenu()
            menu.addAction(self.icon_edit, "Edit", partial(self.edit_contact, item))
            menu.addAction(self.icon_delete, "Delete", partial(self.delete_contact, item))

            global_pos = self.list_contacts.mapToGlobal(pos)
            menu.exec_(global_pos)

    # PyQt5 slot to hide and show items that are filtered through search bar
    @QtCore.Slot(str)
    def filter_contacts(self, new_text):
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

    def new_contact(self):
        edit_window = ContactsEditing(self)
        edit_window.exec_()
        if edit_window.return_value:
            self.contact_widgets.append(edit_window.return_value)
            self.add_contact(edit_window.return_value)

    def edit_contact(self, item):
        edit_window = ContactsEditing(self, item)
        edit_window.exec_()
        if edit_window.return_value:
            self.delete_contact(
                item,
                True if item.widget_pic_name != edit_window.return_value.contact_pic_name else False
            )
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
    def delete_contact(self, item, delete_thumbnail=True):
        # Saving internally reference to item in list and to widget in item
        row = self.list_contacts.row(item)
        widget = item.child_widget

        # Saving pic_name before deleting widget to delete pic from hard disk
        pic_name = widget.extrapolate()[0]

        # Deleting item from list and deleting widget from contact_widgets
        self.list_contacts.takeItem(row)
        self.contact_widgets.remove(widget)
        if pic_name and delete_thumbnail:
            remove(path.join(ContactListWidget.contact_pic_path, pic_name))

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
    @staticmethod
    def random_file_name(length=16):
        character_pool = frozenset(ascii_letters + digits)
        return "".join(sample(character_pool, length))

    icon_valid = QtGui.QPixmap(path.abspath("graphics/valid.png"))
    icon_not_valid = QtGui.QPixmap(path.abspath("graphics/not valid.png"))

    def __init__(self, parent, pre_filled=None):
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
            self.edit_name.setText(pre_filled.widget_name)
            self.edit_address.setText(pre_filled.widget_info)
            self.pic_name = pre_filled.widget_pic_name
            self.label_pic.setPixmap(pre_filled.widget_pixmap.scaled(
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

    @QtCore.Slot(str)
    def validate_inputs(self):
        name_state = self.edit_name.text() != ""
        address_state = is_valid_address(self.edit_address.text())

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
            path.join(path.expanduser("~"), "Pictures"),
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
                if not path.exists(path.join(ContactListWidget.contact_pic_path, rnd_file_name)):
                    break
            copyfile(self.external_pic_full_path, path.join(ContactListWidget.contact_pic_path, rnd_file_name))
            pic_name = rnd_file_name
        else:
            pic_name = self.pic_name
        self.return_value = ContactListWidget(pic_name, self.edit_name.text(), self.edit_address.text())
        self.close()
