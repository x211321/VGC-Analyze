from tkinter import *
from tkinter import ttk


######################
# initTreeView
# --------------------
def initTreeView(gui):
    # Treeview
    # ------------------
    gui.item_view               = ttk.Treeview(gui.view_frame)
    gui.view_scroll_vertical    = Scrollbar(gui.view_frame)
    gui.view_scroll_horizontal  = Scrollbar(gui.view_frame)
    gui.item_view.lastSortItem  = ""

    # Treeview definition
    gui.item_view['columns']=('Index',
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
    gui.item_view.column('#0'      , anchor="w", width=0, stretch="No")
    gui.item_view.column('Index'   , anchor="w", width=0, stretch="No")
    gui.item_view.column('Title'   , anchor="w", width=300)
    gui.item_view.column('Platform', anchor="w", width=100)
    gui.item_view.column('Region'  , anchor="w", width=5)
    gui.item_view.column('Price'   , anchor="e", width=25)
    gui.item_view.column('Date'    , anchor="w", width=10)
    gui.item_view.column('Cart'    , anchor="w", width=5)
    gui.item_view.column('Box'     , anchor="w", width=5)
    gui.item_view.column('Manual'  , anchor="w", width=5)
    gui.item_view.column('Other'   , anchor="w", width=5)
    gui.item_view.column('Bookmark', anchor="w", width=5)
    gui.item_view.column('Finished', anchor="w", width=5)
    gui.item_view.column('Notes'   , anchor="w", width=100)

    # View column headers
    gui.item_view.heading('#0'      , text='Group'   , anchor="w")
    gui.item_view.heading('Index'   , text=''        , anchor="w")
    gui.item_view.heading('Title'   , text='Title'   , anchor="w", command=lambda:treeviewSort(gui.item_view, 'Title', False))
    gui.item_view.heading('Platform', text='Platform', anchor="w", command=lambda:treeviewSort(gui.item_view, 'Platform', False))
    gui.item_view.heading('Region'  , text='Region'  , anchor="w", command=lambda:treeviewSort(gui.item_view, 'Region', False))
    gui.item_view.heading('Price'   , text='Price'   , anchor="e", command=lambda:treeviewSort(gui.item_view, 'Price', False))
    gui.item_view.heading('Date'    , text='Date'    , anchor="w", command=lambda:treeviewSort(gui.item_view, 'Date', False))
    gui.item_view.heading('Cart'    , text='Cart'    , anchor="w", command=lambda:treeviewSort(gui.item_view, 'Cart', False))
    gui.item_view.heading('Box'     , text='Box'     , anchor="w", command=lambda:treeviewSort(gui.item_view, 'Box', False))
    gui.item_view.heading('Manual'  , text='Manual'  , anchor="w", command=lambda:treeviewSort(gui.item_view, 'Manual', False))
    gui.item_view.heading('Other'   , text='Other'   , anchor="w", command=lambda:treeviewSort(gui.item_view, 'Other', False))
    gui.item_view.heading('Bookmark', text='Bookmark', anchor="w", command=lambda:treeviewSort(gui.item_view, 'Bookmark', False))
    gui.item_view.heading('Finished', text='Finished', anchor="w", command=lambda:treeviewSort(gui.item_view, 'Finished', False))
    gui.item_view.heading('Notes'   , text='Notes'   , anchor="w", command=lambda:treeviewSort(gui.item_view, 'Notes', False))

    # View events
    gui.item_view.bind('<<TreeviewSelect>>', gui.selectViewItem)

    # View scrollbar
    gui.item_view.config(yscrollcommand=gui.view_scroll_vertical.set)
    gui.view_scroll_vertical.config(orient=VERTICAL, command=gui.item_view.yview)

    gui.item_view.config(xscrollcommand=gui.view_scroll_horizontal.set)
    gui.view_scroll_horizontal.config(orient=HORIZONTAL, command=gui.item_view.xview)

    # Position view and scrollbar
    gui.view_scroll_vertical.pack(side=RIGHT, fill=Y)
    gui.item_view.pack(expand=True, fill="both")
    gui.view_scroll_horizontal.pack(side=BOTTOM, fill=X)

    treeviewSort(gui.item_view, "Title", False)


def treeviewSort(treeView, column, reverse):

    if not treeView.lastSortItem == column:
        reverse = False

    itemList = [(treeView.set(row, column), row) for row in treeView.get_children('')]
    itemList.sort(reverse=reverse)

    # rearrange items in sorted positions
    for newRow, (val, item) in enumerate(itemList):
        treeView.move(item, '', newRow)

    # reverse sort next time
    treeView.lastSortItem = column
    treeView.heading(column, command=lambda:treeviewSort(treeView, column, not reverse))
