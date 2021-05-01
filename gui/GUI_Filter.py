from lib.Locale import _

from tkinter import *
from tkinter import ttk

from lib.Widgets import Label_
from lib.Widgets import Entry_
from lib.Widgets import Combobox_

from gui.GUI_Popups import Pop_FilterSelect

import lib.Var as VAR


######################
# GUI_Filter
# --------------------
class GUI_Filter(Frame):

    def __init__(self, master, width=0, height=0, pady=0, padx=0):
        super().__init__(master=master, width=width, height=height, pady=pady, padx=padx)

        self.showData       = master.showData
        self.collectionData = master.collectionData

        self.platformSelect       = Pop_FilterSelect(master, self.selectPlatformsCallback)
        self.platformHolderSelect = Pop_FilterSelect(master, self.selectPlatformHoldersCallback)
        self.regionSelect         = Pop_FilterSelect(master, self.selectRegionsCallback)

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

        self.filterInputs["name_txt"]               = Label_(self, width=25, text=_("Title"))
        self.filterInputs["name"]                   = Entry_(self, width=30)
        self.filterInputs["platforms_txt"]          = Label_(self, width=25, text=_("Platforms"))
        self.filterInputs["platforms_select"]       = Button(self, width=25, text=_("Select"), relief="groove", command=self.selectPlatforms, bg=VAR.INPUT_COLOR)
        self.filterInputs["platformHolders_txt"]    = Label_(self, width=25, text=_("Platform holders"))
        self.filterInputs["platformHolders_select"] = Button(self, width=25, text=_("Select"), relief="groove", command=self.selectPlatformHolders, bg=VAR.INPUT_COLOR)
        self.filterInputs["regions_txt"]            = Label_(self, width=25, text=_("Regions"))
        self.filterInputs["regions_select"]         = Button(self, width=25, text=_("Select"), relief="groove", command=self.selectRegions, bg=VAR.INPUT_COLOR)
        self.filterInputs["notes_txt"]              = Label_(self, width=25, text=_("Notes"))
        self.filterInputs["notes"]                  = Entry_(self, width=30)
        self.filterInputs["dateStart_txt"]          = Label_(self, width=25, text=_("Min. date (purchased)"))
        self.filterInputs["dateStart"]              = Entry_(self, width=30)
        self.filterInputs["dateEnd_txt"]            = Label_(self, width=25, text=_("Max. date (purchased)"))
        self.filterInputs["dateEnd"]                = Entry_(self, width=30)
        self.filterInputs["dateAddedStart_txt"]     = Label_(self, width=25, text=_("Min. date (added)"))
        self.filterInputs["dateAddedStart"]         = Entry_(self, width=30)
        self.filterInputs["dateAddedEnd_txt"]       = Label_(self, width=25, text=_("Max. date (added)"))
        self.filterInputs["dateAddedEnd"]           = Entry_(self, width=30)
        self.filterInputs["priceStart_txt"]         = Label_(self, width=25, text=_("Min. purchase price"))
        self.filterInputs["priceStart"]             = Entry_(self, width=30)
        self.filterInputs["priceEnd_txt"]           = Label_(self, width=25, text=_("Max. purchase price"))
        self.filterInputs["priceEnd"]               = Entry_(self, width=30)
        self.filterInputs["group_txt"]              = Label_(self, text=_("Group by"), width=25)
        self.filterInputs["group"]                  = Combobox_(self, state="readonly", width=27)
        self.filterInputs["cart_txt"]               = Label_(self, width=10, text=_("Cart"))
        self.filterInputs["box_txt"]                = Label_(self, width=10, text=_("Box"))
        self.filterInputs["cart"]                   = Combobox_(self, values=("", VAR.ITEM_ATTRIBUTE_YES, VAR.ITEM_ATTRIBUTE_NO), state="readonly", width=10)
        self.filterInputs["box"]                    = Combobox_(self, values=("", VAR.ITEM_ATTRIBUTE_YES, VAR.ITEM_ATTRIBUTE_NO), state="readonly", width=10)
        self.filterInputs["manual_txt"]             = Label_(self, width=10, text=_("Manual"))
        self.filterInputs["other_txt"]              = Label_(self, width=10, text=_("Other"))
        self.filterInputs["manual"]                 = Combobox_(self, values=("", VAR.ITEM_ATTRIBUTE_YES, VAR.ITEM_ATTRIBUTE_NO), state="readonly", width=10)
        self.filterInputs["other"]                  = Combobox_(self, values=("", VAR.ITEM_ATTRIBUTE_YES, VAR.ITEM_ATTRIBUTE_NO), state="readonly", width=10)
        self.filterInputs["bookmarked_txt"]         = Label_(self, text=_("Bookmarked"), width=10)
        self.filterInputs["finished_txt"]           = Label_(self, text=_("Finished"), width=10)
        self.filterInputs["bookmarked"]             = Combobox_(self, values=("", VAR.ITEM_ATTRIBUTE_YES, VAR.ITEM_ATTRIBUTE_NO), state="readonly", width=10)
        self.filterInputs["finished"]               = Combobox_(self, values=("", VAR.ITEM_ATTRIBUTE_YES, VAR.ITEM_ATTRIBUTE_NO), state="readonly", width=10)
        self.filterInputs["order_txt"]              = Label_(self, text=_("Sort by"), width=10)
        self.filterInputs["order_dir_txt"]          = Label_(self, text=_("Sort direction"), width=10)
        self.filterInputs["order"]                  = Combobox_(self, state="readonly", width=10)
        self.filterInputs["orderDirection"]         = Combobox_(self, values=("", VAR.ORDER_DIRECTION_ASCENDING, VAR.ORDER_DIRECTION_DESCENDING), state="readonly", width=10)

        self.filter_apply = Button(self, width=10, relief="groove", bg=VAR.BUTTON_COLOR_GOOD)
        self.filter_reset = Button(self, width=10, relief="groove", bg=VAR.BUTTON_COLOR_BAD)

        row = 0
        col = 0

        itemWidth        = 0
        colspan          = 0
        rowWidth         = 25
        rowWidth_current = 0

        for key in self.filterInputs:
            itemWidth = self.filterInputs[key]['width']

            if rowWidth_current and (rowWidth_current + itemWidth <= rowWidth):
                col +=1

            rowWidth_current += itemWidth

            if rowWidth_current >= rowWidth:
                rowWidth_current = itemWidth
                row += 1
                col  = 0

            if itemWidth >= rowWidth:
                colspan = 2
            else:
                colspan = 1
                if col == 0:
                    self.filterInputs[key].grid(padx=(0, 18))

            self.filterInputs[key].grid(row=row, column=col, sticky="nw", columnspan=colspan)

            if (row) % 2 == 0:
                self.filterInputs[key].grid(pady=(0,3))

            self.filterInputs[key].bind("<Return>", self.showData)

        self.filter_reset.config(text=_("Reset filter"), command=self.reset)
        self.filter_reset.grid(row=100, column=0, sticky="nw", pady=(10, 5))

        self.filter_apply.config(text=_("Apply filter"), command=self.showData)
        self.filter_apply.grid(row=100, column=1, sticky="nw", pady=(10, 5))


    ######################
    # reset
    # --------------------
    def reset(self):
        for key in self.filterInputs:
            if self.filterInputs[key].__class__.__name__ == "Entry_":
                self.filterInputs[key].delete(0, END)
            if self.filterInputs[key].__class__.__name__ == "Combobox_":
                self.filterInputs[key].set("")
            if self.filterInputs[key].__class__.__name__ == "Button":
                self.filterInputs[key].config(text=_("Select"))

        self.multiFilter["platforms"] = []
        self.multiFilter["platformHolders"] = []
        self.multiFilter["regions"] = []

        self.showData()


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
            self.filterInputs["platforms_select"].config(text=str(len(platforms)) + _(" selected"))
        else:
            self.filterInputs["platforms_select"].config(text=_("Select"))


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
            self.filterInputs["platformHolders_select"].config(text=str(len(platformHolders)) + _(" selected"))
        else:
            self.filterInputs["platformHolders_select"].config(text=_("Select"))


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
            self.filterInputs["regions_select"].config(text=str(len(regions)) + _(" selected"))
        else:
            self.filterInputs["regions_select"].config(text=_("Select"))


    ######################
    # fillGroupCombobox
    # --------------------
    def fillGroupCombobox(self):
        groups = []
        self.filterInputs["group"].delete(0, END)

        groups.append("")
        groups.append(VAR.GROUP_BY_YEAR)
        groups.append(VAR.GROUP_BY_MONTH)
        groups.append(VAR.GROUP_BY_DAY)
        groups.append(VAR.GROUP_BY_YEAR_ADDED)
        groups.append(VAR.GROUP_BY_MONTH_ADDED)
        groups.append(VAR.GROUP_BY_DAY_ADDED)
        groups.append(VAR.GROUP_BY_NAME)
        groups.append(VAR.GROUP_BY_REGION)
        groups.append(VAR.GROUP_BY_PLATFORM)
        groups.append(VAR.GROUP_BY_PLATFORMHOLDER)
        groups.append(VAR.GROUP_BY_NOTES)

        self.filterInputs["group"].setValues(groups)


    ######################
    # fillOrderCombobox
    # --------------------
    def fillOrderCombobox(self):
        orders = []
        self.filterInputs["order"].delete(0, END)

        orders.append("")
        orders.append(VAR.ORDER_BY_NAME)
        orders.append(VAR.ORDER_BY_PRICE)
        orders.append(VAR.ORDER_BY_DATE)
        orders.append(VAR.ORDER_BY_DATE_ADDED)
        orders.append(VAR.ORDER_BY_REGION)
        orders.append(VAR.ORDER_BY_PLATFORM)
        orders.append(VAR.ORDER_BY_NOTES)

        self.filterInputs["order"].setValues(orders)
