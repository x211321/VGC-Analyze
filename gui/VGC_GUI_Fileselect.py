from tkinter import *

import os
import glob

import VGC_Var as VAR

from VGC_Widgets import Label_
from VGC_Widgets import Combobox_
from VGC_Widgets import Checkbutton_


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
        self.file_select_text  = Label_(self, anchor="e", padx=5, text="Active VGC file:")
        self.file_select       = Combobox_(self, width=40, values=[os.path.basename(x) for x in glob.glob(VAR.DATA_PATH+VAR.FILE_PREFIX+"*.csv")])
        self.combine_platforms = Checkbutton_(self, padx=8, label="Combine similar platforms", default=True, command=self.setCurrentVGCFile)

        self.combine_platforms.pack(side=RIGHT)
        self.file_select.pack(side=RIGHT)
        self.file_select_text.pack(side=RIGHT)

        self.file_select.sorted = True
        self.file_select.set(os.path.basename(self.collectionData.csv_file))
        self.file_select.bind("<<ComboboxSelected>>", self.setCurrentVGCFile)

