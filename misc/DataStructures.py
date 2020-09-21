"""
This file contains some classes that implement functionality for some data structure
"""


from typing import Dict
from collections.abc import MutableSequence, MutableMapping


class ChangeDetectable:
    """
    This class implements functionality for detecting changes in a data structure between two points in time.
    Namely from the last time .save_state() was called and the last time has_changed() was called.

    One would need to structure this a little better if we knew what kind of underlying data structure we have.
    I'm going to use this for a MutableSequence and a MutableMapping so i'm not going to write abstract methods that
    have to be defined because write operation on data structure differ. I'm going to rely on the child classes
    to implement correctly their version of write operation that correctly signal the changed flag.
    """

    def __init__(self):
        self._changed = False

    def __getstate__(self) -> Dict:
        """
        We hide this runtime flag from being saved in persistent memory when jsonpickle.encode() is called.
        """
        result = self.__dict__.copy()
        del result["_changed"]
        return result

    def __setstate__(self, state: Dict):
        """
        This method has to be implemented because __getstate__ is.
        """
        self.__dict__.update(state)

    def save_state(self):
        self._changed = False

    def has_changed(self) -> bool:
        return self._changed


class ListJsonContacts(MutableSequence, ChangeDetectable):
    """
    This class implements a list-like object that is used to hold the content of contacts.json file and is able to
    tell if content is changed.
    """
    def __init__(self):
        super().__init__()
        self._list = list()

    def __getitem__(self, item):
        return self._list.__getitem__(item)

    def __setitem__(self, key, value):
        self._list.__setitem__(key, value)
        self._changed = True

    def __delitem__(self, key):
        self._list.__delitem__(key)
        self._changed = True

    def __len__(self):
        return self._list.__len__()

    def insert(self, index, item):
        self._list.insert(index, item)
        self._changed = True


class DictJsonSettings(MutableMapping, ChangeDetectable):
    """
    This class implements a dict-like object that is used to hold the content of settings.json file and is able to tell
    if content is changed.
    """
    def __init__(self):
        super().__init__()
        self._dict = {
            "selected": 0,
            "local": "",
            "algod": {"url": "", "port": "", "token": ""},
            "kmd": {"url": "", "port": "", "token": ""},
            "indexer": {"url": "", "port": "", "token": ""}
        }

    def __getitem__(self, key):
        return self._dict.__getitem__(key)

    def __setitem__(self, key, value):
        self._dict.__setitem__(key, value)
        self._changed = True

    def __delitem__(self, key):
        self._dict.__delitem__(key)
        self._changed = True

    def __iter__(self):
        return self._dict.__iter__()

    def __len__(self):
        return self._dict.__len__()
