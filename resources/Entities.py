"""
This module contains common entities model shared between classes
"""


# Local Project
import resources.Constants as ProjectConstants

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
                print("Could not delete profile picture", file=stderr)
                print(e, file=stderr)
