from lib.Locale import _
import lib.Settings as settings

from tkinter import *

from lib.Widgets import *
from lib.Img import loadIcon
from gui.popups.FilterSelect import FilterSelect
from gui.popups.DatePicker import DatePicker

import lib.Var as VAR


######################
# GUI_Filter
# --------------------
class GUI_Filter(Frame_):

    def __init__(self, master, width=0, height=0):
        super().__init__(master=master, width=width, height=height, style=VAR.FRAME_STYLE_SECONDARY)

        self.setDefaultLabelStyle(VAR.LABEL_STYLE_SECONDARY)

        self.showData       = master.showData
        self.collectionData = master.collectionData

        self.platformSelect       = FilterSelect(master, self.selectPlatformsCallback)
        self.platformHolderSelect = FilterSelect(master, self.selectPlatformHoldersCallback)
        self.regionSelect         = FilterSelect(master, self.selectRegionsCallback)

        self.datePicker = DatePicker(master, self.datePickerCallback)

        self.regexIcon   = loadIcon("regex-outline", 13, 13)
        self.dateIcon    = loadIcon("calendar-outline", 13, 13)
        self.confirmIcon = loadIcon("checkmark-outline", 15, 15)
        self.cancelIcon  = loadIcon("close-outline", 15, 15)

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

        self.filterInputs["name_frame"] = Frame_(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["name_frame"].columnconfigure(0, minsize=205)
        self.filterInputs["name_frame"].columnconfigure(1, minsize=10)
        self.filterInputs["name_txt"]   = Label_(self.filterInputs["name_frame"], _row=0, _col=0, text=_("Title"), _pady=(4,0))
        self.filterInputs["name"]       = Entry_(self.filterInputs["name_frame"], _row=1, _col=0)
        self.filterInputs["name_regex"] = LabelButton_(self.filterInputs["name_frame"], _row=1, _col=2, image=self.regexIcon, _toggle=True)

        self.filterInputs["notes_frame"] = Frame_(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["notes_frame"].columnconfigure(0, minsize=205)
        self.filterInputs["notes_frame"].columnconfigure(1, minsize=10)
        self.filterInputs["notes_txt"]   = Label_(self.filterInputs["notes_frame"], _row=0, _col=0, text=_("Notes"),  _pady=(2,0))
        self.filterInputs["notes"]       = Entry_(self.filterInputs["notes_frame"], _row=1, _col=0)
        self.filterInputs["notes_regex"] = LabelButton_(self.filterInputs["notes_frame"], _row=1, _col=2, image=self.regexIcon, _toggle=True)


        self.filterInputs["platReg_frame"]          = Frame_(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["platReg_frame"].columnconfigure(0, minsize=116)
        self.filterInputs["platReg_frame"].columnconfigure(1, minsize=10)
        self.filterInputs["platReg_frame"].columnconfigure(2, minsize=116)
        self.filterInputs["platforms_txt"]          = Label_(self.filterInputs["platReg_frame"], _row=0, _col=0, _pady=(2,0), text=_("Platforms"))
        self.filterInputs["regions_txt"]            = Label_(self.filterInputs["platReg_frame"], _row=0, _col=2, _pady=(2,0), text=_("Regions"))
        self.filterInputs["platforms_select"]       = LabelButton_(self.filterInputs["platReg_frame"], _row=1, _col=0, _id="select", text=_("Select"), command=self.selectPlatforms)
        self.filterInputs["regions_select"]         = LabelButton_(self.filterInputs["platReg_frame"], _row=1, _col=2, _id="select", text=_("Select"), command=self.selectRegions)


        self.filterInputs["platformHoldersFrame"]   = Frame_(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["platformHoldersFrame"].columnconfigure(0, minsize=242)

        self.filterInputs["platformHolders_txt"]    = Label_(self.filterInputs["platformHoldersFrame"], _row=0, _col=0, _pady=(2,0), text=_("Platform holders"))
        self.filterInputs["platformHolders_select"] = LabelButton_(self.filterInputs["platformHoldersFrame"], _row=1, _col=0, _id="select", text=_("Select"), command=self.selectPlatformHolders)


        self.filterInputs["dateFrame"]           = Frame_(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["dateFrame"].columnconfigure(0, minsize=205)
        self.filterInputs["dateFrame"].columnconfigure(1, minsize=10)

        self.filterInputs["dateStart_txt"]       = Label_(self.filterInputs["dateFrame"], _row=0, _col=0, text=_("Min. date (purchased)"), _pady=(2,0))
        self.filterInputs["dateStart"]           = Entry_(self.filterInputs["dateFrame"], _row=1, _col=0)
        self.filterInputs["dateStart_pick"]      = LabelButton_(self.filterInputs["dateFrame"], _row=1, _col=2,
                                                                image=self.dateIcon,
                                                                command=lambda:self.datePicker.show(self.filterInputs["dateStart"],
                                                                                                    self.filterInputs["dateStart_pick"],
                                                                                                    self.filterInputs["dateStart"].get(),
                                                                                                    "start"))

        self.filterInputs["dateEnd_txt"]         = Label_(self.filterInputs["dateFrame"], _row=2, _col=0, text=_("Max. date (purchased)"), _pady=(2,0))
        self.filterInputs["dateEnd"]             = Entry_(self.filterInputs["dateFrame"], _row=3, _col=0)
        self.filterInputs["dateEnd_pick"]        = LabelButton_(self.filterInputs["dateFrame"], _row=3, _col=2,
                                                                image=self.dateIcon,
                                                                command=lambda:self.datePicker.show(self.filterInputs["dateEnd"],
                                                                                                    self.filterInputs["dateEnd_pick"],
                                                                                                    self.filterInputs["dateEnd"].get(),
                                                                                                    "end"))

        self.filterInputs["dateAddedStart_txt"]  = Label_(self.filterInputs["dateFrame"], _row=4, _col=0, text=_("Min. date (added)"), _pady=(2,0))
        self.filterInputs["dateAddedStart"]      = Entry_(self.filterInputs["dateFrame"], _row=5, _col=0)
        self.filterInputs["dateAddedStart_pick"] = LabelButton_(self.filterInputs["dateFrame"], _row=5, _col=2,
                                                                image=self.dateIcon,
                                                                command=lambda:self.datePicker.show(self.filterInputs["dateAddedStart"],
                                                                                                    self.filterInputs["dateAddedStart_pick"],
                                                                                                    self.filterInputs["dateAddedStart"].get(),
                                                                                                    "start"))

        self.filterInputs["dateAddedEnd_txt"]    = Label_(self.filterInputs["dateFrame"], _row=6, _col=0, text=_("Max. date (added)"), _pady=(2,0))
        self.filterInputs["dateAddedEnd"]        = Entry_(self.filterInputs["dateFrame"], _row=7, _col=0)
        self.filterInputs["dateAddedEnd_pick"]   = LabelButton_(self.filterInputs["dateFrame"], _row=7, _col=2,
                                                                image=self.dateIcon,
                                                                command=lambda:self.datePicker.show(self.filterInputs["dateAddedEnd"],
                                                                                                    self.filterInputs["dateAddedEnd_pick"],
                                                                                                    self.filterInputs["dateAddedEnd"].get(),
                                                                                                    "end"))


        self.filterInputs["group_frame"]     = Frame_(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["group_frame"].columnconfigure(0, minsize=240)

        self.filterInputs["group_txt"]       = Label_(self.filterInputs["group_frame"], _pady=(2,0), _row=0, _col=0, text=_("Group by"))
        self.filterInputs["group"]           = Combobox_(self.filterInputs["group_frame"], height=20, _row=1, _col=0, state="readonly")

        self.filterInputs["priceRange_txt"]  = Label_(self, text=_("Price range"), _pady=(2,0))


        self.filterInputs["column_frame"]    = Frame_(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.filterInputs["column_frame"].columnconfigure(0, minsize=111)
        self.filterInputs["column_frame"].columnconfigure(1, minsize=18)
        self.filterInputs["column_frame"].columnconfigure(2, minsize=111)

        self.filterInputs["priceStart"]     = Entry_(self.filterInputs["column_frame"], _row=0, _col=0)
        self.filterInputs["priceRange"]     = Label_(self.filterInputs["column_frame"], _row=0, _col=1, text="-", anchor="center")
        self.filterInputs["priceEnd"]       = Entry_(self.filterInputs["column_frame"], _row=0, _col=2)

        self.filterInputs["cart_txt"]       = Label_(self.filterInputs["column_frame"], _row=1, _col=0, text=_("Cart"), _pady=(2,0))
        self.filterInputs["box_txt"]        = Label_(self.filterInputs["column_frame"], _row=1, _col=2, text=_("Box"), _pady=(2,0))
        self.filterInputs["cart"]           = Combobox_(self.filterInputs["column_frame"], _row=2, _col=0, state="readonly")
        self.filterInputs["box"]            = Combobox_(self.filterInputs["column_frame"], _row=2, _col=2, state="readonly")

        self.filterInputs["manual_txt"]     = Label_(self.filterInputs["column_frame"], _row=3, _col=0, text=_("Manual"), _pady=(2,0))
        self.filterInputs["other_txt"]      = Label_(self.filterInputs["column_frame"], _row=3, _col=2, text=_("Other"), _pady=(2,0))
        self.filterInputs["manual"]         = Combobox_(self.filterInputs["column_frame"], _row=4, _col=0, state="readonly")
        self.filterInputs["other"]          = Combobox_(self.filterInputs["column_frame"], _row=4, _col=2, state="readonly")

        self.filterInputs["bookmarked_txt"] = Label_(self.filterInputs["column_frame"], _row=5, _col=0, text=_("Bookmarked"), _pady=(2,0))
        self.filterInputs["finished_txt"]   = Label_(self.filterInputs["column_frame"], _row=5, _col=2, text=_("Finished"), _pady=(2,0))
        self.filterInputs["bookmarked"]     = Combobox_(self.filterInputs["column_frame"], _row=6, _col=0, state="readonly")
        self.filterInputs["finished"]       = Combobox_(self.filterInputs["column_frame"], _row=6, _col=2, state="readonly")

        self.filterInputs["order_txt"]      = Label_(self.filterInputs["column_frame"], _row=7, _col=0, text=_("Sort by"), _pady=(2,0))
        self.filterInputs["order_dir_txt"]  = Label_(self.filterInputs["column_frame"], _row=7, _col=2, text=_("Sort direction"), _pady=(2,0))
        self.filterInputs["order"]          = Combobox_(self.filterInputs["column_frame"], _row=8, _col=0, state="readonly")
        self.filterInputs["orderDirection"] = Combobox_(self.filterInputs["column_frame"], _row=8, _col=2, state="readonly")

        self.filterInputs["filter_reset"]   = LabelButton_(self.filterInputs["column_frame"], _row=9, _col=0, _pady=(10,0), command=self.reset, style=VAR.LABELBUTTON_STYLE_CANCEL)
        self.filterInputs["filter_apply"]   = LabelButton_(self.filterInputs["column_frame"], _row=9, _col=2, _pady=(10,0), command=self.showData, style=VAR.LABELBUTTON_STYLE_CONFIRM)
        self.filterInputs["filter_reset"].config(text=_("Reset filter"), image=self.cancelIcon, compound="left")
        self.filterInputs["filter_apply"].config(text=_("Apply filter"), image=self.confirmIcon, compound="left")


        if settings.get("display", "refreshOnFilterSelect", True):
            self.bindComboboxes()

        self.fillYesNoComboboxes()
        self.fillOrderDirectionCombobox()

        # self.filter_button_frame = Frame_(self, style=VAR.FRAME_STYLE_SECONDARY)


        rowCount = 0

        for key in self.filterInputs:
            widget = self.filterInputs[key]

            col  = 0
            row  = rowCount
            padx = 0
            pady = 0

            if widget.__class__.__name__[-1] == "_":
                if not widget._col == None:
                    col = widget._col
                if not widget._row == None:
                    row = widget._row
                if not widget._padx == None:
                    padx = widget._padx
                if not widget._pady == None:
                    pady = widget._pady

            widget.grid(row=row, column=col, sticky="we", padx=padx, pady=pady)
            widget.bind("<Return>", self.showData)
            rowCount += 1

        # self.filter_button_frame.grid(row=rowCount, column=0, padx=0, pady=0, sticky="nw")


        # self.filter_reset.grid(row=0, column=0, sticky="nw", padx=(0,18), pady=(10, 5))

        # self.filter_apply.grid(row=0, column=1, sticky="nw", pady=(10, 5))


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
            if widget.__class__.__name__ == "LabelButton_":
                if widget._id == "select":
                    self.filterInputs[key].config(text=_("Select"))
                    self.filterInputs[key].setStyle(VAR.LABELBUTTON_STYLE_DEFAULT)
                if widget._toggle:
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
                    self.filterInputs[key + "_select"].config(text=str(len(value)) + _(" selected"))
                    self.filterInputs[key + "_select"].setStyle(VAR.LABELBUTTON_STYLE_TOGGLED)
                continue
            if key in self.filterInputs:
                widget = self.filterInputs[key]

                if widget.__class__.__name__ == "Entry_" or widget.__class__.__name__ == "Combobox_":
                    widget.set(value)

                if widget.__class__.__name__ == "LabelButton_":
                    if widget._toggle:
                        widget.setToggle(value)


    ######################
    # selectPlatforms
    # --------------------
    def selectPlatforms(self):
        self.platformSelect.show(sorted(self.collectionData.platforms_all.items()), self.multiFilter["platforms"], _("platforms"), focusWidget=self.filterInputs["platforms_select"])


    ######################
    # selectPlatformsCallback
    # --------------------
    def selectPlatformsCallback(self, platforms):
        self.multiFilter["platforms"] = platforms

        if len(platforms):
            self.filterInputs["platforms_select"].config(text=str(len(platforms)) + _(" selected"))
            self.filterInputs["platforms_select"].setStyle(VAR.LABELBUTTON_STYLE_TOGGLED)
        else:
            self.filterInputs["platforms_select"].config(text=_("Select"))
            self.filterInputs["platforms_select"].setStyle(VAR.LABELBUTTON_STYLE_DEFAULT)

        if settings.get("display", "refreshOnFilterSelect", True):
            self.showData()


    ######################
    # selectPlatformHolders
    # --------------------
    def selectPlatformHolders(self):
        self.platformHolderSelect.show(sorted(self.collectionData.platformHolders_all.items()), self.multiFilter["platformHolders"], _("platform holders"), focusWidget=self.filterInputs["platformHolders_select"])


    ######################
    # selectPlatformHoldersCallback
    # --------------------
    def selectPlatformHoldersCallback(self, platformHolders):
        self.multiFilter["platformHolders"] = platformHolders

        if len(platformHolders):
            self.filterInputs["platformHolders_select"].config(text=str(len(platformHolders)) + _(" selected"))
            self.filterInputs["platformHolders_select"].setStyle(VAR.LABELBUTTON_STYLE_TOGGLED)
        else:
            self.filterInputs["platformHolders_select"].config(text=_("Select"))
            self.filterInputs["platformHolders_select"].setStyle(VAR.LABELBUTTON_STYLE_DEFAULT)

        if settings.get("display", "refreshOnFilterSelect", True):
            self.showData()


    ######################
    # selectRegions
    # --------------------
    def selectRegions(self):
        self.regionSelect.show(sorted(self.collectionData.regions_all.items()), self.multiFilter["regions"], _("regions"), focusWidget=self.filterInputs["regions_select"])


    ######################
    # selectRegionsCallback
    # --------------------
    def selectRegionsCallback(self, regions):
        self.multiFilter["regions"] = regions

        if len(regions):
            self.filterInputs["regions_select"].config(text=str(len(regions)) + _(" selected"))
            self.filterInputs["regions_select"].setStyle(VAR.LABELBUTTON_STYLE_TOGGLED)
        else:
            self.filterInputs["regions_select"].config(text=_("Select"), style=VAR.LABELBUTTON_STYLE_DEFAULT)
            self.filterInputs["regions_select"].setStyle(VAR.LABELBUTTON_STYLE_DEFAULT)

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
