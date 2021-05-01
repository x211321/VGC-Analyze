import VGC_Settings as settings

from VGC_Locale import _
from VGC_Locale import setLanguage
from VGC_Locale import setLocale
from VGC_Locale import getAvailableLanguageNames
from VGC_Locale import getAvailableLocaleNames
from VGC_Locale import getLocaleCode
from VGC_Locale import getLocaleName

from gui.VGC_GUI_Popups import centerPopup
from gui.VGC_GUI_Popups import Pop_FilterSelect

import VGC_Var as VAR

from tkinter import *
from tkinter import ttk
from VGC_Img import loadIcon

from VGC_Widgets import Label_
from VGC_Widgets import Entry_
from VGC_Widgets import Text_
from VGC_Widgets import Button_
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
        self.withdraw()

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

        # Display settings
        self.initDisplay()

        # Platform holders
        self.initPlatformHolders()

        # Platforms
        self.initPlatforms()

        # Restore settings
        self.restore()

        # Center window
        self.center()

        # Display window
        self.deiconify()

        # Run main loop
        self.mainloop()


    def initLocale(self):
        self.w["locale"] = {}

        self.w["locale"]["language_txt"] = Label_(self.pages["locale"], text=_("Language (requires restart)"))
        self.w["locale"]["language"]     = Combobox_(self.pages["locale"], id="language", values=getAvailableLanguageNames(), width=25, state="readonly")

        self.w["locale"]["locale_txt"]   = Label_(self.pages["locale"], text=_("Locale"))
        self.w["locale"]["locale"]       = Combobox_(self.pages["locale"], id="locale", values=getAvailableLocaleNames(), width=25, state="readonly")

        self.grid(self.w["locale"])


    def initDisplay(self):
        self.columnSelectPop = Pop_FilterSelect(self, self.columnSelectCallback)

        self.w["display"] = {}
        self.w["display"]["columns_txt"]    = Label_(self.pages["display"], text=_("Table columns"), bg=VAR.GUI_COLOR_PRIMARY)
        self.w["display"]["columns"]        = Text_(self.pages["display"], width=50, height=4, wrap=WORD, state="disabled", id="columns")
        self.w["display"]["columns_spacer"] = Label_(self.pages["display"], bg=VAR.GUI_COLOR_PRIMARY)
        self.w["display"]["columns_select"] = Button_(self.pages["display"], text=_("Select"), width=20, relief="groove", bg=VAR.GUI_COLOR_PRIMARY, command=self.columnSelect)

        self.grid(self.w["display"])


    def initPlatformHolders(self):
        self.platformHolders_input   = Frame(self.pages["platformHolders"], bg=VAR.GUI_COLOR_PRIMARY)
        self.platformHolders_buttons = Frame(self.platformHolders_input, bg=VAR.GUI_COLOR_PRIMARY)

        self.platformHoldersViewFrame = Frame(self.pages["platformHolders"], bg=VAR.GUI_COLOR_PRIMARY)
        self.platformHoldersView      = ttk.Treeview(self.platformHoldersViewFrame)
        self.platformHoldersViewScroll= Scrollbar(self.platformHoldersViewFrame)

        self.platformHolder_txt = Label_(self.platformHolders_input, text=_("Platform holder"), bg=VAR.GUI_COLOR_PRIMARY)
        self.platformHolder     = Entry_(self.platformHolders_input, width=25)

        self.platformHolderKeywords_txt  = Label_(self.platformHolders_input, text=_("Platform keywords"), bg=VAR.GUI_COLOR_PRIMARY)
        self.platformHolderKeywords      = Text_(self.platformHolders_input, width=50, height=4, wrap=WORD)
        self.platformHolderKeywords_info = Label_(self.platformHolders_input, text=_("(comma separated)"), bg=VAR.GUI_COLOR_PRIMARY)

        self.platformHolder_save   = Button_(self.platformHolders_buttons,
                                             image=self.icon_save, bg=VAR.BUTTON_COLOR_GOOD,
                                             relief="groove", command=self.savePlatformHolder)
        self.platformHolder_remove = Button_(self.platformHolders_buttons,
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

        self.platformHoldersViewScroll.pack(side=RIGHT, fill=Y)
        self.platformHoldersView.pack(expand=True, fill="both")

        self.platformHolders_input.grid(row=0, column=0, padx=10, pady=10, sticky="nwse")
        self.platformHoldersViewFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nwse")

        # Input bindings
        self.platformHolder.bind("<Return>", self.savePlatformHolder)
        self.platformHolderKeywords.bind("<Return>", self.savePlatformHolder)

        # Scrollbar bindings
        self.platformHoldersView.config(yscrollcommand=self.platformHoldersViewScroll.set)
        self.platformHoldersViewScroll.config(orient=VERTICAL, command=self.platformHoldersView.yview)

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


    def initPlatforms(self):
        self.platforms_input    = Frame(self.pages["platforms"], bg=VAR.GUI_COLOR_PRIMARY)
        self.platforms_buttons  = Frame(self.platforms_input, bg=VAR.GUI_COLOR_PRIMARY)
        self.platformsViewFrame = Frame(self.pages["platforms"], bg=VAR.GUI_COLOR_PRIMARY)
        self.platformsView      = ttk.Treeview(self.platformsViewFrame)
        self.platformsViewScroll= Scrollbar(self.platformsViewFrame)

        self.platform_txt = Label_(self.platforms_input, text=_("Platform"), bg=VAR.GUI_COLOR_PRIMARY)
        self.platform     = Entry_(self.platforms_input, width=37)

        self.platformOverwrite_txt  = Label_(self.platforms_input, text=_("Overwrite with"), bg=VAR.GUI_COLOR_PRIMARY)
        self.platformOverwrite      = Entry_(self.platforms_input, width=70)

        self.platform_save   = Button_(self.platforms_buttons,
                                       image=self.icon_save, bg=VAR.BUTTON_COLOR_GOOD,
                                       relief="groove", command=self.savePlatform)
        self.platform_remove = Button_(self.platforms_buttons,
                                       image=self.icon_delete,
                                       bg=VAR.BUTTON_COLOR_BAD,
                                       relief="groove", command=self.removePlatform)

        self.platform_txt.grid(row=0, column=0, padx=(0, 10), sticky="nw")
        self.platform.grid(row=0, column=1, padx=(0, 20), sticky="nw")
        self.platformOverwrite_txt.grid(row=0, column=2, padx=(0, 10), sticky="ne")
        self.platformOverwrite.grid(row=0, column=3, padx=(0, 0), sticky="ne", rowspan=2)

        self.platforms_buttons.grid(row=1, column=0, sticky="nwse")
        self.platform_remove.grid(row=0, column=0, sticky="nw", padx=(0, 10), pady=(11, 0))
        self.platform_save.grid(row=0, column=1, sticky="nw", pady=(11, 0))

        self.platformsViewScroll.pack(side=RIGHT, fill=Y)
        self.platformsView.pack(expand=True, fill="both")

        self.platforms_input.grid(row=0, column=0, padx=10, pady=10, sticky="nwse")
        self.platformsViewFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nwse")

        # Input bindings
        self.platform.bind("<Return>", self.savePlatform)
        self.platformOverwrite.bind("<Return>", self.savePlatform)

        # Scrollbar bindings
        self.platformsView.config(yscrollcommand=self.platformsViewScroll.set)
        self.platformsViewScroll.config(orient=VERTICAL, command=self.platformsView.yview)

        # Treeview definition
        self.platformsView['columns']=("Platform", "Overwrite with")

        # Treeview columns
        self.platformsView.column("#0"            , anchor="w", width=0, stretch="No")
        self.platformsView.column("Platform"      , anchor="w", width=250, stretch="No")
        self.platformsView.column("Overwrite with", anchor="w")

        # Treeview column headers
        self.platformsView.heading("#0"            , text=""                 , anchor="w")
        self.platformsView.heading("Platform"      , text=_("Platform")      , anchor="w")
        self.platformsView.heading("Overwrite with", text=_("Overwrite with"), anchor="w")

        # Treeview bindings
        self.platformsView.bind('<<TreeviewSelect>>', self.selectPlatform)


    def columnSelect(self):
        self.columnSelectPop.show(VAR.VIEW_COLUMNS.items(), settings.get("display", "columns", []), _("table columns"), maxCol=3)


    def columnSelectCallback(self, columns):
        self.setValue("display", self.w["display"]["columns"], columns)

    def center(self):
        centerPopup(self, self.parent)


    def grid(self, widgets):
        row = 0
        col = 0

        for key in widgets:
            if not widgets[key].__class__.__name__ == "Combobox_":
                widgets[key].config(bg=VAR.GUI_COLOR_PRIMARY)

            if col == 0:
                sticky = "nw"
            if col == 1:
                sticky = "ne"

            widgets[key].grid(row=row, column=col, sticky=sticky, padx=20, pady=10)

            col += 1

            if col > 1:
                col  = 0
                row += 1


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
        platformHolder = self.platformHolder.get().strip()
        keywords = self.platformHolderKeywords.get("1.0", "end").split(",")

        if len(platformHolder) and len(keywords):
            keywords = [keyword.strip().lower() for keyword in keywords]

            settings.setPlatformHolderKeywords(platformHolder, keywords)

            self.restorePlatformHolders(platformHolder)


    def removePlatformHolder(self, a = None):
        platformHolder = self.platformHolder.get().strip()

        if len(platformHolder):
            settings.removePlatformHolder(platformHolder)
            self.restorePlatformHolders(platformHolder)


    def restorePlatforms(self, scrollTo = ""):
        # Clear treeview
        self.platformsView.delete(*self.platformsView.get_children())

        # Clear inputs
        self.platform.set("")
        self.platformOverwrite.set("")

        # Insert platforms
        if len(settings.listPlatforms()):
            for platform in sorted(settings.listPlatforms(), reverse=True):
                self.platformsView.insert(parent="",
                                          index=0,
                                          values=(platform, settings.getPlatformOverwrite(platform)))

            if len(scrollTo):
                # Find item
                for row in self.platformsView.get_children():
                    if scrollTo == self.platformsView.item(row)["values"][0]:
                        # Scroll into view
                        self.platformsView.see(row)
                        break


    def selectPlatform(self, a = None):
        selection = self.platformsView.focus()

        if len(self.platformsView.item(selection)["values"]):
            self.platform.set(self.platformsView.item(selection)["values"][0])
            self.platformOverwrite.set(self.platformsView.item(selection)["values"][1])


    def savePlatform(self, a = None):
        platform  = self.platform.get().strip()
        overwrite = self.platformOverwrite.get().strip()

        if len(platform) and len(overwrite):
            settings.setPlatformOverwrite(platform, overwrite)

            self.restorePlatforms(platform)


    def removePlatform(self, a = None):
        platform = self.platform.get().strip()

        if len(platform):
            settings.removePlatform(platform)
            self.restorePlatforms(platform)


    def close(self, a = None):
        self.destroy()


    def restore(self):
        for sectionKey in self.w:
            section = self.w[sectionKey]

            for widgetKey in section:
                widget = section[widgetKey]

                if len(widget.id):
                    self.setValue(sectionKey, widget, settings.get(sectionKey, widget.id, ""))

        self.restorePlatformHolders()
        self.restorePlatforms()


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
        settings.writePlatforms()

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
        if sectionKey == "display" and widget.id == "columns":
            return value.split(", ")

        return value


    def setValue(self, sectionKey, widget, value):
        if sectionKey == "locale" and widget.id == "language":
            value = getLocaleName(value)
        if sectionKey == "locale" and widget.id == "locale":
            value = getLocaleName(value)
        if sectionKey == "display" and widget.id =="columns":
            value = ", ".join(value)

        widget.set(value)




