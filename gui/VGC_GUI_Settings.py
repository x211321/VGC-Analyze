import VGC_Settings as settings

from VGC_Locale import _
from VGC_Locale import setLanguage
from VGC_Locale import setLocale
from VGC_Locale import getAvailableLanguageNames
from VGC_Locale import getAvailableLocaleNames
from VGC_Locale import getLocaleCode
from VGC_Locale import getLocaleName

from gui.VGC_GUI_Popups import centerPopup

from tkinter import *
from tkinter import ttk
from VGC_Img import loadIcon

from VGC_Widgets import Label_
from VGC_Widgets import Entry_
from VGC_Widgets import Combobox_
from VGC_Widgets import Checkbutton_

import VGC_Var as VAR


class GUI_Settings(Toplevel):

    def __init__(self, parent, callback = None):
        super().__init__()

        self.parent   = parent
        self.callback = callback

        # Window attributes
        self.wm_title(_("Settings"))
        self.resizable(False, False)
        self.iconphoto(False, loadIcon("settings-outline", 15, 15))
        self.bind('<Escape>', self.close)
        self.focus_force()

        # Add frames
        self.tab_frame = Frame(self, bg=VAR.GUI_COLOR_PRIMARY)
        self.btn_frame = Frame(self, bg=VAR.GUI_COLOR_SECONDARY)

        self.tab_frame.grid(row=0, column=0, sticky="nwse")
        self.btn_frame.grid(row=1, column=0, sticky="nwse")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Add buttons
        self.btn_cancel  = Button(self.btn_frame, text=_("Cancel"), width=20, relief="groove", bg=VAR.BUTTON_COLOR_BAD, command=self.close)
        self.btn_spacer  = Label_(self.btn_frame, bg=VAR.GUI_COLOR_SECONDARY)
        self.btn_confirm = Button(self.btn_frame, text=_("OK"), width=20, relief="groove", bg=VAR.BUTTON_COLOR_GOOD, command=self.apply)

        self.btn_cancel.grid(row=0, column=0, sticky="e", padx=10, pady=20)
        self.btn_spacer.grid(row=0, column=1)
        self.btn_confirm.grid(row=0, column=2, sticky="w", padx=10, pady=20)

        self.btn_frame.columnconfigure(1, weight=1)

        # Load icons
        self.icon_save   = loadIcon("save-outline", 20, 20)
        self.icon_delete = loadIcon("trash-outline", 20, 20)

        # Add tab widget
        self.tab = ttk.Notebook(self.tab_frame)
        self.tab.pack(fill="both")

        # Add tab pages
        self.pages = {}
        self.pages["locale"]          = Frame(self.tab)
        self.pages["display"]         = Frame(self.tab)
        self.pages["download"]        = Frame(self.tab)
        self.pages["platformHolders"] = Frame(self.tab)
        self.pages["platforms"]       = Frame(self.tab)

        for key in self.pages:
            self.pages[key].columnconfigure(0, weight=1)
            self.pages[key].config(bg=VAR.GUI_COLOR_PRIMARY)

        self.tab.add(self.pages["locale"], text=_("Locale"))
        self.tab.add(self.pages["display"], text=_("Display"))
        self.tab.add(self.pages["download"], text=_("Download"))
        self.tab.add(self.pages["platformHolders"], text=_("Platform holders"))
        self.tab.add(self.pages["platforms"], text=_("Platforms"))

        self.w = {}

        # Locale settings
        self.initLocale()

        # Platform holders
        self.initPlatformHolders()

        # Restore settings
        self.restore()

        # Center window
        self.center()

        # Run main loop
        self.mainloop()


    def initLocale(self):
        self.w["locale"] = {}

        self.w["locale"]["language_txt"] = Label_(self.pages["locale"], text=_("Language"))
        self.w["locale"]["language"]     = Combobox_(self.pages["locale"], id="language", values=getAvailableLanguageNames(), width=25, state="readonly")

        self.w["locale"]["locale_txt"]   = Label_(self.pages["locale"], text=_("Locale"))
        self.w["locale"]["locale"]       = Combobox_(self.pages["locale"], id="locale", values=getAvailableLocaleNames(), width=25, state="readonly")

        self.grid(self.w["locale"])


    def initPlatformHolders(self):
        self.platformHolders_input   = Frame(self.pages["platformHolders"], bg=VAR.GUI_COLOR_PRIMARY)
        self.platformHolders_buttons = Frame(self.platformHolders_input, bg=VAR.GUI_COLOR_PRIMARY)
        self.platformHoldersView     = ttk.Treeview(self.pages["platformHolders"])

        self.platformHolder_txt = Label_(self.platformHolders_input, text=_("Platform holder"), bg=VAR.GUI_COLOR_PRIMARY)
        self.platformHolder     = Entry_(self.platformHolders_input, width=25)

        self.platformHolderKeywords_txt  = Label_(self.platformHolders_input, text=_("Platform keywords"), bg=VAR.GUI_COLOR_PRIMARY)
        self.platformHolderKeywords      = Text(self.platformHolders_input, width=50, height=4, wrap=WORD)
        self.platformHolderKeywords_info = Label_(self.platformHolders_input, text=_("(comma separated)"), bg=VAR.GUI_COLOR_PRIMARY)

        self.platformHolder_save   = Button(self.platformHolders_buttons,
                                            image=self.icon_save, bg=VAR.BUTTON_COLOR_GOOD,
                                            relief="groove", command=self.savePlatformHolder)
        self.platformHolder_remove = Button(self.platformHolders_buttons,
                                            image=self.icon_delete,
                                            bg=VAR.BUTTON_COLOR_BAD,
                                            relief="groove", command=self.removePlatformHolder)

        self.platformHolder_txt.grid(row=0, column=0, padx=(0, 10), sticky="nw")
        self.platformHolder.grid(row=0, column=1, padx=(0, 20), sticky="nw")
        self.platformHolderKeywords_txt.grid(row=0, column=2, padx=(0, 10), sticky="ne")
        self.platformHolderKeywords.grid(row=0, column=3, padx=(0, 0), sticky="ne", rowspan=2)
        self.platformHolderKeywords_info.grid(row=1, column=2, padx=(0, 10), sticky="ne")

        self.platformHolders_buttons.grid(row=1, column=0, sticky="nwse")
        self.platformHolder_remove.grid(row=0, column=0, sticky="nw", padx=(0, 10))
        self.platformHolder_save.grid(row=0, column=1, sticky="nw")

        self.platformHolders_input.grid(row=0, column=0, padx=10, pady=10, sticky="nwse")
        self.platformHoldersView.grid(row=1, column=0, padx=10, pady=10, sticky="nwse")

        # Input bindings
        self.platformHolder.bind("<Return>", self.savePlatformHolder)
        self.platformHolderKeywords.bind("<Return>", self.savePlatformHolder)

        # Treeview definition
        self.platformHoldersView['columns']=("Platform holder", "Keywords")

        # Treeview columns
        self.platformHoldersView.column("#0"             , anchor="w", width=0, stretch="No")
        self.platformHoldersView.column("Platform holder", anchor="w", width=100, stretch="No")
        self.platformHoldersView.column("Keywords"       , anchor="w")

        # Treeview column headers
        self.platformHoldersView.heading("#0"             , text=""                    , anchor="w")
        self.platformHoldersView.heading("Platform holder", text=_("Platform holder")  , anchor="w")
        self.platformHoldersView.heading("Keywords"       , text=_("Platform keywords"), anchor="w")

        # Treeview bindings
        self.platformHoldersView.bind('<<TreeviewSelect>>', self.selectPlatformHolder)


    def center(self):
        centerPopup(self, self.parent)


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

            if col > 1:
                col  = 0
                row += 1


    def restore(self):
        for sectionKey in self.w:
            section = self.w[sectionKey]

            for widgetKey in section:
                widget = section[widgetKey]

                if len(widget.id):
                    self.setValue(sectionKey, widget, settings.get(sectionKey, widget.id, ""))

        self.restorePlatformHolders()


    def restorePlatformHolders(self, scrollTo = ""):
        # Clear treeview
        self.platformHoldersView.delete(*self.platformHoldersView.get_children())

        # Clear inputs
        self.platformHolder.set("")
        self.platformHolderKeywords.delete("1.0", "end")

        # Insert platform holders
        if len(settings.listPlatformHolders()):
            for platformHolder in sorted(settings.listPlatformHolders(), reverse=True):
                self.platformHoldersView.insert(parent="",
                                                index=0,
                                                values=(platformHolder, ", ".join(settings.getPlatformHolderKeywords(platformHolder))))

            if len(scrollTo):
                # Find item
                for row in self.platformHoldersView.get_children():
                    if scrollTo == self.platformHoldersView.item(row)["values"][0]:
                        # Scroll into view
                        self.platformHoldersView.see(row)
                        break


    def selectPlatformHolder(self, a = None):
        selection = self.platformHoldersView.focus()

        if len(self.platformHoldersView.item(selection)["values"]):
            self.platformHolder.set(self.platformHoldersView.item(selection)["values"][0])
            self.platformHolderKeywords.delete("1.0", "end")
            self.platformHolderKeywords.insert("1.0", self.platformHoldersView.item(selection)["values"][1])


    def savePlatformHolder(self, a = None):
        platformHolder = self.platformHolder.get()
        keywords = self.platformHolderKeywords.get("1.0", "end").split(",")

        if len(platformHolder) and len(keywords):
            keywords = [keyword.strip().lower() for keyword in keywords]

            settings.setPlatformHolderKeywords(platformHolder, keywords)

            self.restorePlatformHolders(platformHolder)


    def removePlatformHolder(self, a = None):
        platformHolder = self.platformHolder.get()

        if len(platformHolder):
            settings.removePlatformHolder(platformHolder)
            self.restorePlatformHolders(platformHolder)


    def close(self, a = None):
        self.destroy()


    def apply(self):
        for sectionKey in self.w:
            section = self.w[sectionKey]

            for widgetKey in section:
                widget = section[widgetKey]

                if len(widget.id):

                    value = self.getValue(sectionKey, widget)
                    settings.set(sectionKey, widget.id, value)

        settings.write()
        settings.writePlatformHolders()

        setLanguage(settings.get("locale", "language", ""))
        setLocale(settings.get("locale", "locale", ""))

        if not self.callback == None:
            self.callback()

        self.close()


    def getValue(self, sectionKey, widget):
        value = widget.get()

        if sectionKey == "locale" and widget.id == "language":
            return getLocaleCode(value)
        if sectionKey == "locale" and widget.id == "locale":
            return getLocaleCode(value)

        return value


    def setValue(self, sectionKey, widget, value):
        if sectionKey == "locale" and widget.id == "language":
            value = getLocaleName(value)
        if sectionKey == "locale" and widget.id == "locale":
            value = getLocaleName(value)

        widget.set(value)




