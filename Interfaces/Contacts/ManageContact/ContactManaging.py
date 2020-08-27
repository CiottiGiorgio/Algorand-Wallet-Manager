# PySide 2
from PySide2 import QtWidgets, QtGui, QtCore

# Algorand
from algosdk.encoding import is_valid_address

# Local project
import misc.Constants as ProjectConstants
from misc.Entities import Contact
from Interfaces.Contacts.ManageContact.Ui_ManageContact import Ui_ManageContact
from Interfaces.Contacts.Widgets import ContactListWidget

# Python standard libraries
import os
from shutil import copyfile
from string import ascii_letters, digits
from random import sample


class ContactManaging(QtWidgets.QDialog, Ui_ManageContact):
    """
    This class implements the window to edit / create a contact.
    """
    character_pool = frozenset(ascii_letters + digits)

    @staticmethod
    def random_file_name(length: int = 16):
        """
        Returns a random string of default length = 16 with characters contained inside character_pool.
        """
        return "".join(sample(ContactManaging.character_pool, length))

    # Static images to avoid IO bottleneck
    icon_valid = QtGui.QPixmap(os.path.abspath("graphics/valid.png"))
    icon_not_valid = QtGui.QPixmap(os.path.abspath("graphics/not_valid.png"))

    def __init__(self, parent: QtWidgets.QWidget, pre_filled: ContactListWidget = None):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.pre_filled = pre_filled

        # This value is set if the user selects a new picture.
        self.external_pic_full_path = None

        # This value holds the new ContactListWidget that will be read from ContactsWindow.
        self.return_value = None

        self.setupUi(self)

        # Setup interface
        self.lineEditAction_name = self.lineEdit_Name.addAction(
            QtGui.QIcon(), QtWidgets.QLineEdit.TrailingPosition
        )
        self.lineEditAction_address = self.lineEdit_Address.addAction(
            QtGui.QIcon(), QtWidgets.QLineEdit.TrailingPosition
        )
        self.set_label_pixmap(ContactListWidget.pixmap_generic_user)

        # Initial state
        if pre_filled:
            self.setWindowTitle("Edit contact")
            self.lineEdit_Name.setText(pre_filled.contact.name)
            self.lineEdit_Address.setText(pre_filled.contact.info)
            if pre_filled.contact.pic_name:
                self.set_label_pixmap(
                    QtGui.QPixmap(os.path.join(ProjectConstants.fullpath_thumbnails, pre_filled.contact.pic_name))
                )
                self.external_pic_full_path = ProjectConstants.fullpath_thumbnails + pre_filled.contact.pic_name
                self.pushButton_Delete.setEnabled(True)

        # Connections
        self.pushButton_Change.clicked.connect(self.pushbutton_modify)
        self.pushButton_Delete.clicked.connect(self.pushbutton_delete)
        self.lineEdit_Name.textChanged.connect(self.validate_inputs)
        self.lineEdit_Address.textChanged.connect(self.validate_inputs)

        self.validate_inputs()

    @QtCore.Slot()
    def accept(self):
        """
        This method sets the return value of self with a valid widget constructed following user inputs and then calls
        super().accept()
        """
        # If there is a picture for the widget
        if self.external_pic_full_path:
            # Picture has to be updated if:
            # - widget had no picture or
            # - widget picture is different from the one selected now
            # This truth evaluation is risky because at this point self.pre_filled.contact.pic_name could be None
            #  so trying to concatenate a string + NoneType would result in an error. However if
            #  self.pre_filled.contact.pic_name is None the first condition would return True and, since it's an
            #  or statement, that's enough to stop evaluating the truth and the second evaluation should never
            #  take place.
            #  If it does take place then self.pre_filled.contact.pic_name was not None and the concatenation
            #  can take place.
            #  I am just learning not that this process is called short-circuit.
            if (
                    not self.pre_filled.contact.pic_name or
                    self.external_pic_full_path != ProjectConstants.fullpath_thumbnails + self.pre_filled.contact.pic_name
            ):
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
                new_pic_name = self.pre_filled.contact.pic_name
        else:
            new_pic_name = None
        self.return_value = ContactListWidget(
            Contact(new_pic_name, self.lineEdit_Name.text(), self.lineEdit_Address.text())
        )

        super().accept()

    @QtCore.Slot()
    def validate_inputs(self):
        """
        This method makes sure inputs are valid.

        Action icon on each QLineEdit is changed accordingly and Ok button is enabled accordingly.
        """
        states = {
            "name": self.lineEdit_Name.text() != "",
            "address": is_valid_address(self.lineEdit_Address.text())
        }

        self.lineEditAction_name.setIcon(
            self.icon_valid if states["name"] else self.icon_not_valid
        )

        self.lineEditAction_address.setIcon(
            self.icon_valid if states["address"] else self.icon_not_valid
        )

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(
            all(states)
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

            self.pushButton_Delete.setEnabled(True)

    @QtCore.Slot()
    def pushbutton_delete(self):
        self.external_pic_full_path = None
        self.set_label_pixmap(ContactListWidget.pixmap_generic_user)
        self.pushButton_Delete.setEnabled(False)

    def set_label_pixmap(self, pixmap: QtGui.QPixmap):
        """
        This method sets the label inside the picture frame.

        It only resized the input pixmap if it is bigger than the label that is going to contain it.
        """
        picture_size = pixmap.size()
        label_max_size = self.label_Picture.maximumSize()

        self.label_Picture.setPixmap(
            pixmap
            if picture_size.width() < label_max_size.width() and picture_size.height() < label_max_size.height() else
            pixmap.scaled(
                label_max_size,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
        )
