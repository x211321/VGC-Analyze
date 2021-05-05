from lib.Locale import _

import os

from tkinter import *
from tkinter import ttk

from lib.Img import loadImage

import lib.Var as VAR


######################
# Label_
# --------------------
class Label_(Label):

    # Constructor
    def __init__(self, master=None,
                 id="", text="", col=None, row=None,
                 anchor="nw", justify="left",
                 width=0, height=0,
                 _padx=None, _pady=None,
                 wraplength=0, font=None,
                 img="", imgdef="", imgwidth=0,
                 bg=None, fg=None,
                 relief=None):

        super().__init__(master=master, width=width, height=height, anchor=anchor, justify=justify, wraplength=wraplength, bg=bg, fg=fg, relief=relief, font=font)

        self.id       = id
        self.col      = col
        self.row      = row
        self._padx    = _padx
        self._pady    = _pady
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
                 id="", text="", col=None, row=None,
                 justify="left",
                 width=0, show="",
                 _padx=None, _pady=None,
                 bg=VAR.INPUT_COLOR, fg=None,
                 relief=None):

        super().__init__(master=master, justify=justify, width=width, show=show, bg=bg, fg=fg, relief=relief)

        self.id    = id
        self.col   = col
        self.row   = row
        self._padx = _padx
        self._pady = _pady
        self.text  = StringVar(self, text, id)
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
                 id="", check=0, col=None, row=None,
                 label="",
                 justify="left",
                 _padx=None, _pady=None,
                 width=0, command=None,
                 default = False,
                 bg = None,
                 anchor = None):

        super().__init__(master=master, text=label, justify=justify, width=width, command=command, bg=bg, anchor=anchor)

        self.id    = id
        self.col   = col
        self.row   = row
        self._padx = _padx
        self._pady = _pady
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
                 id="", text="", col=None, row=None,
                 justify="left",
                 width=0, height=10,
                 _padx=None, _pady=None,
                 show="", values=None,
                 state=""):

        super().__init__(master=master, justify=justify, width=width, height=height, values=values, state=state)

        self.id    = id
        self.col   = col
        self.row   = row
        self._padx = _padx
        self._pady = _pady

    def setValues(self, values):
        self['values'] = values


######################
# Button_
# --------------------
class Button_(Button):

    # Constructor
    def __init__(self, master=None,
                 id="", text="", col=None, row=None,
                 justify="left",
                 width=None, height=None,
                 _padx=None, _pady=None,
                 state="normal", relief=None,
                 bg=None, fg=None,
                 image=None, command=None,
                 toggle=False):

        super().__init__(master=master, text=text, justify=justify, width=width, height=height, state=state, relief=relief, bg=bg, fg=fg, image=image, command=command)

        self.id          = id
        self.col         = col
        self.row         = row
        self.bg          = bg
        self._padx       = _padx
        self._pady       = _pady
        self.toggle      = toggle
        self.toggleState = False

        if self.toggle:
            self.config(command=self.toggleButtonState)

    def setToggle(self, newToggleState):
        self.toggleState = newToggleState

        if self.toggleState:
            self.config(bg=VAR.BUTTON_COLOR_TOGGLE)
        else:
            self.config(bg=self.bg)

    def toggleButtonState(self):
        self.setToggle(not self.toggleState)


######################
# Text_
# --------------------
class Text_(Text):

    # Constructor
    def __init__(self, master=None,
                 id="", text="", col=None, row=None,
                 width=None, height=None,
                 _padx=None, _pady=None,
                 state="normal", wrap=None):

        super().__init__(master=master, width=width, height=height, state=state, wrap=wrap)

        self.id    = id
        self.col   = col
        self.row   = row
        self._padx = _padx
        self._pady = _pady

    def set(self, value):
        state = self["state"]
        self.config(state="normal")
        self.delete("1.0", "end")
        self.insert("1.0", value)
        self.config(state=state)

    def get(self):
        return super().get("1.0", "end").rstrip('\n')