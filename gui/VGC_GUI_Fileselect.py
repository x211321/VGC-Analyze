from tkinter import *

import os
import glob

import VGC_Var as VAR

from VGC_Widgets import Label_
from VGC_Widgets import Combobox_


######################
# GUI_File
# --------------------
class GUI_File(Frame):

    def __init__(self, master, width=0, height=0, pady=0, padx=0):
        super().__init__(master=master, width=width, height=height, pady=pady, padx=padx)

        self.setCurrentVGCFile = master.setCurrentVGCFile
        self.collectionData    = master.collectionData

        self.init()

    def init(self):
        self.item_select      = Combobox_(self, width=40, values=[os.path.basename(x) for x in glob.glob(VAR.DATA_PATH+VAR.FILE_PREFIX+"*.csv")])
        self.item_select_text = Label_(self, anchor="e", padx=5, text="Active VGC file:")

        self.item_select.pack(side=RIGHT, padx=8)
        self.item_select.sorted = True
        self.item_select.set(os.path.basename(self.collectionData.csv_file))
        self.item_select.bind("<<ComboboxSelected>>", self.setCurrentVGCFile)

        self.item_select_text.pack(side=RIGHT)