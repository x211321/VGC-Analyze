from lib.Locale import _

import os
import platform
import threading
import time
import ctypes

from tkinter import *
from tkinter import ttk

from lib.Img import loadImage
from lib.Img import loadAnimationFrame

import lib.Var as VAR


######################
# AnimationThread
# --------------------
class AnimationThread(threading.Thread):
    def __init__(self, widget, animation, frames, interval):

        self.widget    = widget
        self.animation = animation
        self.frames    = frames
        self.interval  = interval

        threading.Thread.__init__(self)

    def run(self):
        try:
            frame = 0

            while True:
                time.sleep(self.interval / 1000)

                self.image = loadAnimationFrame(self.animation, frame)
                self.widget.config(image=self.image)

                frame += 1

                if frame == self.frames:
                    frame = 0
        finally:
            pass

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def kill(self):
        thread_id = self.get_id()

        result = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if result > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)


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
                 relief=None, highlight_bg=None):

        super().__init__(master=master, width=width, height=height, anchor=anchor,
                         justify=justify, wraplength=wraplength, bg=bg, fg=fg,
                         relief=relief, font=font)

        self.id           = id
        self.col          = col
        self.row          = row
        self._padx        = _padx
        self._pady        = _pady
        self.imgdef       = imgdef
        self.text         = StringVar(self, text, id)
        self.imgwidth     = imgwidth
        self.bg           = bg
        self.highlight_bg = highlight_bg

        self.animationThread = None

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

    def startAnimation(self, img, frames, interval):
        self.stopAnimation()
        self.animationThread = AnimationThread(self, img, frames, interval)
        self.animationThread.start()

    def stopAnimation(self):
        if not self.animationThread == None:
            self.animationThread.kill()

    def highlight(self):
        if not self.highlight_bg == None:
            self.config(bg=self.highlight_bg)

    def restore_bg(self):
        if not self.bg == None:
            self.config(bg=self.bg)

    def set_bg(self, bg):
        self.bg = bg
        self.restore_bg()


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
                 id="", col=None, row=None,
                 justify="left",
                 width=0, height=10,
                 _padx=None, _pady=None,
                 values=None, state=""):

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
                 toggle=False, borderButton=False):

        super().__init__(master=master, text=text, justify=justify, width=width, height=height, state=state, relief=relief, bg=bg, fg=fg, image=image, command=command)

        self.id          = id
        self.col         = col
        self.row         = row
        self.bg          = bg
        self._padx       = _padx
        self._pady       = _pady
        self.toggle      = toggle
        self.toggleState = False
        self.master      = master
        self.borderButton= borderButton

        if self.toggle:
            self.config(command=self.toggleButtonState)

    def setToggle(self, newToggleState):
        self.toggleState = newToggleState

        if self.toggleState:
            self.config(bg=VAR.BUTTON_COLOR_TOGGLE)
        else:
            self.config(bg=self.bg)

        if self.borderButton == True:
            self.master.setBorderToggle()

    def toggleButtonState(self):
        self.setToggle(not self.toggleState)



######################
# BorderButton_
# --------------------
# Combination of LabelFrame and Button
# as a workaround for the missing button
# colors under macOS
class BorderButton_(LabelFrame):
    # Constructor
    def __init__(self, master=None,
                 id="", text="", col=None, row=None,
                 justify="left",
                 width=None, height=None,
                 _padx=None, _pady=None,
                 state="normal", relief=None,
                 bg=None, fg=None,
                 image=None, command=None,
                 toggle=False, border_bg=None, border_bd=0):

        if platform.system() == "Darwin":
            if border_bd == 0:
                border_bd = 2

        self.id          = id
        self.col         = col
        self.row         = row
        self.bg          = bg
        self._padx       = _padx
        self._pady       = _pady
        self.toggle      = toggle
        self.toggleState = False
        self.border_bd   = border_bd

        super().__init__(master=master, padx=border_bd, pady=border_bd, bg=border_bg, bd=0)

        if not border_bg == None:
            self.border_bg = border_bg
        else:
            self.border_bg = self.cget("bg")

        if not width == None and width > border_bd:
            width = width - border_bd
        if not height == None and height > border_bd:
            height = height - border_bd

        self.button = Button_(master=self, id=id, text=text, col=col, row=row, justify=justify,
                              width=width, height=height, _padx=_padx, _pady=_pady, state=state,
                              relief=relief, bg=bg, fg=fg, image=image, command=command, toggle=toggle, borderButton=True)

        self.button.grid()

    def setToggle(self, newToggleState):
        self.button.setToggle(newToggleState)

    def toggleButtonState(self):
        self.button.toggleButtonState()

    def setBorderToggle(self):
        # Gets triggered by the button that's inside
        # this LabelFrame
        self.toggleState = self.button.toggleState

        if self.toggleState:
            self.config(bg=VAR.BUTTON_COLOR_TOGGLE)
        else:
            self.config(bg=self.border_bg)




######################
# Text_
# --------------------
class Text_(Text):

    # Constructor
    def __init__(self, master=None,
                 id="", col=None, row=None,
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