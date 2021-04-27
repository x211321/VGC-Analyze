from tkinter import *
from tkinter import ttk
from VGC_Img import loadIcon

from VGC_Widgets import Label_
from VGC_Widgets import Entry_
from VGC_Widgets import Combobox_
from VGC_Widgets import Checkbutton_

import VGC_Var as VAR


class GUI_Settings(Toplevel):

    def __init__(self, parent):
        super().__init__()

        w = 700
        h = 500

        # Calculate position relative to main parent
        x = int(parent.winfo_x() + (parent.winfo_width() / 2) - (w / 2))
        y = int(parent.winfo_y() + (parent.winfo_height() / 2) - (h / 2))

        # Window attributes
        self.wm_title("Settings")
        self.geometry(str(w)+"x"+str(h)+"+"+str(x)+"+"+str(y))
        self.resizable(False, False)
        self.iconphoto(False, loadIcon("settings-outline", 15, 15))
        self.bind('<Escape>', self.destroy)
        self.focus_force()

        # Add frames
        tab_frame = Frame(self, bg=VAR.GUI_COLOR_PRIMARY)
        btn_frame = Frame(self, bg=VAR.GUI_COLOR_SECONDARY)

        tab_frame.grid(row=0, column=0, sticky="nwse")
        btn_frame.grid(row=1, column=0, sticky="nwse")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Add buttons
        btn_cancel  = Button(btn_frame, text="Cancel", width=20, relief="groove", bg=VAR.BUTTON_COLOR_BAD)
        btn_spacer  = Label_(btn_frame, bg=VAR.GUI_COLOR_SECONDARY)
        btn_confirm = Button(btn_frame, text="OK", width=20, relief="groove", bg=VAR.BUTTON_COLOR_GOOD)

        btn_cancel.grid(row=0, column=0, sticky="e", padx=10, pady=20)
        btn_spacer.grid(row=0, column=1)
        btn_confirm.grid(row=0, column=2, sticky="w", padx=10, pady=20)

        btn_frame.columnconfigure(1, weight=1)

        # Add tab widget
        tab = ttk.Notebook(tab_frame)
        tab.pack(fill="both")

        # Add tab pages
        display_settings_frame        = Frame(tab)
        platformHolder_keywords_frame = Frame(tab)
        platform_overwrites_frame     = Frame(tab)

        tab.add(display_settings_frame, text="Display settings")
        tab.add(platformHolder_keywords_frame, text="Platform holder keywords")
        tab.add(platform_overwrites_frame, text="Platform overwrites")


        # Run main loop
        self.mainloop()

