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
#   Hard coding the version of kmd isn't the greatest of ideas however this program is written with v0.5 in mind so it
#    shouldn't be guaranteed that it will work for version of kmd past v0.5.
filename_kmd_net = "kmd-v0.5/kmd.net"
filename_kmd_token = "kmd-v0.5/kmd.token"

# Composite constants
#   Software data paths & filenames
fullpath_contacts_json = path.join(path_user_data, filename_contacts_json)
fullpath_settings_json = path.join(path_user_data, filename_settings_json)
fullpath_thumbnails = path.join(path_user_data, folder_thumbnails)
