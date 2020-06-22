"""
This module contains common entities model shared between classes
"""


class Contact:
    """
    Object that represents a single contact in the contact list
    """
    def __init__(self, pic_name, name, info):
        self.pic_name = pic_name
        self.name = name
        self.info = info
