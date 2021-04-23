from tkinter import *
from tkinter import ttk


######################
# initTreeView
# --------------------
def initTreeView(gui):
    # Treeview
    # ------------------
    gui.item_view   = ttk.Treeview(gui.view_frame)
    gui.view_scroll = Scrollbar(gui.view_frame)

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
    gui.item_view.column('Notes'   , anchor="w", width=100)

    # View column headers
    gui.item_view.heading('#0'      , text='Group'   , anchor="w")
    gui.item_view.heading('Index'   , text=''        , anchor="w")
    gui.item_view.heading('Title'   , text='Title'   , anchor="w")
    gui.item_view.heading('Platform', text='Platform', anchor="w")
    gui.item_view.heading('Region'  , text='Region'  , anchor="w")
    gui.item_view.heading('Price'   , text='Price'   , anchor="e")
    gui.item_view.heading('Date'    , text='Date'    , anchor="w")
    gui.item_view.heading('Cart'    , text='Cart'    , anchor="w")
    gui.item_view.heading('Box'     , text='Box'     , anchor="w")
    gui.item_view.heading('Manual'  , text='Manual'  , anchor="w")
    gui.item_view.heading('Other'   , text='Other'   , anchor="w")
    gui.item_view.heading('Bookmark', text='Bookmark', anchor="w")
    gui.item_view.heading('Notes'   , text='Notes'   , anchor="w")

    # View events
    gui.item_view.bind('<ButtonRelease-1>', gui.selectViewItem)
    gui.item_view.bind('<KeyRelease>', gui.selectViewItem)

    # View scrollbar
    gui.item_view.config(yscrollcommand=gui.view_scroll.set)
    gui.view_scroll.config(orient=VERTICAL, command=gui.item_view.yview)

    # Position view and scrollbar
    gui.view_scroll.pack(side=RIGHT, fill=Y)
    gui.item_view.pack(expand=True, fill="both")