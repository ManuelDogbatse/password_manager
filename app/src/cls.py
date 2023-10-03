import os

def cls():
    # "clear" for Mac/Linux, "cls" for Windows
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")