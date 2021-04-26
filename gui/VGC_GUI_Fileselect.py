from tkinter import *

import os
import glob

from VGC_Widgets import Label_
from VGC_Widgets import Combobox_

from VGC_Var     import DATA_PATH
from VGC_Var     import FILE_PREFIX

def initFileSelect(gui):
    gui.item_select               = Combobox_(gui.file_frame, width=40, values=[os.path.basename(x) for x in glob.glob(DATA_PATH+FILE_PREFIX+"*.csv")])
    gui.item_select_text          = Label_(gui.file_frame, anchor="e", padx=5, text="Active VGC file:")

    gui.item_select.pack(side=RIGHT, padx=8)
    gui.item_select.sorted = True
    gui.item_select.set(os.path.basename(gui.collectionData.csv_file))
    gui.item_select.bind("<<ComboboxSelected>>", gui.setCurrentVGCFile)

    gui.item_select_text.pack(side=RIGHT)