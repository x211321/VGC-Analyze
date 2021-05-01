from VGC_Locale import _
from VGC_Locale import locCurrencySymbol
from VGC_Locale import locStrToNum

import VGC_Var as VAR

from tkinter import *
from tkinter import ttk

from gui.VGC_GUI_Fileselect import GUI_File

######################
# GUI_TreeView
# --------------------
class GUI_TreeView(Frame):

    def __init__(self, master, width=0, height=0, pady=0, padx=0):
        super().__init__(master=master, width=width, height=height, pady=pady, padx=padx)

        self.selectViewItem    = master.selectViewItem
        self.setCurrentVGCFile = master.setCurrentVGCFile
        self.collectionData    = master.collectionData

        self.init()


    def init(self):
        # Treeview
        # ------------------
        self.item_view               = ttk.Treeview(self)
        self.view_scroll_vertical    = Scrollbar(self)
        self.view_scroll_horizontal  = Scrollbar(self)
        self.item_view.lastSortItem  = ""

        # Define columns
        columns = ("Index", )

        for column in VAR.VIEW_COLUMNS:
            columns += (column, )

        self.item_view["columns"] = columns

        # Configure columns
        self.item_view.column("#0"   , anchor="w", width=0, stretch="No")
        self.item_view.column("Index", anchor="w", width=0, stretch="No")

        self.item_view.heading("#0"   , text=_("Group"), anchor="w")
        self.item_view.heading("Index", text=""        , anchor="w")

        for column in VAR.VIEW_COLUMNS:
            colData = VAR.VIEW_COLUMNS[column]
            self.item_view.column(colData["name"], anchor=colData["anchor"], width=colData["width"])
            self.item_view.heading(colData["name"], text=colData["name"],
                                                    anchor=colData["anchor"],
                                                    command=lambda colData=colData:self.treeviewSort(colData["name"], False, colData["type"]))

        # View events
        self.item_view.bind('<<TreeviewSelect>>', self.selectViewItem)

        # View scrollbar
        self.item_view.config(yscrollcommand=self.view_scroll_vertical.set)
        self.view_scroll_vertical.config(orient=VERTICAL, command=self.item_view.yview)

        self.item_view.config(xscrollcommand=self.view_scroll_horizontal.set)
        self.view_scroll_horizontal.config(orient=HORIZONTAL, command=self.item_view.xview)

        self.file_frame = GUI_File(self, width=1000, height=100, pady=10, padx=0)
        self.file_frame.pack(side=TOP, fill=X)

        # Position view and scrollbar
        self.view_scroll_vertical.pack(side=RIGHT, fill=Y)
        self.item_view.pack(expand=True, fill="both")
        self.view_scroll_horizontal.pack(side=BOTTOM, fill=X)

        self.treeviewSort(list(VAR.VIEW_COLUMNS.values())[0]["name"], False)


    def treeviewSort(self, column, reverse, datatype=None):
        if not self.item_view.lastSortItem == column:
            reverse = False


        itemList = [(self.item_view.set(row, column), row) for row in self.item_view.get_children('')]

        if datatype:
            itemList.sort(reverse=reverse, key=lambda tuple: datatype(locStrToNum(tuple[0].lower().strip("abcdefghijklmnopqrstuvwxyz[]: "+locCurrencySymbol()))))
        else:
            itemList.sort(reverse=reverse, key=lambda tuple: tuple[0].lower())

        # rearrange items in sorted positions
        for newRow, (val, item) in enumerate(itemList):
            self.item_view.move(item, '', newRow)

        # reverse sort next time
        self.item_view.lastSortItem = column
        self.item_view.heading(column, command=lambda:self.treeviewSort(column, not reverse, datatype))
