from lib.Locale import _
import lib.Settings as settings

from tkinter import *
from tkinter import ttk

from lib.Widgets import Label_
from lib.Widgets import Entry_
from lib.Widgets import Combobox_
from lib.Widgets import Button_
from lib.Widgets import BorderButton_
from lib.Img import loadIcon

from gui.GUI_Popups import Pop_FilterSelect
from gui.GUI_Popups import Pop_DatePicker

import lib.Var as VAR


######################
# GUI_Filter
# --------------------
class GUI_Filter(ttk.Frame):

    def __init__(self, master, width=0, height=0):
        super().__init__(master=master, width=width, height=height, style=VAR.FRAME_STYLE_SECONDARY)

        self.showData       = master.showData
        self.collectionData = master.collectionData

        self.platformSelect       = Pop_FilterSelect(master, self.selectPlatformsCallback)
        self.platformHolderSelect = Pop_FilterSelect(master, self.selectPlatformHoldersCallback)
        self.regionSelect         = Pop_FilterSelect(master, self.selectRegionsCallback)

        self.datePicker = Pop_DatePicker(master, self.datePickerCallback)

        self.regexIcon = loadIcon("regex-outline", 15, 15)
        self.dateIcon  = loadIcon("calendar-outline", 15, 15)

        self.init()


    def init(self):
        # Multi filter
        # ------------------
        self.multiFilter  = {}
        self.multiFilter["platforms"] = []
        self.multiFilter["platformHolders"] = []
        self.multiFilter["regions"] = []

        # Filter inputs
        # ------------------
        self.filterInputs = {}

        self.filterInputs["name_txt"]   = Label_(self, width=25, _pady=(0,0), text=_("Title"))
        self.filterInputs["name_frame"] = ttk.Frame(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["name"]       = Entry_(self.filterInputs["name_frame"], width=25, row=0, col=0, _padx=(0,10))
        self.filterInputs["name_regex"] = BorderButton_(self.filterInputs["name_frame"], width=15, row=0, col=1, height=13, image=self.regexIcon, relief="groove", bg=VAR.GUI_COLOR_PRIMARY, toggle=True)

        self.filterInputs["notes_txt"]   = Label_(self, width=25, _pady=(2,0), text=_("Notes"))
        self.filterInputs["notes_frame"] = ttk.Frame(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["notes"]       = Entry_(self.filterInputs["notes_frame"], width=25, row=0, col=0, _padx=(0,10))
        self.filterInputs["notes_regex"] = BorderButton_(self.filterInputs["notes_frame"], width=15, row=0, col=1, height=13, image=self.regexIcon, relief="groove", bg=VAR.GUI_COLOR_PRIMARY, toggle=True)

        self.filterInputs["platforms_txt"]          = Label_(self, width=25, _pady=(2,0), text=_("Platforms"))
        self.filterInputs["platforms_select"]       = Button_(self, width=25, id="select", text=_("Select"), relief="groove", command=self.selectPlatforms, bg=VAR.INPUT_COLOR)
        self.filterInputs["platformHolders_txt"]    = Label_(self, width=25, _pady=(2,0), text=_("Platform holders"))
        self.filterInputs["platformHolders_select"] = Button_(self, width=25, id="select", text=_("Select"), relief="groove", command=self.selectPlatformHolders, bg=VAR.INPUT_COLOR)
        self.filterInputs["regions_txt"]            = Label_(self, width=25, _pady=(2,0), text=_("Regions"))
        self.filterInputs["regions_select"]         = Button_(self, width=25, id="select", text=_("Select"), relief="groove", command=self.selectRegions, bg=VAR.INPUT_COLOR)

        self.filterInputs["dateStart_txt"]          = Label_(self, width=25, _pady=(2,0), text=_("Min. date (purchased)"))
        self.filterInputs["dateStart_frame"]        = ttk.Frame(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["dateStart"]              = Entry_(self.filterInputs["dateStart_frame"], width=25, row=0, col=0, _padx=(0,10))
        self.filterInputs["dateStart_pick"]         = Button_(self.filterInputs["dateStart_frame"], width=15, row=0, col=1, height=13,
                                                              image=self.dateIcon, relief="groove", bg=VAR.GUI_COLOR_PRIMARY,
                                                              command=lambda:self.datePicker.show(self.filterInputs["dateStart"], self.filterInputs["dateStart"].get(), "start"))

        self.filterInputs["dateEnd_txt"]            = Label_(self, width=25, _pady=(2,0), text=_("Max. date (purchased)"))
        self.filterInputs["dateEnd_frame"]          = ttk.Frame(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["dateEnd"]                = Entry_(self.filterInputs["dateEnd_frame"], width=25, row=0, col=0, _padx=(0,10))
        self.filterInputs["dateEnd_pick"]           = Button_(self.filterInputs["dateEnd_frame"], width=15, row=0, col=1, height=13,
                                                              image=self.dateIcon, relief="groove", bg=VAR.GUI_COLOR_PRIMARY,
                                                              command=lambda:self.datePicker.show(self.filterInputs["dateEnd"], self.filterInputs["dateEnd"].get(), "end"))

        self.filterInputs["dateAddedStart_txt"]     = Label_(self, width=25, _pady=(2,0), text=_("Min. date (added)"))
        self.filterInputs["dateAddedStart_frame"]   = ttk.Frame(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["dateAddedStart"]         = Entry_(self.filterInputs["dateAddedStart_frame"], width=25, row=0, col=0, _padx=(0,10))
        self.filterInputs["dateAddedStart_pick"]    = Button_(self.filterInputs["dateAddedStart_frame"], width=15, row=0, col=1, height=13,
                                                              image=self.dateIcon, relief="groove", bg=VAR.GUI_COLOR_PRIMARY,
                                                              command=lambda:self.datePicker.show(self.filterInputs["dateAddedStart"], self.filterInputs["dateAddedStart"].get(), "start"))


        self.filterInputs["dateAddedEnd_txt"]     = Label_(self, width=25, _pady=(2,0), text=_("Max. date (added)"))
        self.filterInputs["dateAddedEnd_frame"]   = ttk.Frame(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["dateAddedEnd"]         = Entry_(self.filterInputs["dateAddedEnd_frame"], width=25, row=0, col=0, _padx=(0,10))
        self.filterInputs["dateAddedEnd_pick"]    = Button_(self.filterInputs["dateAddedEnd_frame"], width=15, row=0, col=1, height=13,
                                                              image=self.dateIcon, relief="groove", bg=VAR.GUI_COLOR_PRIMARY,
                                                              command=lambda:self.datePicker.show(self.filterInputs["dateAddedEnd"], self.filterInputs["dateAddedEnd"].get(), "end"))

        self.filterInputs["priceStart_txt"]         = Label_(self, width=25, _pady=(2,0), text=_("Min. purchase price"))
        self.filterInputs["priceStart"]             = Entry_(self, width=30)
        self.filterInputs["priceEnd_txt"]           = Label_(self, width=25, _pady=(2,0), text=_("Max. purchase price"))
        self.filterInputs["priceEnd"]               = Entry_(self, width=30)
        self.filterInputs["group_txt"]              = Label_(self, width=25, _pady=(2,0), text=_("Group by"))
        self.filterInputs["group"]                  = Combobox_(self, width=27, height=20, state="readonly")

        self.filterInputs["cb_frame"] = ttk.Frame(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["cart_txt"] = Label_(self.filterInputs["cb_frame"], width=10, _pady=(2,0), row=0, col=0, _padx=(0,18), text=_("Cart"))
        self.filterInputs["box_txt"]  = Label_(self.filterInputs["cb_frame"], width=10, _pady=(2,0), row=0, col=1, text=_("Box"))
        self.filterInputs["cart"]     = Combobox_(self.filterInputs["cb_frame"], width=10, row=1, col=0, _padx=(0,18), state="readonly")
        self.filterInputs["box"]      = Combobox_(self.filterInputs["cb_frame"], width=10, row=1, col=1, state="readonly")

        self.filterInputs["mo_frame"]   = ttk.Frame(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["manual_txt"] = Label_(self.filterInputs["mo_frame"], width=10, _pady=(2,0), row=0, col=0, _padx=(0,18), text=_("Manual"))
        self.filterInputs["other_txt"]  = Label_(self.filterInputs["mo_frame"], width=10, _pady=(2,0), row=0, col=1, text=_("Other"))
        self.filterInputs["manual"]     = Combobox_(self.filterInputs["mo_frame"], width=10, row=1, col=0, _padx=(0,18), state="readonly")
        self.filterInputs["other"]      = Combobox_(self.filterInputs["mo_frame"], width=10, row=1, col=1, state="readonly")

        self.filterInputs["bf_frame"]       = ttk.Frame(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["bookmarked_txt"] = Label_(self.filterInputs["bf_frame"], width=10, _pady=(2,0), row=0, col=0, _padx=(0,18), text=_("Bookmarked"))
        self.filterInputs["finished_txt"]   = Label_(self.filterInputs["bf_frame"], width=10, _pady=(2,0), row=0, col=1, text=_("Finished"))
        self.filterInputs["bookmarked"]     = Combobox_(self.filterInputs["bf_frame"], width=10, row=1, col=0, _padx=(0,18), state="readonly")
        self.filterInputs["finished"]       = Combobox_(self.filterInputs["bf_frame"], width=10, row=1, col=1, state="readonly")

        self.filterInputs["oo_frame"]       = ttk.Frame(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["order_txt"]      = Label_(self.filterInputs["oo_frame"], width=10, _pady=(2,0), row=0, col=0, _padx=(0,18), text=_("Sort by"))
        self.filterInputs["order_dir_txt"]  = Label_(self.filterInputs["oo_frame"], width=10, _pady=(2,0), row=0, col=1, text=_("Sort direction"))
        self.filterInputs["order"]          = Combobox_(self.filterInputs["oo_frame"], width=10, row=1, col=0, _padx=(0,18), state="readonly")
        self.filterInputs["orderDirection"] = Combobox_(self.filterInputs["oo_frame"], width=10, row=1, col=1, state="readonly")

        if settings.get("display", "refreshOnFilterSelect", True):
            self.bindComboboxes()

        self.fillYesNoComboboxes()
        self.fillOrderDirectionCombobox()

        self.filter_button_frame = ttk.Frame(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filter_apply = Button_(self.filter_button_frame, width=10, relief="groove", bg=VAR.BUTTON_COLOR_GOOD)
        self.filter_reset = Button_(self.filter_button_frame, width=10, relief="groove", bg=VAR.BUTTON_COLOR_BAD)

        rowCount = 0

        for key in self.filterInputs:
            widget = self.filterInputs[key]

            col  = 0
            row  = rowCount
            padx = 0
            pady = 0

            if widget.__class__.__name__[-1] == "_":
                if not widget.col == None:
                    col = widget.col
                if not widget.row == None:
                    row = widget.row
                if not widget._padx == None:
                    padx = widget._padx
                if not widget._pady == None:
                    pady = widget._pady

            widget.grid(row=row, column=col, sticky="nw", padx=padx, pady=pady)
            widget.bind("<Return>", self.showData)
            rowCount += 1

        self.filter_button_frame.grid(row=rowCount, column=0, padx=0, pady=0, sticky="nw")

        self.filter_reset.config(text=_("Reset filter"), command=self.reset)
        self.filter_reset.grid(row=0, column=0, sticky="nw", padx=(0,22), pady=(10, 5))

        self.filter_apply.config(text=_("Apply filter"), command=self.showData)
        self.filter_apply.grid(row=0, column=1, sticky="nw", pady=(10, 5))


    ######################
    # reset
    # --------------------
    def reset(self, noShow=False):
        for key in self.filterInputs:
            widget = self.filterInputs[key]

            if widget.__class__.__name__ == "Entry_":
                widget.delete(0, END)
            if widget.__class__.__name__ == "Combobox_":
                widget.set("")
            if widget.__class__.__name__ == "Button_" or widget.__class__.__name__ == "BorderButton_":
                if widget.id == "select":
                    self.filterInputs[key].config(text=_("Select"), bg=VAR.GUI_COLOR_PRIMARY)
                if widget.toggle:
                    widget.setToggle(False)

        self.multiFilter["platforms"] = []
        self.multiFilter["platformHolders"] = []
        self.multiFilter["regions"] = []

        if not noShow:
            self.showData()


    ######################
    # restore
    # --------------------
    def restore(self, template):
        self.reset(True)

        for key in template:

            value = template[key]

            if type(value) == str and len(value):
                value = _(template[key])

            if key in self.multiFilter:
                if len(value):
                    self.multiFilter[key] = value
                    self.filterInputs[key + "_select"].config(text=str(len(value)) + _(" selected"), bg=VAR.BUTTON_COLOR_TOGGLE)
                continue
            if key in self.filterInputs:
                widget = self.filterInputs[key]

                if widget.__class__.__name__ == "Entry_" or widget.__class__.__name__ == "Combobox_":
                    widget.set(value)

                if widget.__class__.__name__ == "Button_" or widget.__class__.__name__ == "BorderButton_":
                    if widget.toggle:
                        widget.setToggle(value)


    ######################
    # selectPlatforms
    # --------------------
    def selectPlatforms(self):
        self.platformSelect.show(sorted(self.collectionData.platforms_all.items()), self.multiFilter["platforms"], _("platforms"))


    ######################
    # selectPlatformsCallback
    # --------------------
    def selectPlatformsCallback(self, platforms):
        self.multiFilter["platforms"] = platforms

        if len(platforms):
            self.filterInputs["platforms_select"].config(text=str(len(platforms)) + _(" selected"), bg=VAR.BUTTON_COLOR_TOGGLE)
        else:
            self.filterInputs["platforms_select"].config(text=_("Select"), bg=VAR.GUI_COLOR_PRIMARY)

        if settings.get("display", "refreshOnFilterSelect", True):
            self.showData()


    ######################
    # selectPlatformHolders
    # --------------------
    def selectPlatformHolders(self):
        self.platformHolderSelect.show(sorted(self.collectionData.platformHolders_all.items()), self.multiFilter["platformHolders"], _("platform holders"))


    ######################
    # selectPlatformHoldersCallback
    # --------------------
    def selectPlatformHoldersCallback(self, platformHolders):
        self.multiFilter["platformHolders"] = platformHolders

        if len(platformHolders):
            self.filterInputs["platformHolders_select"].config(text=str(len(platformHolders)) + _(" selected"), bg=VAR.BUTTON_COLOR_TOGGLE)
        else:
            self.filterInputs["platformHolders_select"].config(text=_("Select"), bg=VAR.GUI_COLOR_PRIMARY)

        if settings.get("display", "refreshOnFilterSelect", True):
            self.showData()


    ######################
    # selectRegions
    # --------------------
    def selectRegions(self):
        self.regionSelect.show(sorted(self.collectionData.regions_all.items()), self.multiFilter["regions"], _("regions"))


    ######################
    # selectRegionsCallback
    # --------------------
    def selectRegionsCallback(self, regions):
        self.multiFilter["regions"] = regions

        if len(regions):
            self.filterInputs["regions_select"].config(text=str(len(regions)) + _(" selected"), bg=VAR.BUTTON_COLOR_TOGGLE)
        else:
            self.filterInputs["regions_select"].config(text=_("Select"), bg=VAR.GUI_COLOR_PRIMARY)

        if settings.get("display", "refreshOnFilterSelect", True):
            self.showData()


    ######################
    # fillGroupCombobox
    # --------------------
    def fillGroupCombobox(self):
        groups = []
        self.filterInputs["group"].delete(0, END)

        groups.append("")

        for key in VAR.GROUP_BY.keys():
            groups.append(VAR.GROUP_BY[key])

        self.filterInputs["group"].setValues(groups)


    ######################
    # fillOrderCombobox
    # --------------------
    def fillOrderCombobox(self):
        orders = []
        self.filterInputs["order"].delete(0, END)

        orders.append("")
        for key in VAR.ORDER_BY.keys():
            orders.append(VAR.ORDER_BY[key])

        self.filterInputs["order"].setValues(orders)


    ######################
    # fillOrderDirectionCombobox
    # --------------------
    def fillOrderDirectionCombobox(self):
        directions = []
        self.filterInputs["orderDirection"].delete(0, END)

        directions.append("")
        for key in VAR.ORDER_DIRECTION.keys():
            directions.append(VAR.ORDER_DIRECTION[key])

        self.filterInputs["orderDirection"].setValues(directions)


    ######################
    # fillYesNoComboboxes
    # --------------------
    def fillYesNoComboboxes(self):
        options = []

        options.append("")
        for key in VAR.ATTRIBUTE_YN.keys():
            options.append(VAR.ATTRIBUTE_YN[key])

        self.filterInputs["cart"].setValues(options)
        self.filterInputs["box"].setValues(options)
        self.filterInputs["manual"].setValues(options)
        self.filterInputs["other"].setValues(options)
        self.filterInputs["bookmarked"].setValues(options)
        self.filterInputs["finished"].setValues(options)


    ######################
    # unbindComboboxes
    # --------------------
    def unbindComboboxes(self):
        for inputKey in self.filterInputs:
            input = self.filterInputs[inputKey]
            if input.__class__.__name__ == "Combobox_":
                input.unbind("<<ComboboxSelected>>")


    ######################
    # bindComboboxes
    # --------------------
    def bindComboboxes(self):
        for inputKey in self.filterInputs:
            input = self.filterInputs[inputKey]
            if input.__class__.__name__ == "Combobox_":
                input.bind("<<ComboboxSelected>>", self.showData)


    ######################
    # datePickerCallback
    # --------------------
    def datePickerCallback(self):
        if settings.get("display", "refreshOnFilterSelect", True):
            self.showData()
