
import os

from tkinter import *
from tkinter import ttk

from VGC_Img import loadImage


######################
# Label_
# --------------------
class Label_(object):

    id       = ""
    text     = None
    item     = None
    image    = None
    imgwidth = 0
    imgdef   = ""

    # Constructor
    def __init__(self, parent,
                 id="", text="",
                 anchor="nw", justify="left",
                 width=0, height=0,
                 padx=0, pady=0,
                 wraplength=0, font=None,
                 img="", imgdef="", imgwidth=0,
                 bg=None, fg=None):

        self.item = Label(parent,
                          anchor=anchor,
                          justify=justify,
                          width=width,
                          height=height,
                          padx=padx,
                          pady=pady,
                          wraplength=wraplength,
                          font=font,
                          bg=bg,
                          fg=fg)

        self.id          = id
        self.imgdef      = imgdef
        self.text        = StringVar(self.item, text, id)
        self.item.config(textvariable=self.text)

        self.setImage(img, imgwidth)

    def get(self):
        return self.text.get()

    def set(self, text):
        self.text.set(text)

    def setImage(self, img, imgwidth=0):
        if imgwidth > 0:
            self.imgwidth = imgwidth

        if not os.path.exists(img):
            img = self.imgdef

        if len(img) > 0:
            self.image = loadImage(img, self.imgwidth)
            self.item.config(image=self.image)



######################
# Entry_
# --------------------
class Entry_(object):

    id       = ""
    text     = None
    item     = None

    # Constructor
    def __init__(self, parent,
                 id="", text="",
                 justify="left",
                 width=0, show=""):

        self.item = Entry(parent,
                          justify=justify,
                          width=width,
                          show=show)

        self.id   = id
        self.text = StringVar(self.item, text, id)
        self.item.config(textvariable=self.text)

    def get(self):
        return self.text.get()

    def set(self, text):
        self.text.set(text)

    def delete(self, start, end):
        self.item.delete(start, end)



######################
# Combobox_
# --------------------
class Combobox_(object):

    id   = ""
    item = None

    # Constructor
    def __init__(self, parent,
                 id="", text="",
                 justify="left",
                 width=0, height=10,
                 show="", values=None,
                 state=""):

        self.item = ttk.Combobox(parent,
                          justify=justify,
                          width=width,
                          height=height,
                          values=values,
                          state=state)

        self.id = id

    def get(self):
        return self.item.get()

    def set(self, text):
        self.item.set(text)

    def delete(self, start, end):
        self.item.delete(start, end)

    def setValues(self, values):
        self.item['values'] = values