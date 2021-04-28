from VGC_Locale import _

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

        # Treeview definition
        self.item_view['columns']=('Index',
                                   'Title',
                                   'Platform',
                                   'Region',
                                   'Price',
                                   'Date',
                                   'Cart',
                                   'Box',
                                   'Manual',
                                   'Other',
                                   'Bookmark',
                                   'Finished',
                                   'Notes')

        # View columns
        self.item_view.column('#0'      , anchor="w", width=0, stretch="No")
        self.item_view.column('Index'   , anchor="w", width=0, stretch="No")
        self.item_view.column('Title'   , anchor="w", width=300)
        self.item_view.column('Platform', anchor="w", width=100)
        self.item_view.column('Region'  , anchor="w", width=5)
        self.item_view.column('Price'   , anchor="e", width=25)
        self.item_view.column('Date'    , anchor="w", width=10)
        self.item_view.column('Cart'    , anchor="w", width=5)
        self.item_view.column('Box'     , anchor="w", width=5)
        self.item_view.column('Manual'  , anchor="w", width=5)
        self.item_view.column('Other'   , anchor="w", width=5)
        self.item_view.column('Bookmark', anchor="w", width=5)
        self.item_view.column('Finished', anchor="w", width=5)
        self.item_view.column('Notes'   , anchor="w", width=100)

        # View column headers
        self.item_view.heading("#0"      , text=_("Group")   , anchor="w")
        self.item_view.heading("Index"   , text=_("")        , anchor="w")
        self.item_view.heading("Title"   , text=_("Title")   , anchor="w", command=lambda:self.treeviewSort("Title", False))
        self.item_view.heading("Platform", text=_("Platform"), anchor="w", command=lambda:self.treeviewSort("Platform", False))
        self.item_view.heading("Region"  , text=_("Region")  , anchor="w", command=lambda:self.treeviewSort("Region", False))
        self.item_view.heading("Price"   , text=_("Price")   , anchor="e", command=lambda:self.treeviewSort("Price", False, float))
        self.item_view.heading("Date"    , text=_("Date")    , anchor="w", command=lambda:self.treeviewSort("Date", False))
        self.item_view.heading("Cart"    , text=_("Cart")    , anchor="w", command=lambda:self.treeviewSort("Cart", False))
        self.item_view.heading("Box"     , text=_("Box")     , anchor="w", command=lambda:self.treeviewSort("Box", False))
        self.item_view.heading("Manual"  , text=_("Manual")  , anchor="w", command=lambda:self.treeviewSort("Manual", False))
        self.item_view.heading("Other"   , text=_("Other")   , anchor="w", command=lambda:self.treeviewSort("Other", False))
        self.item_view.heading("Bookmark", text=_("Bookmark"), anchor="w", command=lambda:self.treeviewSort("Bookmark", False))
        self.item_view.heading("Finished", text=_("Finished"), anchor="w", command=lambda:self.treeviewSort("Finished", False))
        self.item_view.heading("Notes"   , text=_("Notes")   , anchor="w", command=lambda:self.treeviewSort("Notes", False))

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

        self.treeviewSort("Title", False)


    def treeviewSort(self, column, reverse, datatype=None):

        if not self.item_view.lastSortItem == column:
            reverse = False


        itemList = [(self.item_view.set(row, column), row) for row in self.item_view.get_children('')]

        if datatype:
            itemList.sort(reverse=reverse, key=lambda tuple: datatype(tuple[0].lower().strip("abcdefghijklmnopqrstuvwxyz[]: ")))
        else:
            itemList.sort(reverse=reverse, key=lambda tuple: tuple[0].lower())

        # rearrange items in sorted positions
        for newRow, (val, item) in enumerate(itemList):
            self.item_view.move(item, '', newRow)

        # reverse sort next time
        self.item_view.lastSortItem = column
        self.item_view.heading(column, command=lambda:self.treeviewSort(column, not reverse, datatype))
