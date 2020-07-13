"""
This file contains subclasses of PySide2 widgets that are used throughout this project.
"""


# PySide2
from PySide2 import QtWidgets

# Python standard libraries
from typing import Type


class CustomListWidget(QtWidgets.QListWidget):
    def __init__(self, parent: QtWidgets.QWidget, item_type: Type[QtWidgets.QListWidgetItem]):
        super().__init__(parent)

        self.item_type = item_type

    def add_widget(self, widget: QtWidgets.QWidget):
        item = self.item_type()
        item.setSizeHint(widget.minimumSizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)
