"""
This file contains some classes that implement functionality for some data structure
"""


from typing import Dict


# TODO rethink the way this wrapper checks if a mutable structure underneath has changed.
#  Using hash could be problematic because there is a small chance that a changed in time structure gives out the same
#  hash as the first time it was hashed.
class ChangeContainer:
    """
    This is a wrapper for whatever mutable data structure that implements the functionality to save the state of
    the container in order to decide if it has changed over time.
    """
    def __init__(self):
        self.memory = None
        self.old_hash = None

    def __getstate__(self) -> Dict:
        """
        Method used in jsonpickle.encode
        """
        result = self.__dict__.copy()
        del result["old_hash"]
        return result

    def __setstate__(self, state: Dict):
        """
        Method used in jsonpickle.decode.

        Looks useless but actually has to be implemented because __getstate__ is.
        """
        self.__dict__.update(state)

    def save_state(self):
        self.old_hash = str(self.memory).__hash__()

    def has_changed(self) -> bool:
        return str(self.memory).__hash__() != self.old_hash


class ListJsonContacts(ChangeContainer):
    """
    This class will be used to hold the information of contacts.json file.
    """
    def __init__(self):
        super().__init__()
        self.memory = list()


class DictJsonSettings(ChangeContainer):
    """
    This class will be used to hold the information of settings.json file.
    """
    def __init__(self):
        super().__init__()
        self.memory = dict()

        self.memory["selected"] = 0

        self.memory["local"] = ""

        self.memory["algod"] = {"url": "", "port": "", "token": ""}
        self.memory["kmd"] = {"url": "", "port": "", "token": ""}
        self.memory["indexer"] = {"url": "", "port": "", "token": ""}