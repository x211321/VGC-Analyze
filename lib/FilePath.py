from lib.Locale import _

import os

from tkinter import Tk
from tkinter.filedialog import askopenfilename

######################
# writeFile
# --------------------
def writeFile(filePath, content, mode = "w", encoding = ""):
    dir = os.path.dirname(filePath)

    if len(dir) and not os.path.exists(dir):
        os.makedirs(dir)

    if len(encoding):
        file = open(filePath, mode, encoding=encoding)
    else:
        file = open(filePath, mode)

    file.write(content)
    file.close()


######################
# readFile
# --------------------
def readFile(filePath, mode = "r", encoding = ""):

    result = ""

    if os.path.exists(filePath):
        if len(encoding):
            file = open(filePath, mode, encoding=encoding)
        else:
            file = open(filePath, mode)

        for line in file:
            result += line

        file.close()

    return result



######################
# chooseFile
# --------------------
def chooseFile():
    # hide main-window of Tk
    Tk().withdraw()
    # show selection dialog and return it to caller
    return askopenfilename()
