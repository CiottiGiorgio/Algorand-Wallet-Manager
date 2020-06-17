from PySide2 import QtWidgets, QtGui
from functools import cached_property
from os import path

# TODO: credit author with
#  "Icon made by "Freepik", "Those Icons", "Pixel perfect" from www.flaticon.com"


class WalletListItem(QtWidgets.QListWidgetItem):
    pass
    # Empty class just in case


class WalletListWidget(QtWidgets.QWidget):
    def __init__(self, wallet_name, wallet_info):
        super().__init__()

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 5)

        # Here the inner layout is created inside addLayout but also is assigned to label_layout using walrus operator.
        main_layout.addLayout(label_layout := QtWidgets.QVBoxLayout())

        # Here the label with the name of the wallet is created, styled and added to the window
        self.label_name = QtWidgets.QLabel(wallet_name)
        self.label_name.setStyleSheet("font: 13pt;")
        label_layout.addWidget(self.label_name)

        # Same for the info label
        self.label_info = QtWidgets.QLabel(wallet_info)
        self.label_info.setStyleSheet("font: 8pt;")
        label_layout.addWidget(self.label_info)

        main_layout.addStretch(1)

        self.setLayout(main_layout)


# Of course once a ContactListWidget has been assigned to a ContactListItem it's wrong to swap with a
#  second ContactListWidget becuase then the cached properties will be different
class ContactListItem(QtWidgets.QListWidgetItem):
    def __lt__(self, other):
        return self.child_widget < other.child_widget

    @cached_property
    def child_widget(self):
        # This is dumb as hell. You can't do something like .child() on QListWidgetItem. You have to go back to the
        #  entire list and reference yourself as the item and then retrieve the widget contained in self.
        return self.listWidget().itemWidget(self)

    # This changes the method into being an attribute that is only computed the first time.
    # This is made under the assumption that the widget inside a given item doesn't change.
    # This will be useful for dynamic filtering with search bar.
    @cached_property
    def widget_name(self):
        return self.child_widget.label_name.text()

    @cached_property
    def widget_info(self):
        return self.child_widget.label_info.text()

    @cached_property
    def widget_pixmap(self):
        return self.child_widget.label_pixmap.pixmap()


class ContactListWidget(QtWidgets.QWidget):
    # Static loading of graphic resources
    pixmap_generic_user = QtGui.QPixmap(path.abspath("graphics/generic_user.png")).scaled(30, 30)

    contact_pic_path = path.join(path.expanduser("~"), ".Algorand Wallet Manager/thumbnails")

    def __init__(self, contact_pic_name, contact_name, contact_info):
        super().__init__()

        self.contact_pic_name = contact_pic_name

        main_layout = QtWidgets.QHBoxLayout()

        self.label_pixmap = QtWidgets.QLabel()
        self.label_pixmap.setPixmap(QtGui.QPixmap(path.join(self.contact_pic_path, self.contact_pic_name)).scaled(30, 30)
                                    if contact_pic_name else
                                    self.pixmap_generic_user)
        main_layout.addWidget(self.label_pixmap)

        main_layout.addSpacing(5)

        main_layout.addLayout(label_layout := QtWidgets.QVBoxLayout())

        self.label_name = QtWidgets.QLabel(contact_name)
        self.label_name.setStyleSheet("font: 13pt;")
        label_layout.addWidget(self.label_name)

        self.label_info = QtWidgets.QLabel(contact_info)
        self.label_info.setStyleSheet("font: 8pt;")
        label_layout.addWidget(self.label_info)

        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def __lt__(self, other):
        return self.label_name.text() < other.label_name.text()

    def extrapolate(self):
        return self.contact_pic_name, self.label_name.text(), self.label_info.text()
