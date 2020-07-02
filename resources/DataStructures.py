"""
This file contains some classes that implement functionality for some data structure
"""


from typing import Dict


class ChangeContainer:
    """
    This is a wrapper for whatever mutable variable that implements the functionality to save the state of
    the container in order to decide if it has changed over time.
    """
    def __init__(self):
        self.memory = None
        self.old_hash = None

    def __getstate__(self) -> Dict:
        result = self.__dict__.copy()
        del result["old_hash"]
        return result

    def __setstate__(self, state: Dict):
        self.__dict__.update(state)

    def save_state(self):
        self.old_hash = str(self.memory).__hash__()

    def has_changed(self) -> bool:
        return str(self.memory).__hash__() != self.old_hash

