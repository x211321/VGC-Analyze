from lib.Locale import _

import os

try:
    from PIL import Image, ImageTk
except ImportError:
    pillow_available = False
    print("PIL (Pillow) not found")
else:
    pillow_available = True

from tkinter import PhotoImage

import lib.Var as VAR


######################
# loadImage
# --------------------
def loadImage(path, width = 0, padx = 0):

    if pillow_available:
        if os.path.exists(path):
            img = Image.open(path)

            percent = width/float(img.size[0])
            height  = int(float(img.size[1]) * float(percent))

            img = img.resize((width, height), Image.ANTIALIAS)

            if padx:
                img = padImage(img, width, height, padx)

            return ImageTk.PhotoImage(img)
    else:
        return PhotoImage(file=VAR.IMG_COVER_PIL_MISSING)


######################
# loadIcon
# --------------------
def loadIcon(name, width, height, padx = 0):
    iconPath     = VAR.ICON_PATH + name + ".png"
    alt_iconPath = VAR.ICON_PATH + str(width) + "x" + str(height) + "/" + name + ".png"

    if pillow_available == False:
        # When Pillow is not available we try to find a fallback Icon
        # that has been pre-resized
        if os.path.exists(alt_iconPath):
            iconPath = alt_iconPath
    if pillow_available:
        if os.path.exists(iconPath):
            icon = Image.open(iconPath)
            icon = icon.resize((width, height), Image.ANTIALIAS)

            if padx:
                icon = padImage(icon, width, height, padx)

            return ImageTk.PhotoImage(icon)
        else:
            return ImageTk.PhotoImage(Image.new('RGB', (width, height)))
    else:
        return PhotoImage(file=iconPath)


######################
# padImage
# --------------------
def padImage(image, x, y, padx):
    temp = Image.new('RGBA', (x + padx, y))
    temp.paste(Image.new('RGB', (x, y)), image)
    return temp