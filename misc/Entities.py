"""
This module contains common entities model shared between classes.
"""

# PySide2
from PySide2 import QtWidgets, QtGui, QtCore

# Local Project
import misc.Constants as ProjectConstants

# Python standard libraries
from os import path, remove
from sys import stderr


class Contact:
    """
    Object that represents a single contact in the contact list.
    """
    def __init__(self, pic_name, name, info):
        self.pic_name = pic_name
        self.name = name
        self.info = info

    def release(self):
        """
        Method to destroy profile picture on disk.
        """
        if self.pic_name:
            try:
                remove(path.join(ProjectConstants.fullpath_thumbnails, self.pic_name))
            except Exception as e:
                print("Could not delete profile picture for %s" % self.name, file=stderr)
                print(e, file=stderr)


class Wallet:
    """
    Object that represents a single wallet.
    """
    def __init__(self, name, info):
        self.name = name
        self.info = info


class AlgorandWorkerSignals(QtCore.QObject):
    """
    QObject with custom signals.

    This is used in AlgorandWorker to signal a success with return value or an error.
    """
    success = QtCore.Signal(object)
    error = QtCore.Signal(str)


class AlgorandWorker(QtCore.QRunnable):
    """
    This class is used to run a callable in a thread using QThreadPool.

    We use this instead of a separate class for every piece of code we could ever need to run.
    As long as it's a simple blocking call with a return value this is fine. Just connect to result signal with the
    function that process the return value.
    """
    def __init__(self, fn, *args, **kwargs):
        super().__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = AlgorandWorkerSignals()

    def run(self):
        """
        This overridden method calls a callable fn with args, kwargs parameters.

        This method gets called once this object is inside a QThreadPool.
        """
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            self.signals.error.emit(str(e))
        else:
            self.signals.success.emit(result)


class LoadingWidget(QtWidgets.QWidget):
    """
    This class implements a simple widget used to show a loading message.
    """

    # We don't make the loading gif static because it's a movie with a .start() method and i'm not sure
    #  if sharing it with other widget might cause an issue.

    def __init__(self, label_content: str):
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

    error_icon = QtGui.QPixmap(path.abspath("graphics/not valid.png")).scaled(
        20, 20,
        QtCore.Qt.IgnoreAspectRatio,
        QtCore.Qt.SmoothTransformation)

    def __init__(self, label_content: str):
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
