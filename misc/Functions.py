"""
This file contains some function that are used in multiple classes but belong to none of them.
"""

# Local project
from misc.DataStructures import ChangeContainer

# Python standard libraries
import jsonpickle
from sys import stderr


def load_json_file(file: str) -> ChangeContainer:
    """
    This method takes a json file and returns the data structure contained in it.

    Any error during this method results in the application quitting.
    """
    try:
        with open(file) as f:
            return jsonpickle.decode(f.read())
    except Exception as e:
        print("Could not load %s" % file.split('\\')[-1], file=stderr)
        print(e, file=stderr)
        print("Now exiting.", file=stderr)
        quit()


def dump_json_file(file: str, structure: ChangeContainer):
    """
    This function takes a data structure and writes it to the json file.

    Any error during this method WILL NOT result in the application quitting. Although the application might
    be in the stage of closing anyway if it's trying to save to disk.
    """
    try:
        with open(file, 'w') as f:
            f.write(jsonpickle.encode(structure, indent='\t'))
    except Exception as e:
        print("Could not dump %s" % file.split('\\')[-1], file=stderr)
        print(e, file=stderr)
