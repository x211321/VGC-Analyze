from VGC_Locale import _

from tkinter import *
from tkinter import ttk


######################
# initMainMenu
# --------------------
def initMainMenu(gui):
    gui.main_menu = Menu(gui)

    # File menu
    gui.file_menu = Menu(gui.main_menu, tearoff=0)
    gui.file_menu.add_command(label="Quit", command=gui.destroy, accelerator="Ctrl+Q")

    # Search menu
    gui.search_menu = Menu(gui.main_menu, tearoff=0)
    gui.search_menu.add_command(label="Search for item", command=gui.pop_itemSearch.show, accelerator="Ctrl+F")

    # Download menu
    gui.download_menu = Menu(gui.main_menu, tearoff=0)
    gui.download_menu.add_command(label="Download collection", command=gui.pop_collectionDownload.show, accelerator="Ctrl+D")

    # Window menu
    gui.window_menu = Menu(gui.main_menu, tearoff=0)
    gui.window_menu.add_command(label="Filters", command=gui.toggleFilterFrame, accelerator="Alt+F")
    gui.window_menu.add_command(label="Item info", command=gui.toggleItemInfoFrame, accelerator="Alt+I")
    gui.window_menu.add_command(label="Graphs", command=gui.toggleGraphFrame, accelerator="Alt+G")

    # Settings menu
    gui.settings_menu = Menu(gui.main_menu, tearoff=0)
    gui.settings_menu.add_command(label="Settings", command=gui.showSettings)

    # About menu
    gui.about_menu = Menu(gui.main_menu, tearoff=0)
    gui.about_menu.add_command(label="About VGC Analyzer", command=gui.showAbout)

    gui.main_menu.add_cascade(label="File"    , menu=gui.file_menu)
    gui.main_menu.add_cascade(label="Search"  , menu=gui.search_menu)
    gui.main_menu.add_cascade(label="Download", menu=gui.download_menu)
    gui.main_menu.add_cascade(label="Window"  , menu=gui.window_menu)
    gui.main_menu.add_cascade(label="Settings", menu=gui.settings_menu)
    gui.main_menu.add_cascade(label="About"   , menu=gui.about_menu)

    gui.config(menu=gui.main_menu)