"""
This file is a script that compiles all .ui files in this project folder and subfolders into a .py file.
This is for the convenience of development only. Once this application is not on development there's no need to run
this script before main.py

You should run this script before every time you execute main.py because it checks whether or not to compile a .ui file.
Of course this file is only useful in development when .ui files are changed through "Qt Creator".
"""


import os


def ui_compile(source: str, destination: str):
    os.system("pyside2-uic %s -o %s" % (source, destination))


# This loop recursively walk through all dirs starting from this script dir
for x, y, z in os.walk(os.path.join(os.path.dirname(__file__), "Interfaces")):
    # This filter removes from y all .git and __pycache__ subdirs
    y[:] = filter(
        lambda h: h != ".git" and h != "__pycache__", y
    )

    # For each .ui file we should check if it has to be recompiled into a new .py file.
    #  (Either .py file doesn't exists or it's older than .ui file)
    for filename in z:
        if filename[-3:] == ".ui":
            ui_fullpath = os.path.join(x, filename)
            py_fullpath = os.path.join(x, filename[:-3] + ".py")

            # If there is a newer .py file of a .ui file then skip. Otherwise compile.
            #  (Meaning the py file is either non existent or older than ui file)
            ui_time = os.path.getmtime(ui_fullpath)
            if os.path.exists(py_fullpath):
                py_time = os.path.getmtime(py_fullpath)
                if ui_time <= py_time:
                    continue

            ui_compile(ui_fullpath, py_fullpath)
