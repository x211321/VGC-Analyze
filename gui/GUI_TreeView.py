import lib.Settings as settings

from lib.Locale import _
from lib.Locale import locCurrencySymbol
from lib.Locale import locStrToNum

import lib.Var as VAR

from tkinter import *
from tkinter import ttk

from gui.GUI_Fileselect import GUI_File

######################
# GUI_TreeView
# --------------------
class GUI_TreeView(ttk.Frame):

    def __init__(self, master, width=0, height=0):
        super().__init__(master=master, width=width, height=height, style=VAR.FRAME_STYLE_SECONDARY)

        self.selectViewItem      = master.selectViewItem
        self.setCurrentVGCFile   = master.setCurrentVGCFile
        self.collectionData      = master.collectionData
        self.showViewContextMenu = master.showViewContextMenu
        self.showItemDetails     = master.showItemDetails

        self.init()


    def init(self):
        # Treeview
        # ------------------
        self.item_view               = ttk.Treeview(self)
        self.view_scroll_vertical    = Scrollbar(self)
        self.view_scroll_horizontal  = Scrollbar(self)
        self.item_view.lastSortItem  = ""

        # Define columns
        columns = ("Index", "VGCID", )

        for column in VAR.VIEW_COLUMNS:
            columns += (column, )

        self.item_view["columns"] = columns

        # Configure columns
        self.item_view.column("#0"   , anchor="w", width=0, stretch="No")
        self.item_view.column("Index", anchor="w", width=0, stretch="No")
        self.item_view.column("VGCID", anchor="w", width=0, stretch="No")

        self.item_view.heading("#0"   , text=_("Group"), anchor="w")
        self.item_view.heading("Index", text=""        , anchor="w")
        self.item_view.heading("VGCID", text=""        , anchor="w")

        for column in VAR.VIEW_COLUMNS:
            self.item_view.column(column, anchor=VAR.VIEW_COLUMNS[column]["anchor"], width=VAR.VIEW_COLUMNS[column]["width"])
            self.item_view.heading(column, text=VAR.VIEW_COLUMNS[column]["name"], anchor=VAR.VIEW_COLUMNS[column]["anchor"],
                                   command=lambda column=column:self.treeviewSort(column, False, VAR.VIEW_COLUMNS[column]["type"], VAR.VIEW_COLUMNS[column]["grouptype"]))

        # View events
        self.item_view.bind('<<TreeviewSelect>>', self.selectViewItem)
        self.item_view.bind("<Button-3>", self.showViewContextMenu)
        self.item_view.bind("<Double-1>", self.showItemDetails)

        # View scrollbar
        self.item_view.config(yscrollcommand=self.view_scroll_vertical.set)
        self.view_scroll_vertical.config(orient=VERTICAL, command=self.item_view.yview)

        self.item_view.config(xscrollcommand=self.view_scroll_horizontal.set)
        self.view_scroll_horizontal.config(orient=HORIZONTAL, command=self.item_view.xview)

        self.file_frame = GUI_File(self, width=1000, height=100)
        self.file_frame.pack(side=TOP, fill=X, pady=10, padx=0)

        # Position view and scrollbar
        self.view_scroll_vertical.pack(side=RIGHT, fill=Y)
        self.item_view.pack(expand=True, fill="both")
        self.view_scroll_horizontal.pack(side=BOTTOM, fill=X)

        column = list(VAR.VIEW_COLUMNS.keys())[0]
        self.treeviewSort(column, False, VAR.VIEW_COLUMNS[column]["type"], VAR.VIEW_COLUMNS[column]["grouptype"])

        self.setColumnDisplay()


    def treeviewSort(self, column, reverse, datatype=None, groupdatatype=None):
        if not self.item_view.lastSortItem == column:
            reverse = False

        groupMode = False

        try:
            if(self.item_view.get_children()[0][0]) == "#":
                groupMode = True
        except:
            groupMode = False

        itemList = [(self.item_view.set(row, column), row) for row in self.item_view.get_children('')]

        if groupMode and groupdatatype:
            itemList.sort(reverse=reverse, key=lambda tuple: groupdatatype(locStrToNum("".join(char for char in tuple[0].lower() if char in ",.1234567890"))))
        elif datatype:
            itemList.sort(reverse=reverse, key=lambda tuple: datatype(locStrToNum("".join(char for char in tuple[0].lower() if char in ",.1234567890"))))
        else:
            itemList.sort(reverse=reverse, key=lambda tuple: tuple[0].lower())

        # rearrange items in sorted positions
        for newRow, (val, item) in enumerate(itemList):
            self.item_view.move(item, '', newRow)

        # reverse sort next time
        self.item_view.lastSortItem = column
        self.item_view.heading(column, command=lambda:self.treeviewSort(column, not reverse, datatype, groupdatatype))


    def setColumnDisplay(self, resize=False):
        columns = settings.get("display", "columns", [])
        displayColumns = ()

        if len(columns):
            for column in columns:
                if len(column.strip()):
                    displayColumns += (column, )

        if not len(displayColumns):
            displayColumns = "#all"

        if not self.item_view["displaycolumns"] == displayColumns:
            self.item_view["displaycolumns"] = displayColumns

            if resize:
                viewWidth   = self.item_view.winfo_reqwidth()
                columnCount = 0

                for column in VAR.VIEW_COLUMNS:
                    if column in displayColumns or len(displayColumns) == 0:
                        columnCount += 1

                for column in VAR.VIEW_COLUMNS:
                    if column in displayColumns or len(displayColumns) == 0:
                        self.item_view.column(column, width=int(viewWidth/columnCount), stretch="Yes")