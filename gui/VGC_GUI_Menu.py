from tkinter import *
from tkinter import ttk


######################
# initMainMenu
# --------------------
def initMainMenu(gui):
    gui.main_menu = Menu(gui.main_window)

    # File menu
    gui.file_menu = Menu(gui.main_menu, tearoff=0)
    gui.file_menu.add_command(label="Quit", command=gui.main_window.destroy, accelerator="Ctrl+Q")

    # Search menu
    gui.search_menu = Menu(gui.main_menu, tearoff=0)
    gui.search_menu.add_command(label="Search for item", command=gui.pop_itemSearch.show, accelerator="Ctrl+F")

    # Download menu
    gui.download_menu = Menu(gui.main_menu, tearoff=0)
    gui.download_menu.add_command(label="Download collection", command=gui.pop_collectionDownload.show, accelerator="Ctrl+D")

    # About menu
    gui.about_menu = Menu(gui.main_menu, tearoff=0)
    gui.about_menu.add_command(label="About VGC Analyzer", command=gui.showAbout)

    gui.main_menu.add_cascade(label="File"    , menu=gui.file_menu)
    gui.main_menu.add_cascade(label="Search"  , menu=gui.search_menu)
    gui.main_menu.add_cascade(label="Download", menu=gui.download_menu)
    gui.main_menu.add_cascade(label="About"   , menu=gui.about_menu)

    gui.main_window.config(menu=gui.main_menu)