"""
This file contains some function that are used in multiple classes but belong to none of them.
"""

# PySide2
from PySide2 import QtWidgets

# Python standard libraries
import jsonpickle
from sys import stderr


def load_json_file(file: str) -> object:
    """
    This method takes a json file and returns the data structure contained in it.

    Any error during this method results in the application quitting.
    """
    try:
        with open(file) as f:
            return jsonpickle.decode(f.read())
    except Exception as e:
        print("Could not load {}".format(file.split('\\')[-1]), file=stderr)
        print(e, file=stderr)
        quit()


def dump_json_file(file: str, structure: object):
    """
    This function takes a data structure and writes it to the json file.

    Any error during this method WILL NOT result in the application quitting. Although the application might
    be in the stage of closing anyway if it's trying to save to disk.
    """
    try:
        with open(file, 'w') as f:
            f.write(jsonpickle.encode(structure, indent='\t'))
    except Exception as e:
        print("Could not dump {}".format(file.split('\\')[-1]), file=stderr)
        print(e, file=stderr)


class ProjectException(Exception):
    """
    Custom exception class to raise an internal error.
    """
    def __init__(self, message: str):
        self.message = message


def find_main_window() -> QtWidgets.QMainWindow:
    """
    This function returns a reference to MainWindow

    This function operates under the assumption that there is only one instance of QMainWindow in the whole application.
    It will raise an error otherwise.
    """
    top_widgets = QtWidgets.QApplication.topLevelWidgets()
    main_window = [x for x in top_widgets if isinstance(x, QtWidgets.QMainWindow)]

    if len(main_window) != 1:
        # Uh oh...
        raise ProjectException(f"Found {len(main_window)} instance(s) of QMainWindow not equal to one.")

    return main_window[0]
