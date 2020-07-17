"""
This file contains subclasses of PySide2 widgets that are used throughout this project.
"""


# PySide2
from PySide2 import QtWidgets, QtCore, QtGui

# Python standard libraries
from os import path
from typing import Type


class CustomListWidget(QtWidgets.QListWidget):
    """
    This class is used to implement a QListWidget with some common code used in the project.
    """
    def __init__(
            self,
            parent: QtWidgets.QWidget,
            item_type: Type[QtWidgets.QListWidgetItem],
            loading_widget: bool = False
    ):
        super().__init__(parent)

        self.item_type = item_type
        self.timer = None

        # We make a LoadingWidget appear after a fixed amount of time. Making it appear instantly would cause weird
        #  effects on the GUI.
        if loading_widget:
            self.timer = QtCore.QTimer()
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(lambda: self.add_widget(LoadingWidget()))
            self.timer.start(300)

    def add_widget(self, widget: QtWidgets.QWidget):
        """
        This method adds a widget to the list using the custom QListWidgetItem specified in the constructor.

        This method avoids code duplication.
        """
        item = self.item_type()
        item.setSizeHint(widget.minimumSizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)

    def clear_loading(self):
        """
        This method cleans the list from a possible LoadingWidget.
        """
        if self.timer.isActive():
            self.timer.stop()
            self.timer.timeout.disconnect()
        elif isinstance(self.itemWidget(self.item(0)), LoadingWidget):
            self.takeItem(0)


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
        self.removeWidget(self.widget(self.count() - 1))

    def clear_queue(self):
        while self.count() >= 1:
            self.remove_top_widget()


class LoadingWidget(QtWidgets.QWidget):
    """
    This class implements a simple widget used to show a loading message.
    """

    # We don't make the loading gif static because it's a movie with a .start() method and i'm not sure
    #  if sharing it with other widget might cause an issue.

    def __init__(self, label_content: str = "Loading..."):
        super().__init__()

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Setup interface
        main_layout = QtWidgets.QHBoxLayout(self)

        movie = QtGui.QMovie("graphics/loading.webp")
        movie.setScaledSize(QtCore.QSize(30, 30))
        movie.setCacheMode(QtGui.QMovie.CacheAll)

        main_layout.addStretch(1)

        movie_label = QtWidgets.QLabel()
        movie_label.setMovie(movie)
        main_layout.addWidget(movie_label)

        loading_label = QtWidgets.QLabel(label_content)
        loading_label.adjustSize()
        main_layout.addWidget(loading_label)

        main_layout.addStretch(1)
        # End setup

        movie.start()


class ErrorWidget(QtWidgets.QWidget):
    """
    This class implements a simple widget used to show an error message.
    """

    error_icon = QtGui.QPixmap(path.abspath("graphics/not_valid.png")).scaled(
        20, 20,
        QtCore.Qt.IgnoreAspectRatio,
        QtCore.Qt.SmoothTransformation)

    def __init__(self, label_content: str = "Error."):
        super().__init__()

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Setup interface
        main_layout = QtWidgets.QHBoxLayout(self)

        main_layout.addStretch(1)

        label_pixmap = QtWidgets.QLabel()
        label_pixmap.setPixmap(ErrorWidget.error_icon)
        main_layout.addWidget(label_pixmap)

        label_message = QtWidgets.QLabel(label_content)
        main_layout.addWidget(label_message)

        main_layout.addStretch(1)
        # End setup
