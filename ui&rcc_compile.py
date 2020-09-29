"""
This file is a script that compiles all .ui files and .qrc files in this project folder and subfolders into a .py file.
This is for the convenience of development only. Once this application is not on development there's no need to run
this script before main.py

You should run this script before every time you execute main.py because it checks whether or not to compile a .ui or
.qrc file.
Of course this file is only useful in development when .ui files are changed through "Qt Creator".
"""


import os


compile_cmds = {
    "ui": lambda source, destination: os.system(f"pyside2-ui {source} -o {destination}"),
    "rcc": lambda source, destination: os.system(f"pyside2-rcc {source} -o {destination}")
}


# This walks recursively through all dirs starting from this script dir
for dirpath, dirnames, filenames in os.walk(os.path.join(os.path.dirname(__file__))):
    # This filter removes from y all .git and __pycache__ subdirs
    dirnames[:] = filter(
        lambda h: h != ".git" and h != "__pycache__" and h != ".idea", dirnames
    )

    # For every .ui file we should check if it has to be recompiled into a new .py file.
    #  (Either .py file doesn't exists or it's older than .ui file)
    # Same reasoning for every .qrc file.
    for filename in filenames:
        if filename[-3:] == ".ui" or filename[-4:] == ".qrc":
            qt_fullpath = os.path.join(dirpath, filename)
            if filename[-3:] == ".ui":
                py_fullpath = os.path.join(dirpath, filename[:-3] + ".py")
                compile_cmd = compile_cmds["ui"]
            else:
                py_fullpath = os.path.join(dirpath, filename[:-4] + ".py")
                compile_cmd = compile_cmds["rcc"]

            # If there is a newer .py file of a .ui file then skip. Otherwise compile.
            #  (Meaning the py file is either non existent or older than ui file)
            qt_time = os.path.getmtime(qt_fullpath)
            if os.path.exists(py_fullpath):
                py_time = os.path.getmtime(py_fullpath)
                if qt_time <= py_time:
                    continue

            print(f"compiling: {qt_fullpath}")
            compile_cmd(qt_fullpath, py_fullpath)
