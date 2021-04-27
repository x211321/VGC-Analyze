import os

from tkinter import *
from tkinter import ttk

from VGC_Img import loadImage


######################
# Label_
# --------------------
class Label_(Label):

    # Constructor
    def __init__(self, master=None,
                 id="", text="",
                 anchor="nw", justify="left",
                 width=0, height=0,
                 padx=0, pady=0,
                 wraplength=0, font=None,
                 img="", imgdef="", imgwidth=0,
                 bg=None, fg=None,
                 relief=None):

        super().__init__(master=master, width=width, height=height, anchor=anchor, justify=justify, padx=padx, pady=pady, wraplength=wraplength, bg=bg, fg=fg, relief=relief)

        self.id       = id
        self.imgdef   = imgdef
        self.text     = StringVar(self, text, id)
        self.imgwidth = imgwidth
        self.config(textvariable=self.text)

        self.setImage(img, self.imgwidth)

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
            self.config(image=self.image)


######################
# Entry_
# --------------------
class Entry_(Entry):

    # Constructor
    def __init__(self, master=None,
                 id="", text="",
                 justify="left",
                 width=0, show=""):

        super().__init__(master=master, justify=justify, width=width, show=show)

        self.id   = id
        self.text = StringVar(self, text, id)
        self.config(textvariable=self.text)

    def get(self):
        return self.text.get()

    def set(self, text):
        self.text.set(text)


######################
# Checkbutton_
# --------------------
class Checkbutton_(Checkbutton):

    # Constructor
    def __init__(self, master=None,
                 id="", check=0,
                 label="",
                 justify="left",
                 padx=0, pady=0,
                 width=0, command=None,
                 default = False,
                 bg = None):

        super().__init__(master=master, text=label, padx=padx, pady=pady, justify=justify, width=width, command=command, bg=bg)

        self.id   = id
        self.value = IntVar(self, check, id)
        self.config(variable=self.value)

        self.set(default)

    def get(self):
        return self.value.get()

    def set(self, newValue):
        self.value.set(newValue)


######################
# Combobox_
# --------------------
class Combobox_(ttk.Combobox):

    # Constructor
    def __init__(self, master=None,
                 id="", text="",
                 justify="left",
                 width=0, height=10,
                 show="", values=None,
                 state=""):

        super().__init__(master=master, justify=justify, width=width, height=height, values=values, state=state)

        self.id = id

    def setValues(self, values):
        self['values'] = values
