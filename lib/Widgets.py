from lib.Locale import _

import os
import time

from tkinter import *
from tkinter import ttk

from lib.Img import loadImage
from lib.Img import loadAnimationFrame
from lib.Thread import Thread_

import lib.Var as VAR


######################
# Label_
# --------------------
class Label_(ttk.Label):

    # Constructor
    def __init__(self,
                 master=None,
                 text="",
                 style="",
                 anchor="nw",
                 justify="left",
                 width=0,
                 wraplength=0,
                 font=None,
                 relief=None,
                 _padx=None, _pady=None,
                 _id="",
                 _col=None, _row=None,
                 _img="",
                 _imgdef="",
                 _imgwidth=0,
                 _highlight_style=None):

        # Get Style from parent if available
        if not len(style) and hasattr(master, "defaultLabelStyle"):
            style = master.defaultLabelStyle

        super().__init__(master=master, style=style, width=width, anchor=anchor,
                         justify=justify, wraplength=wraplength,
                         relief=relief, font=font, takefocus=False)

        self._style           = style
        self._id              = _id
        self._col             = _col
        self._row             = _row
        self._padx            = _padx
        self._pady            = _pady
        self._imgdef          = _imgdef
        self._text            = StringVar(self, text, _id)
        self._imgwidth        = _imgwidth
        self._highlight_style = _highlight_style

        self.animationThread = None

        # Set display text
        self.config(textvariable=self._text)

        # Set image
        self.setImage(_img, self._imgwidth)

    def get(self):
        return self._text.get()

    def set(self, text):
        self._text.set(text)

    def setImage(self, img, imgwidth=0):
        if imgwidth > 0:
            self._imgwidth = imgwidth

        if not os.path.exists(img):
            img = self._imgdef

        if len(img) > 0:
            self._image = loadImage(img, self._imgwidth)
            self.config(image=self._image)

    def startAnimation(self, animation, frames, interval):
        self.stopAnimation()
        self.animationThread = Thread_(target = lambda:self.runAnimation(animation, frames, interval))
        self.animationThread.start()

    def stopAnimation(self):
        if not self.animationThread == None:
            self.animationThread.kill()
            self.animationThread.join()

    def runAnimation(self, animation, frames, interval):
        frame = 0

        while True:
            time.sleep(interval / 1000)

            image = loadAnimationFrame(animation, frame)
            self.config(image=image)

            frame += 1

            if frame == frames:
                frame = 0

    def highlight(self):
        if not self._highlight_style == None:
            self.config(style=self._highlight_style)

    def restore_style(self):
        if not self._style == None:
            self.config(style=self._style)

    def set_style(self, style):
        self._style = style
        self.restore_style()


######################
# Frame_
# --------------------
class Frame_(ttk.Frame):
    # Constructor
    def __init__(self,
                 master=None,
                 style="",
                 width=None,
                 height=None,
                 borderwidth=None,
                 relief=None):

        self._id   = ""
        self._col  = None
        self._row  = None
        self._padx = None
        self._pady = None

        super().__init__(master=master, style=style, width=width, height=height, borderwidth=borderwidth, relief=relief)

        self.defaultLabelStyle = ""

        # Get Style from parent if available
        if hasattr(master, "defaultLabelStyle"):
            self.defaultLabelStyle = master.defaultLabelStyle

    def setDefaultLabelStyle(self, style):
        self.defaultLabelStyle = style


######################
# Entry_
# --------------------
class Entry_(ttk.Entry):

    # Constructor
    def __init__(self,
                 master=None,
                 text="",
                 style="",
                 justify="left",
                 width=0,
                 show="",
                 font=None,
                 _id="",
                 _padx=None, _pady=None,
                 _col=None, _row=None):

        super().__init__(master=master, justify=justify, width=width, show=show, style=style, font=font)

        self._id   = _id
        self._col  = _col
        self._row  = _row
        self._padx = _padx
        self._pady = _pady
        self._text  = StringVar(self, text, _id)
        self.config(textvariable=self._text)

    def get(self):
        return self._text.get()

    def set(self, text):
        self._text.set(text)


######################
# Checkbutton_
# --------------------
class Checkbutton_(ttk.Checkbutton):

    # Constructor
    def __init__(self,
                 master=None,
                 style="",
                 check=0,
                 label="",
                 anchor = None,
                 width=0,
                 command=None,
                 _id="",
                 _col=None, _row=None,
                 _padx=None, _pady=None,
                 ):

        super().__init__(master=master, text=label, style=style, width=width, command=command, anchor=anchor)

        self._id    = _id
        self._col   = _col
        self._row   = _row
        self._padx  = _padx
        self._pady  = _pady
        self._value = IntVar(self, check, _id)
        self.config(variable=self._value)

    def get(self):
        return self._value.get()

    def set(self, newValue):
        self._value.set(newValue)


######################
# Combobox_
# --------------------
class Combobox_(ttk.Combobox):

    # Constructor
    def __init__(self,
                 master=None,
                 style="",
                 justify="left",
                 width=0, height=10,
                 values=None,
                 state="",
                 _id="",
                 _col=None, _row=None,
                 _padx=None, _pady=None):

        super().__init__(master=master, justify=justify, width=width, height=height, values=values, state=state, style=style)

        self._id   = _id
        self._col  = _col
        self._row  = _row
        self._padx = _padx
        self._pady = _pady

    def setValues(self, values):
        self['values'] = values


######################
# LabelButton_
# --------------------
class LabelButton_(ttk.Label):

    # Constructor
    def __init__(self,
                 master=None,
                 style="",
                 text="",
                 width=None,
                 state="normal",
                 image=None,
                 command=None,
                 compound=None,
                 _toggle=False,
                 _id="",
                 _col=None, _row=None,
                 _padx=None, _pady=None):

        if len(text) and image and compound == None:
            compound = "left"

        if not len(style):
            style = VAR.LABELBUTTON_STYLE_DEFAULT

        super().__init__(master=master, style=style,
                         text=text, width=width,
                         state=state,
                         image=image, compound=compound,
                         takefocus=False)

        self._style        = style
        self._command      = command
        self._id           = _id
        self._col          = _col
        self._row          = _row
        self._padx         = _padx
        self._pady         = _pady
        self._toggle       = _toggle
        self._toggleState  = False
        self._master       = master

        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<Button-1>", self._press)
        self.bind("<ButtonRelease-1>", self._click)

        if self._toggle:
            self._command = self.toggleButtonState

    def _click(self, a = None):
        self.config(style=VAR.LABELBUTTON_STYLE_HOVER)
        self._command()

    def _press(self, a = None):
        self.config(style=VAR.LABELBUTTON_STYLE_PRESSED)

    def _enter(self, a = None):
        self.config(style=VAR.LABELBUTTON_STYLE_HOVER)

    def _leave(self, a = None):
        if self._toggle and self._toggleState:
            self.config(style=VAR.LABELBUTTON_STYLE_TOGGLED)
        else:
            self.config(style=self._style)

    def setToggle(self, newToggleState):
        self._toggleState = newToggleState

        if self._toggleState:
            self.config(style=VAR.LABELBUTTON_STYLE_TOGGLED)
        else:
            self.config(style=self._style)

    def toggleButtonState(self):
        self.setToggle(not self._toggleState)

    def setStyle(self, style):
        self._style = style
        self.config(style=self._style)


######################
# Text_
# --------------------
class Text_(Text):

    # Constructor
    def __init__(self,
                 master=None,
                 width=None,
                 height=None,
                 state="normal",
                 wrap=None,
                 _id="",
                 _col=None, _row=None,
                 _padx=None, _pady=None):

        super().__init__(master=master, width=width, height=height, state=state, wrap=wrap)

        self._id   = _id
        self._col  = _col
        self._row  = _row
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
