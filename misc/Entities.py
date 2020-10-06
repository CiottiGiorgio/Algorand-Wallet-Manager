"""
This module contains common entities model shared between classes.
"""

# PySide2
from PySide2 import QtCore

# algosdk
from algosdk.wallet import Wallet as AlgosdkWallet

# Local Project
import misc.Constants as ProjectConstants

# Python standard libraries
from os import path, remove
from sys import stderr
from typing import Dict


class Contact:
    """
    Object that represents a single contact in the contact list.
    """
    def __init__(self, pic_name: str, name: str, info: str):
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
                if __debug__:
                    print(type(e), str(e), file=stderr)
                print("Could not delete profile picture for %s" % self.name, file=stderr)


class Wallet:
    """
    This class represents a wallet inside this program memory. Not to be confused with algosdk.wallet.Wallet.

    It just holds 2 properties:
        1. The dict returned from algosdk call
        2. algosdk.wallet.Wallet for when the wallet is unlocked with its password
    """
    def __init__(self, info: Dict):
        self.info = info
        self.algo_wallet = None

    def unlock(self, algo_wallet: AlgosdkWallet):
        self.algo_wallet = algo_wallet

    def lock(self):
        self.algo_wallet = None


class AlgorandWorkerSignals(QtCore.QObject):
    """
    QObject with custom signals.

    This is used in AlgorandWorker to signal a success with return value or an error.
    """
    success = QtCore.Signal(object)
    error = QtCore.Signal(Exception)


class AlgorandWorker(QtCore.QRunnable):
    """
    This class is used to run a callable in a thread using QThreadPool.

    We use this instead of a separate class for every piece of code we could ever need to run.
    As long as it's a simple blocking call with a return value this is fine. Just connect to result signal with the
    function that process the return value.
    """
    def __init__(self, fn: callable, *args, **kwargs):
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
            self.signals.error.emit(e)
        else:
            self.signals.success.emit(result)
