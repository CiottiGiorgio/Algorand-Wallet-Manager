from PyQt5 import QtWidgets, QtGui, QtCore
from resources.CustomListWidgetItem import ContactListItem, ContactListWidget
from os import path, remove


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
        self.menu_new_contact = self.menu_bar.addAction("New contact")

        self.menu_new_contact.setDisabled(True)

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

        for widget in self.contact_widgets:
            item = ContactListItem()
            item.setSizeHint(widget.minimumSizeHint())
            self.list_contacts.addItem(item)
            self.list_contacts.setItemWidget(item, widget)

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
            menu_edit = menu.addAction(self.icon_edit, "Edit", lambda: None)
            menu_delete = menu.addAction(self.icon_delete, "Delete", lambda: self.delete_contact(item))

            menu_edit.setDisabled(True)

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

    # We remove the item from the list and we delete the widget contained inside from self.contact_widgets
    def delete_contact(self, item):
        row = self.list_contacts.row(item)
        widget = self.list_contacts.itemWidget(item)
        pic_name = widget.extrapolate()[0]
        self.list_contacts.takeItem(row)
        self.contact_widgets.remove(widget)
        if pic_name:
            remove(path.join(path.expanduser("~"), ".Algorand Wallet Manager/thumbnails", pic_name))

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
