"""
Custom classes for QListWidget in ContactsWindow.

Subclass of QWidget is the actual representation.
Subclass of QListWidgetItem is the item that goes into the list and holds the space for the widget.
It also offers functionality for the ordering of the items inside ContactsWindow contact list.
"""


# PySide 2
from PySide2 import QtWidgets, QtGui, QtCore

# Local project
import misc.Constants as ProjectConstants
from misc.Entities import Contact

# Python standard libraries
from functools import cached_property
from os import path


# Of course once a ContactListWidget has been assigned to a ContactListItem it's wrong to swap with a
#  second ContactListWidget because then the cached properties will be incoherent.
class ContactListItem(QtWidgets.QListWidgetItem):
    """
    Item used in the contacts list.

    Most of its features are only available when a ContactListWidget is inside it.
    """
    def __lt__(self, other):
        return self.child_widget < other.child_widget

    @cached_property
    def child_widget(self):
        # This is dumb as hell. You can't do something like .child() on QListWidgetItem. You have to go back to the
        #  entire list and reference yourself as the item and then retrieve the widget contained in self.
        return self.listWidget().itemWidget(self)

    # This changes the method into being an attribute that is only computed the first time.
    # This is made under the assumption that the widget inside a given item doesn't change.
    # This will be useful for dynamically filtering search bar.
    @cached_property
    def widget_name(self):
        return self.child_widget.name

    @cached_property
    def widget_info(self):
        return self.child_widget.info

    @cached_property
    def widget_pic_name(self):
        return self.child_widget.pic_name

    @cached_property
    def widget_pixmap(self):
        return self.child_widget.pixmap


class ContactListWidget(QtWidgets.QWidget):
    """
    This widget represents a contact inside ContactWindow.
    """
    pixmap_generic_user = QtGui.QPixmap(path.abspath("graphics/generic_user.png"))
    bitmap_user_mask = QtGui.QBitmap.fromImage(QtGui.QImage(path.abspath("graphics/user_pic_mask.png")))

    def __init__(self, contact: Contact):
        super().__init__()

        # We might need to extract this reference to the contact when we want to delete the contact and not just
        #  the widget.
        self.contact = contact

        self.pic_name = contact.pic_name
        self.name = contact.name
        self.info = contact.info
        self.pixmap = QtGui.QPixmap(
            path.join(ProjectConstants.path_user_data, ProjectConstants.folder_thumbnails, self.contact.pic_name)) if \
            self.pic_name else \
            self.pixmap_generic_user

        # Setup interface
        main_layout = QtWidgets.QHBoxLayout(self)

        self.label_pixmap = QtWidgets.QLabel()
        self.label_pixmap.setPixmap(self.derive_profile_pic(self.pixmap))
        main_layout.addWidget(self.label_pixmap)

        main_layout.addSpacing(5)

        main_layout.addLayout(label_layout := QtWidgets.QVBoxLayout())

        #   Name label
        self.label_name = QtWidgets.QLabel(self.name)
        self.label_name.setStyleSheet("font: 13pt;")
        label_layout.addWidget(self.label_name)

        #   Info label
        self.label_info = QtWidgets.QLabel(self.info)
        self.label_info.setStyleSheet("font: 8pt;")
        label_layout.addWidget(self.label_info)

        main_layout.addStretch(1)
        # End setup

    def __lt__(self, other) -> bool:
        return self.name < other.name

    @staticmethod
    def derive_profile_pic(pixmap: QtGui.QPixmap) -> QtGui.QPixmap:
        """
        This method returns the icon for the profile picture starting from a full picture.
        """
        # Crop a the maximum square possible from the middle of the QPixmap.
        width, height = pixmap.width(), pixmap.height()
        side = min(width, height)
        square_top_left_corner = QtCore.QPoint(width//2 - side//2, height//2 - side//2)
        cropping_rect = QtCore.QRect(square_top_left_corner, QtCore.QSize(side, side))
        result = pixmap.copy(cropping_rect)

        # Clipping a circle
        temp_mask = ContactListWidget.bitmap_user_mask.scaled(
            side, side,
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        result.setMask(temp_mask)

        return result.scaled(40, 40, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
