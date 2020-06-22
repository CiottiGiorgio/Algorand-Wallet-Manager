"""
This file will contain all constants needed throughout the rest of this project
"""


from os import path

# Single constants
path_user_data = path.abspath(path.join(path.expanduser("~"), ".algorand-wallet-manager"))
filename_contacts_json = "contacts.json"
folder_thumbnails = "thumbnails"

# Composite constants
fullpath_contacts_json = path.join(path_user_data, filename_contacts_json)
fullpath_thumbnails = path.join(path_user_data, folder_thumbnails)
