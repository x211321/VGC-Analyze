from tkinter import *
from tkinter import ttk

from VGC_Widgets import Label_
from VGC_Widgets import Entry_
from VGC_Widgets import Combobox_


######################
# GUI_Filter
# --------------------
class GUI_Filter(Frame):

    def __init__(self, master, width=0, height=0, pady=0, padx=0):
        super().__init__(master=master, width=width, height=height, pady=pady, padx=padx)

        self.showData       = master.showData
        self.collectionData = master.collectionData

        self.init()


    def init(self):
        # Filter inputs
        # ------------------
        self.filterInputs = {}

        self.filterInputs["name_txt"]           = Label_(self, width=25, text="Title")
        self.filterInputs["name"]               = Entry_(self, width=30)
        self.filterInputs["platform_txt"]       = Label_(self, width=25, text="Platform")
        self.filterInputs["platform"]           = Combobox_(self, width=27)
        self.filterInputs["platformHolder_txt"] = Label_(self, width=25, text="Platform holder")
        self.filterInputs["platformHolder"]     = Combobox_(self, width=27)
        self.filterInputs["region_txt"]         = Label_(self, width=25, text="Region")
        self.filterInputs["region"]             = Combobox_(self, width=27)
        self.filterInputs["notes_txt"]          = Label_(self, width=25, text="Notes")
        self.filterInputs["notes"]              = Entry_(self, width=30)
        self.filterInputs["dateStart_txt"]      = Label_(self, width=25, text="Min. purchase date")
        self.filterInputs["dateStart"]          = Entry_(self, width=30)
        self.filterInputs["dateEnd_txt"]        = Label_(self, width=25, text="Max. purchase date")
        self.filterInputs["dateEnd"]            = Entry_(self, width=30)
        self.filterInputs["priceStart_txt"]     = Label_(self, width=25, text="Min. purchase price")
        self.filterInputs["priceStart"]         = Entry_(self, width=30)
        self.filterInputs["priceEnd_txt"]       = Label_(self, width=25, text="Max. purchase price")
        self.filterInputs["priceEnd"]           = Entry_(self, width=30)
        self.filterInputs["group_txt"]          = Label_(self, text="Group by", width=25)
        self.filterInputs["group"]              = Combobox_(self, state="readonly", width=27)
        self.filterInputs["cart_txt"]           = Label_(self, width=10, text="Cart")
        self.filterInputs["box_txt"]            = Label_(self, width=10, text="Box")
        self.filterInputs["cart"]               = Combobox_(self, values=("", "Yes", "No"), state="readonly", width=10)
        self.filterInputs["box"]                = Combobox_(self, values=("", "Yes", "No"), state="readonly", width=10)
        self.filterInputs["manual_txt"]         = Label_(self, width=10, text="Manual")
        self.filterInputs["other_txt"]          = Label_(self, width=10, text="Other")
        self.filterInputs["manual"]             = Combobox_(self, values=("", "Yes", "No"), state="readonly", width=10)
        self.filterInputs["other"]              = Combobox_(self, values=("", "Yes", "No"), state="readonly", width=10)
        self.filterInputs["bookmarked_txt"]     = Label_(self, text="Bookmarked", width=10)
        self.filterInputs["finished_txt"]       = Label_(self, text="Finished", width=10)
        self.filterInputs["bookmarked"]         = Combobox_(self, values=("", "Yes", "No"), state="readonly", width=10)
        self.filterInputs["finished"]           = Combobox_(self, values=("", "Yes", "No"), state="readonly", width=10)
        self.filterInputs["order_txt"]          = Label_(self, text="Sort by", width=10)
        self.filterInputs["order_dir_txt"]      = Label_(self, text="Sort direction", width=10)
        self.filterInputs["order"]              = Combobox_(self, state="readonly", width=10)
        self.filterInputs["orderDirection"]     = Combobox_(self, values=("", "ascending", "descending"), state="readonly", width=10)

        self.filter_apply = Button(self, width=10, relief="groove", bg="#BDF593")
        self.filter_reset = Button(self, width=10, relief="groove", bg="#F59398")

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
                self.filterInputs[key].grid(pady=(0,5))

            self.filterInputs[key].bind('<Return>', self.showData)

        self.filter_reset.config(text="Reset filter", command=self.reset)
        self.filter_reset.grid(row=100, column=0, sticky="nw", pady=(20, 5))

        self.filter_apply.config(text="Apply filter", command=self.showData)
        self.filter_apply.grid(row=100, column=1, sticky="nw", pady=(20, 5))


    ######################
    # reset
    # --------------------
    def reset(self):
        for key in self.filterInputs:
            if self.filterInputs[key].__class__.__name__ == "Entry_":
                self.filterInputs[key].delete(0, END)
            if self.filterInputs[key].__class__.__name__ == "Combobox_":
                self.filterInputs[key].set("")

        self.showData()


    ######################
    # fillPlatformCombobox
    # --------------------
    def fillPlatformCombobox(self):
        platforms = []
        self.filterInputs["platform"].delete(0, END)

        platforms.append("")

        for platform, data in sorted(self.collectionData.platforms.items()):
            platforms.append(platform)

        self.filterInputs["platform"].setValues(platforms)


    ######################
    # fillPlatformHolderCombobox
    # --------------------
    def fillPlatformHolderCombobox(self):
        platformHolders = []
        self.filterInputs["platformHolder"].delete(0, END)

        platformHolders.append("")

        for platformHolder, data in sorted(self.collectionData.platformHolders.items()):
            platformHolders.append(platformHolder)

        self.filterInputs["platformHolder"].setValues(platformHolders)


    ######################
    # fillRegionCombobox
    # --------------------
    def fillRegionCombobox(self):
        regions = []
        self.filterInputs["region"].delete(0, END)

        for region, data in sorted(self.collectionData.regions.items()):
            regions.append(region)

        self.filterInputs["region"].setValues(regions)


    ######################
    # fillGroupCombobox
    # --------------------
    def fillGroupCombobox(self):
        groups = []
        self.filterInputs["region"].delete(0, END)

        groups.append("")
        groups.append("year")
        groups.append("month")
        groups.append("day")
        groups.append("name")
        groups.append("region")
        groups.append("platform")
        groups.append("platform holder")
        groups.append("notes")

        self.filterInputs["group"].setValues(groups)


    ######################
    # fillOrderCombobox
    # --------------------
    def fillOrderCombobox(self):
        orders = []
        self.filterInputs["order"].delete(0, END)

        orders.append("")
        orders.append("name")
        orders.append("price")
        orders.append("date")
        orders.append("region")
        orders.append("platform")
        orders.append("notes")

        self.filterInputs["order"].setValues(orders)
