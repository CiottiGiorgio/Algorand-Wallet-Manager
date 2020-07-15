"""
This file will contain all constants needed throughout the rest of this project
"""


from os import path

# Single constants
#   Software data paths & filenames
path_user_data = path.abspath(path.join(path.expanduser("~"), ".algorand-wallet-manager"))
filename_contacts_json = "contacts.json"
filename_settings_json = "settings.json"
folder_thumbnails = "thumbnails"

#   Algorand node paths & filenames
filename_algod_net = "algod.net"
filename_algod_token = "algod.token"
# TODO hard coding the version of kmd doesn't look like a good idea
filename_kmd_net = "kmd-v0.5/kmd.net"
filename_kmd_token = "kmd-v0.5/kmd.token"

#   Reference to common PySide2 objects
main_window = None  # Am i supposed to change this file at runtime?
wallet_frame = None

# Composite constants
#   Software data paths & filenames
fullpath_contacts_json = path.join(path_user_data, filename_contacts_json)
fullpath_settings_json = path.join(path_user_data, filename_settings_json)
fullpath_thumbnails = path.join(path_user_data, folder_thumbnails)
