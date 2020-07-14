"""
This file contains subclasses of PySide2 widgets that are used throughout this project.
"""


# PySide2
from PySide2 import QtWidgets

# Python standard libraries
from typing import Type


class CustomListWidget(QtWidgets.QListWidget):
    """
    This class is used to implement a QListWidget with some common code used in the project.

    E.g.: How to add a widget directly.
    """
    def __init__(self, parent: QtWidgets.QWidget, item_type: Type[QtWidgets.QListWidgetItem]):
        super().__init__(parent)

        self.item_type = item_type

    def add_widget(self, widget: QtWidgets.QWidget):
        item = self.item_type()
        item.setSizeHint(widget.minimumSizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)


class StackedQueuedWidget(QtWidgets.QStackedWidget):
    """
    This class is used to restrict the behaviour of a QStackedLayout to that of a queue.

    This class will also always display the highest widget in the queue.
    """
    def addWidget(self, w: QtWidgets.QWidget) -> int:
        return_value = super().addWidget(w)
        self.setCurrentIndex(return_value)
        return return_value

    def removeTopWidget(self):
        self.removeWidget(self.widget(self.count()))
