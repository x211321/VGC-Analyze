from lib.Locale import _

from tkinter import *
from tkinter import ttk

import os
import glob

import lib.Var as VAR

from lib.Widgets import Label_
from lib.Widgets import Combobox_
from lib.Widgets import Checkbutton_


######################
# GUI_File
# --------------------
class GUI_File(ttk.Frame):

    def __init__(self, master, width=0, height=0):
        super().__init__(master=master, width=width, height=height)

        self.setCurrentVGCFile = master.setCurrentVGCFile
        self.collectionData    = master.collectionData

        self.init()

    def init(self):
        self.file_select_text  = Label_(self, anchor="e", text=_("Active VGC file:"))
        self.file_select       = Combobox_(self, width=40, state="readonly", values=[os.path.basename(x) for x in glob.glob(VAR.DATA_PATH+VAR.FILE_PREFIX+"*.csv")])
        self.combine_platforms = Checkbutton_(self, label=_("Combine related platforms"), default=True, command=self.setCurrentVGCFile)

        self.combine_platforms.pack(side=RIGHT, padx=8)
        self.file_select.pack(side=RIGHT)
        self.file_select_text.pack(side=RIGHT, padx=5)

        self.file_select.sorted = True
        self.file_select.set(os.path.basename(self.collectionData.csv_file))
        self.file_select.bind("<<ComboboxSelected>>", self.setCurrentVGCFile)

