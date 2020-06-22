"""
This module contains common entities model shared between classes
"""


from json import JSONDecoder


class Contact:
    """
    Object that represents a single contact in our contact list
    """
    def __init__(self, pic_name, name, info):
        # This is meta-data. When this object will be serialized it will contain this piece of information that links
        #  json object to Contact. Of course this only becomes useful when we have heterogeneous objects in a single
        #  list. We'll keep this anyway for compatibility's sake.
        self.__contact__ = True

        self.pic_name = pic_name
        self.name = name
        self.info = info


class ContactJSONDecoder(JSONDecoder):
    """
    This is the JSON Decoder associated to Contact.

    This will be used when loading JSON list of Contact into memory.
    """
    def __init__(self):
        super().__init__(object_hook=self.dict_to_contact)

    @staticmethod
    def dict_to_contact(d):
        if "__contact__" in d:
            return Contact(d["pic_name"], d["name"], d["info"])
        else:
            return d
