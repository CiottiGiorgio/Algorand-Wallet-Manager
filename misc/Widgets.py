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
    This class is to add the behaviour of a queue to QStackedWidget.

    Old methods in this class are unaltered however add_widget is a modified version that always displays the last
    widget inserted.
    """
    def add_widget(self, w: QtWidgets.QWidget) -> int:
        """
        This method adds a widget to the top of the queue and makes it visible.
        """
        return_value = super().addWidget(w)
        self.setCurrentIndex(return_value)
        return return_value

    # We don't touch original .removeWidget() method and we create a new one. It's fine we are all adults and we know
    #  what we are doing.

    def remove_top_widget(self):
        """
        This method removes the top widget in the queue.

        If we removes the nth widget then the new widget shown is automatically the (n-1)th.
        """
        self.removeWidget(self.widget(self.count()))

    def clear_queue(self):
        while self.count() >= 1:
            self.remove_top_widget()
