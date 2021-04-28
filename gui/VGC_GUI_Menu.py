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
    gui.file_menu.add_command(label=_("Quit"), command=gui.destroy, accelerator="Ctrl+Q")

    # Search menu
    gui.search_menu = Menu(gui.main_menu, tearoff=0)
    gui.search_menu.add_command(label=_("Search for item"), command=gui.pop_itemSearch.show, accelerator="Ctrl+F")

    # Download menu
    gui.download_menu = Menu(gui.main_menu, tearoff=0)
    gui.download_menu.add_command(label=_("Download collection"), command=gui.pop_collectionDownload.show, accelerator="Ctrl+D")

    # Window menu
    gui.window_menu = Menu(gui.main_menu, tearoff=0)
    gui.window_menu.add_command(label=_("Filters"), command=gui.toggleFilterFrame, accelerator="Alt+F")
    gui.window_menu.add_command(label=_("Item info"), command=gui.toggleItemInfoFrame, accelerator="Alt+I")
    gui.window_menu.add_command(label=_("Graphs"), command=gui.toggleGraphFrame, accelerator="Alt+G")

    # Settings menu
    gui.settings_menu = Menu(gui.main_menu, tearoff=0)
    gui.settings_menu.add_command(label=_("Settings"), command=gui.showSettings)

    # About menu
    gui.about_menu = Menu(gui.main_menu, tearoff=0)
    gui.about_menu.add_command(label=_("About VGC Analyzer"), command=gui.showAbout)

    gui.main_menu.add_cascade(label=_("File")    , menu=gui.file_menu)
    gui.main_menu.add_cascade(label=_("Search")  , menu=gui.search_menu)
    gui.main_menu.add_cascade(label=_("Download"), menu=gui.download_menu)
    gui.main_menu.add_cascade(label=_("Window")  , menu=gui.window_menu)
    gui.main_menu.add_cascade(label=_("Settings"), menu=gui.settings_menu)
    gui.main_menu.add_cascade(label=_("About")   , menu=gui.about_menu)

    gui.config(menu=gui.main_menu)