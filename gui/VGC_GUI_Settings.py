import VGC_Settings as settings

from VGC_Locale import _
from VGC_Locale import available_languages

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
        btn_cancel  = Button(btn_frame, text=_("Cancel"), width=20, relief="groove", bg=VAR.BUTTON_COLOR_BAD, command=self.close)
        btn_spacer  = Label_(btn_frame, bg=VAR.GUI_COLOR_SECONDARY)
        btn_confirm = Button(btn_frame, text=_("OK"), width=20, relief="groove", bg=VAR.BUTTON_COLOR_GOOD, command=self.apply)

        btn_cancel.grid(row=0, column=0, sticky="e", padx=10, pady=20)
        btn_spacer.grid(row=0, column=1)
        btn_confirm.grid(row=0, column=2, sticky="w", padx=10, pady=20)

        btn_frame.columnconfigure(1, weight=1)

        # Add tab widget
        tab = ttk.Notebook(tab_frame)
        tab.pack(fill="both")

        # Add tab pages
        pages = {}
        pages["locale"]         = Frame(tab)
        pages["display"]        = Frame(tab)
        pages["download"]       = Frame(tab)
        pages["platformHolders"] = Frame(tab)
        pages["platforms"]      = Frame(tab)

        for key in pages:
            pages[key].columnconfigure(0, weight=1)
            pages[key].config(bg=VAR.GUI_COLOR_PRIMARY)

        tab.add(pages["locale"], text=_("Locale"))
        tab.add(pages["display"], text=_("Display"))
        tab.add(pages["download"], text=_("Download"))
        tab.add(pages["platformHolders"], text=_("Platform holders"))
        tab.add(pages["platforms"], text=_("Platforms"))

        self.w = {}

        # Locale settings
        self.w["locale"] = {}

        self.w["locale"]["language_txt"] = Label_(pages["locale"], text=_("Language"))
        self.w["locale"]["language"]     = Combobox_(pages["locale"], id="language", values=available_languages, width=10)

        self.grid(self.w["locale"])

        # Restore settings
        self.restore()

        # Run main loop
        self.mainloop()

    def grid(self, widgets):
        row = 0
        col = 0

        for key in widgets:
            if not widgets[key].__class__.__name__ == "Combobox_":
                widgets[key].config(bg=VAR.GUI_COLOR_PRIMARY)

            if col == 0:
                sticky = "w"
            if col == 1:
                sticky = "e"

            widgets[key].grid(row=row, column=col, sticky=sticky, padx=20, pady=10)

            col += 1
            if col > 2:
                row += 1

    def restore(self):
        for sectionKey in self.w:
            section = self.w[sectionKey]

            for widgetKey in section:
                widget = section[widgetKey]

                if len(widget.id):
                    widget.set(settings.get(sectionKey, widget.id, ""))

    def close(self):
        self.destroy()

    def apply(self):
        for sectionKey in self.w:
            section = self.w[sectionKey]

            for widgetKey in section:
                widget = section[widgetKey]

                if len(widget.id):
                    settings.set(sectionKey, widget.id, widget.get())

        settings.write()
        self.close()




