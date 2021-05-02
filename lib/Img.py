from lib.Locale import _

import os
from PIL import Image, ImageTk

import lib.Var as VAR


######################
# loadImage
# --------------------
def loadImage(path, width = 0, padx = 0):

    if os.path.exists(path):
        img = Image.open(path)

        percent = width/float(img.size[0])
        height  = int(float(img.size[1]) * float(percent))

        img = img.resize((width, height), Image.ANTIALIAS)

        if padx:
            img = padImage(image, width, height, padx)

        return ImageTk.PhotoImage(img)


######################
# loadCover
# --------------------
def loadCover(path = "", width = 120):
    if len(path) == 0 or not os.path.exists(path):
        path = VAR.IMG_COVER_NONE

    loadImage(path, width)


######################
# loadIcon
# --------------------
def loadIcon(name, width, height, padx = 0):
    iconPath = VAR.ICON_PATH + name + ".png"

    if os.path.exists(iconPath):

        icon = Image.open(iconPath)
        icon = icon.resize((width, height), Image.ANTIALIAS)

        if padx:
            icon = padImage(icon, width, height, padx)

        return ImageTk.PhotoImage(icon)
    else:
        return ImageTk.PhotoImage(Image.new('RGB', (width, height)))


######################
# padImage
# --------------------
def padImage(image, x, y, padx):
    temp = Image.new('RGBA', (x + padx, y))
    temp.paste(Image.new('RGB', (x, y)), image)
    return temp