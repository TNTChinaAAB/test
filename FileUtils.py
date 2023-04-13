import os
from ShellUtils import *

def chmod():
    callShell("chmod 777 -R .")


def chmod_file(file: str):
    callShell(f"chmod 777 -R {file}")


def isFileExists(path4: str) -> bool:
    if os.path.exists(path4):
        if os.path.isfile(path4):
            return True
        else:
            return False
    else:
        return False


def isDirExists(path5: str):
    if os.path.exists(path5):
        if os.path.isdir(path5):
            return True
        else:
            return False
    else:
        return False


def getFileSize(path3: str) -> int:
    if not os.path.exists(path3):
        return 0
    return os.path.getsize(path3)
