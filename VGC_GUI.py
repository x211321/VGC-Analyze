

import os
import threading

from tkinter import *
from tkinter import ttk
from datetime import datetime

from VGC_Widgets  import Label_
from VGC_Widgets  import Entry_
from VGC_Widgets  import Combobox_

from VGC_Data     import CollectionData
from VGC_Data     import CollectionItem
from VGC_Data     import FilterData
from VGC_Download import downloadCovers
from VGC_Browser  import openItemInBrowser
from VGC_Print    import YNToX
from VGC_Img      import loadCover
from VGC_Img      import loadIcon
from VGC_FilePath import writeFile
from VGC_FilePath import readFile

from VGC_GUI_Pop   import Pop_CoverViewer
from VGC_GUI_Pop   import Pop_CollectionDownload
from VGC_GUI_Pop   import Pop_ItemSearch
from VGC_GUI_Graph import drawBarGraph

from VGC_Var import IMG_CASHE_FRONT
from VGC_Var import IMG_CASHE_BACK
from VGC_Var import IMG_CASHE_CART
from VGC_Var import IMG_COVER_NONE
from VGC_Var import FILE_PREFIX
from VGC_Var import DOWNLOAD_FILE

COVER_WIDTH   = 120

class GUI(object):

    ######################
    # __init__
    # --------------------
    def __init__(self, filterData):
        # Main window
        # ------------------
        self.main_window = Tk()
        # main_window['bg'] = '#fb0'
        self.main_window.title('VGC Analyzer')
        self.main_window.geometry('1000x750')
        self.main_window.iconphoto(False, loadIcon("game-controller-outline", 15, 15))
        self.main_window.state('zoomed')

        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(1, weight=1)


        # Frames
        # ------------------
        self.filter_frame    = Frame(self.main_window, width=200 , height=550, pady=10, padx=10)
        self.view_frame      = Frame(self.main_window, width=600 , height=550, pady=0 , padx=0)
        self.item_frame      = Frame(self.main_window, width=200 , height=550, pady=0 , padx=0)
        self.graph_frame     = Frame(self.main_window, width=1000, height=200, pady=0 , padx=0)
        self.info_frame      = Frame(self.main_window, width=1000, height=200, pady=10, padx=10)


        self.filter_frame.grid(row=0, column=0, sticky="nws", rowspan=3)
        self.view_frame.grid(row=0, column=1, sticky="nwes")
        self.item_frame.grid(row=0, column=2, sticky="nes", rowspan=3)
        self.graph_frame.grid(row=1, column=1, sticky="nwes")
        self.info_frame.grid(row=2, column=1, sticky="nwes")


        # Treeview
        # ------------------
        self.item_view   = ttk.Treeview(self.view_frame)
        self.view_scroll = Scrollbar(self.view_frame)


        # Icons
        # ------------------
        self.item_refresh_ico  = loadIcon("refresh-outline", 15, 15)
        self.item_view_ico     = loadIcon("eye-outline", 15, 15)
        self.item_link_ico     = loadIcon("link-outline", 15, 15)
        self.item_bookmark_ico = loadIcon("bookmark-outline", 15, 15)
        self.item_graph_ico    = loadIcon("bar-chart-outline", 30, 30)


        # Item info
        # ------------------
        self.item_spacer    = Label(self.item_frame, width=2)

        self.item_title_txt = Label_(self.item_frame, text="Title", anchor="nw")
        self.item_title     = Label_(self.item_frame, anchor="nw", width=22, height=4, wraplength=135)
        self.item_date_txt  = Label_(self.item_frame, text="Purchase date", anchor="nw")
        self.item_date      = Label_(self.item_frame, anchor="nw", width=22)
        self.item_price_txt = Label_(self.item_frame, text="Purchase price", anchor="nw")
        self.item_price     = Label_(self.item_frame, anchor="nw", width=22)

        # Front cover widgets
        self.item_front_txt  = Label_(self.item_frame, text="Front cover", anchor="w")
        self.item_front      = Label_(self.item_frame, anchor="w", imgdef=IMG_COVER_NONE, imgwidth=COVER_WIDTH)
        self.item_front_upd  = Button(self.item_front.item)
        self.item_front_viw  = Button(self.item_front.item)

        # Back cover widgets
        self.item_back_txt   = Label_(self.item_frame, text="Back cover", anchor="w")
        self.item_back       = Label_(self.item_frame, anchor="w", imgdef=IMG_COVER_NONE, imgwidth=COVER_WIDTH)
        self.item_back_upd   = Button(self.item_back.item)
        self.item_back_viw   = Button(self.item_back.item)

        # Cart cover widgets
        self.item_cart_txt   = Label_(self.item_frame, text="Cart cover", anchor="w")
        self.item_cart       = Label_(self.item_frame, anchor="w", imgdef=IMG_COVER_NONE, imgwidth=COVER_WIDTH)
        self.item_cart_upd   = Button(self.item_cart.item)
        self.item_cart_viw   = Button(self.item_cart.item)


        # Filter inputs
        # ------------------
        self.filterInputs = {}

        self.filterInputs["name_txt"]       = Label_(self.filter_frame, width=25, text="Title")
        self.filterInputs["name"]           = Entry_(self.filter_frame, width=30)
        self.filterInputs["platform_txt"]   = Label_(self.filter_frame, width=25, text="Platform")
        self.filterInputs["platform"]       = Combobox_(self.filter_frame, width=27)
        self.filterInputs["region_txt"]     = Label_(self.filter_frame, width=25, text="Region")
        self.filterInputs["region"]         = Combobox_(self.filter_frame, width=27)
        self.filterInputs["notes_txt"]      = Label_(self.filter_frame, width=25, text="Notes")
        self.filterInputs["notes"]          = Entry_(self.filter_frame, width=30)
        self.filterInputs["dateStart_txt"]  = Label_(self.filter_frame, width=25, text="Min. date")
        self.filterInputs["dateStart"]      = Entry_(self.filter_frame, width=30)
        self.filterInputs["dateEnd_txt"]    = Label_(self.filter_frame, width=25, text="Max. date")
        self.filterInputs["dateEnd"]        = Entry_(self.filter_frame, width=30)
        self.filterInputs["priceStart_txt"] = Label_(self.filter_frame, width=25, text="Min. price")
        self.filterInputs["priceStart"]     = Entry_(self.filter_frame, width=30)
        self.filterInputs["priceEnd_txt"]   = Label_(self.filter_frame, width=25, text="Max. price")
        self.filterInputs["priceEnd"]       = Entry_(self.filter_frame, width=30)
        self.filterInputs["cart_txt"]       = Label_(self.filter_frame, width=10, text="Cart")
        self.filterInputs["box_txt"]        = Label_(self.filter_frame, width=10, text="Box")
        self.filterInputs["cart"]           = Combobox_(self.filter_frame, values=("", "Yes", "No"), state="readonly", width=10)
        self.filterInputs["box"]            = Combobox_(self.filter_frame, values=("", "Yes", "No"), state="readonly", width=10)
        self.filterInputs["manual_txt"]     = Label_(self.filter_frame, width=10, text="Manual")
        self.filterInputs["other_txt"]      = Label_(self.filter_frame, width=10, text="Other")
        self.filterInputs["manual"]         = Combobox_(self.filter_frame, values=("", "Yes", "No"), state="readonly", width=10)
        self.filterInputs["other"]          = Combobox_(self.filter_frame, values=("", "Yes", "No"), state="readonly", width=10)
        self.filterInputs["bookmarked_txt"] = Label_(self.filter_frame, text="Bookmarked", width=10)
        self.filterInputs["group_txt"]      = Label_(self.filter_frame, text="Group by", width=10)
        self.filterInputs["bookmarked"]     = Combobox_(self.filter_frame, values=("", "Yes", "No"), state="readonly", width=10)
        self.filterInputs["group"]          = Combobox_(self.filter_frame, state="readonly", width=10)
        self.filterInputs["order_txt"]      = Label_(self.filter_frame, text="Sort by", width=10)
        self.filterInputs["order_dir_txt"]  = Label_(self.filter_frame, text="Sort direction", width=10)
        self.filterInputs["order"]          = Combobox_(self.filter_frame, state="readonly", width=10)
        self.filterInputs["orderDirection"] = Combobox_(self.filter_frame, values=("", "ascending", "descending"), state="readonly", width=10)

        self.filter_apply = Button(self.filter_frame, width=10, relief="groove", bg="#BDF593")
        self.filter_reset = Button(self.filter_frame, width=10, relief="groove", bg="#F59398")


        # Graph
        # ------------------
        self.graph_canvas            = Canvas(self.graph_frame, bg="#FFF", highlightthickness=1, highlightbackground="black")


        # Data
        self.filterData = filterData
        self.collectionData        = CollectionData(self.filterData)
        self.activeItem            = CollectionItem()

        self.init()


    ######################
    # init
    # --------------------
    def init(self):

        # Popup dialogs
        # ------------------
        self.initPopups()

        # Main menu
        # ------------------
        self.initMainMenu()

        # Item treeview
        # ------------------
        self.initTreeView()

        # Item info
        # ------------------
        self.initItemInfo()

        # Filter
        # ------------------
        self.initFilter()

        # Collection info
        # ------------------
        self.initCollectionInfo()

        # Graph
        # ------------------
        self.initGraph()

        # Hotkeys
        # ------------------
        self.initHotkeys()


    ######################
    # onGraphResiz
    # --------------------
    def onGraphResiz(self, event):
        if self.graph_frame.winfo_ismapped:
            self.displayGraphs()


    ######################
    # initPopups
    # --------------------
    def initPopups(self):
        self.pop_coverViewer        = Pop_CoverViewer(self.main_window)
        self.pop_collectionDownload = Pop_CollectionDownload(self.main_window, self.collectionDownload_callback)
        self.pop_itemSearch         = Pop_ItemSearch(self.main_window, self.item_view)


    ######################
    # initMainMenu
    # --------------------
    def initMainMenu(self):
        self.main_menu = Menu(self.main_window)

        # File menu
        self.file_menu = Menu(self.main_menu, tearoff=0)
        self.file_menu.add_command(label="Quit", command=self.main_window.destroy, accelerator="Ctrl+Q")

        # Search menu
        self.search_menu = Menu(self.main_menu, tearoff=0)
        self.search_menu.add_command(label="Search for item", command=self.pop_itemSearch.show, accelerator="Ctrl+F")

        # Download menu
        self.download_menu = Menu(self.main_menu, tearoff=0)
        self.download_menu.add_command(label="Download collection", command=self.pop_collectionDownload.show, accelerator="Ctrl+D")

        # About menu
        self.about_menu = Menu(self.main_menu, tearoff=0)
        self.about_menu.add_command(label="About VGC Analyzer", command=self.showAbout)

        self.main_menu.add_cascade(label="File"    , menu=self.file_menu)
        self.main_menu.add_cascade(label="Search"  , menu=self.search_menu)
        self.main_menu.add_cascade(label="Download", menu=self.download_menu)
        self.main_menu.add_cascade(label="About"   , menu=self.about_menu)

        self.main_window.config(menu=self.main_menu)


    ######################
    # initTreeView
    # --------------------
    def initTreeView(self):
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
        self.item_view.column('Notes'   , anchor="w", width=100)

        # View column headers
        self.item_view.heading('#0'      , text='Group'   , anchor="w")
        self.item_view.heading('Index'   , text=''        , anchor="w")
        self.item_view.heading('Title'   , text='Title'   , anchor="w")
        self.item_view.heading('Platform', text='Platform', anchor="w")
        self.item_view.heading('Region'  , text='Region'  , anchor="w")
        self.item_view.heading('Price'   , text='Price'   , anchor="e")
        self.item_view.heading('Date'    , text='Date'    , anchor="w")
        self.item_view.heading('Cart'    , text='Cart'    , anchor="w")
        self.item_view.heading('Box'     , text='Box'     , anchor="w")
        self.item_view.heading('Manual'  , text='Manual'  , anchor="w")
        self.item_view.heading('Other'   , text='Other'   , anchor="w")
        self.item_view.heading('Bookmark', text='Bookmark', anchor="w")
        self.item_view.heading('Notes'   , text='Notes'   , anchor="w")

        # View events
        self.item_view.bind('<ButtonRelease-1>', self.selectViewItem)
        self.item_view.bind('<KeyRelease>', self.selectViewItem)

        # View scrollbar
        self.item_view.config(yscrollcommand=self.view_scroll.set)
        self.view_scroll.config(orient=VERTICAL, command=self.item_view.yview)

        # Position view and scrollbar
        self.view_scroll.pack(side=RIGHT, fill=Y)
        self.item_view.pack(expand=True, fill="both")


    ######################
    # initItemInfo
    # --------------------
    def initItemInfo(self):

        self.item_title_txt.item.grid(row=1, column=0, columnspan=2, sticky="nwe")
        self.item_spacer.grid(row=2, column=0, sticky="nwe")
        self.item_title.item.grid(row=2, column=1, sticky="nwe")

        self.item_date_txt.item.grid(row=3, column=0, columnspan=2, sticky="nwe")
        self.item_date.item.grid(row=4, column=1, sticky="nwe")

        self.item_price_txt.item.grid(row=5, column=0, columnspan=2, sticky="nwe")
        self.item_price.item.grid(row=6, column=1, sticky="nwe")

        self.item_front_txt.item.grid(row=7, column=0, columnspan=2, sticky="nwe")
        self.item_front.item.grid(row=8, column=1, sticky="nwe")

        self.item_back_txt.item.grid(row=9, column=0, columnspan=2, sticky="nwe")
        self.item_back.item.grid(row=10, column=1, sticky="nwe")

        self.item_cart_txt.item.grid(row=11, column=0, columnspan=2, sticky="nwe")
        self.item_cart.item.grid(row=12, column=1, sticky="nwe")

        # Frame for item toolbar
        self.item_tool_frame = Frame(self.item_frame , width=200 , height=10 , pady=0 , padx=0)
        self.item_tool_frame.grid(row=0, column=0, sticky="nwe", columnspan=2)

        # Item Toolbar
        self.item_open_website = Button(self.item_tool_frame, relief="groove", image=self.item_link_ico)
        self.item_bookmark     = Button(self.item_tool_frame, relief="groove", image=self.item_bookmark_ico)
        self.item_id           = Label_(self.item_tool_frame)
        self.item_id.item.grid(row=0, column=2, sticky="e")

        self.item_open_website.config(command=self.openOnVGCollect)
        self.item_open_website.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        self.item_bookmark.config(command=self.toggleBookmark)
        self.item_bookmark.grid(row=0, column=1, sticky="nw", padx=(5, 25), pady=5)

        # Position cover toolbars
        self.placeCoverToolbars()
        self.showCoverToolbars()


    ######################
    # initFilter
    # --------------------
    def initFilter(self):
        row = 0
        col = 0

        itemWidth        = 0
        colspan          = 0
        rowWidth         = 25
        rowWidth_current = 0

        for key in self.filterInputs:
            itemWidth = self.filterInputs[key].item['width']

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
                    self.filterInputs[key].item.grid(padx=(0, 18))

            self.filterInputs[key].item.grid(row=row, column=col, sticky="nw", columnspan=colspan)

            if (row) % 2 == 0:
                self.filterInputs[key].item.grid(pady=(0,5))

            self.filterInputs[key].item.bind('<Return>', self.showData)

        self.filter_reset.config(text="Reset filter", command=self.resetFilter)
        self.filter_reset.grid(row=100, column=0, sticky="nw", pady=(20, 5))

        self.filter_apply.config(text="Apply filter", command=self.showData)
        self.filter_apply.grid(row=100, column=1, sticky="nw", pady=(20, 5))


    ######################
    # initCollectionInfo
    # --------------------
    def initCollectionInfo(self):
        # Collection info
        # ------------------
        self.info_number_txt = Label_(self.info_frame, text="Item count:")
        self.info_number     = Label_(self.info_frame)

        self.info_value_txt  = Label_(self.info_frame, text="Total price:")
        self.info_value      = Label_(self.info_frame)

        self.info_average_txt= Label_(self.info_frame, text="Avg. price:")
        self.info_average    = Label_(self.info_frame)

        self.info_first_txt  = Label_(self.info_frame, text="First purchase:")
        self.info_first      = Label_(self.info_frame)

        self.info_last_txt   = Label_(self.info_frame, text="Last purchase:")
        self.info_last       = Label_(self.info_frame)

        self.info_update_txt = Label_(self.info_frame, text="Database updated:")
        self.info_update     = Label_(self.info_frame)

        self.info_grp_number_txt     = Label_(self.info_frame)
        self.info_grp_number         = Label_(self.info_frame)
        self.info_grp_number_spacer  = Label_(self.info_frame)

        self.info_grp_average_txt    = Label_(self.info_frame)
        self.info_grp_average        = Label_(self.info_frame)
        self.info_grp_average_spacer = Label_(self.info_frame)

        self.info_grp_priceHigh_txt  = Label_(self.info_frame)
        self.info_grp_priceHigh      = Label_(self.info_frame)
        self.info_grp_priceHigh_name = Label_(self.info_frame)

        self.info_grp_priceLow_txt   = Label_(self.info_frame)
        self.info_grp_priceLow       = Label_(self.info_frame)
        self.info_grp_priceLow_name  = Label_(self.info_frame)

        self.info_grp_countHigh_txt  = Label_(self.info_frame)
        self.info_grp_countHigh      = Label_(self.info_frame)
        self.info_grp_countHigh_name = Label_(self.info_frame)

        self.info_grp_countLow_txt   = Label_(self.info_frame)
        self.info_grp_countLow       = Label_(self.info_frame)
        self.info_grp_countLow_name  = Label_(self.info_frame)

        self.info_number_txt.item.grid(row=0, column=0, sticky="nw", pady=(0, 5))
        self.info_number.item.grid(row=0, column=1, sticky="ne", pady=(0, 5), padx=(0, 30))

        self.info_value_txt.item.grid(row=1, column=0, sticky="nw")
        self.info_value.item.grid(row=1, column=1, sticky="ne", pady=(0, 5), padx=(0, 30))

        self.info_average_txt.item.grid(row=2, column=0, sticky="nw")
        self.info_average.item.grid(row=2, column=1, sticky="ne", pady=(0, 5), padx=(0, 30))

        self.info_first_txt.item.grid(row=0, column=2, sticky="nw", pady=(0, 5), padx=(0, 30))
        self.info_first.item.grid(row=0, column=3, sticky="nw", pady=(0, 5), padx=(0, 30))

        self.info_last_txt.item.grid(row=1, column=2, sticky="nw", pady=(0, 5), padx=(0, 30))
        self.info_last.item.grid(row=1, column=3, sticky="nw", pady=(0, 5), padx=(0, 30))

        self.info_update_txt.item.grid(row=2, column=2, sticky="nw", pady=(0, 5), padx=(0, 30))
        self.info_update.item.grid(row=2, column=3, sticky="nw", pady=(0, 5), padx=(0, 30))


        self.info_grp_number_txt.item.grid(row=0, column=4, sticky="nw", pady=(0, 5))
        self.info_grp_number.item.grid(row=0, column=5, sticky="ne", pady=(0, 5))
        self.info_grp_number_spacer.item.grid(row=0, column=6, sticky="ne", pady=(0, 5), padx=(0, 30))

        self.info_grp_countLow_txt.item.grid(row=1, column=4, sticky="nw", pady=(0, 5))
        self.info_grp_countLow.item.grid(row=1, column=5, sticky="ne", pady=(0, 5))
        self.info_grp_countLow_name.item.grid(row=1, column=6, sticky="nw", pady=(0, 5), padx=(0, 30))

        self.info_grp_countHigh_txt.item.grid(row=2, column=4, sticky="nw", pady=(0, 5))
        self.info_grp_countHigh.item.grid(row=2, column=5, sticky="ne", pady=(0, 5))
        self.info_grp_countHigh_name.item.grid(row=2, column=6, sticky="nw", pady=(0, 5), padx=(0, 30))

        self.info_grp_average_txt.item.grid(row=0, column=7, sticky="nw")
        self.info_grp_average.item.grid(row=0, column=8, sticky="ne", pady=(0, 5))
        self.info_grp_average_spacer.item.grid(row=0, column=9, sticky="ne", pady=(0, 5))

        self.info_grp_priceLow_txt.item.grid(row=1, column=7, sticky="nw", pady=(0, 5))
        self.info_grp_priceLow.item.grid(row=1, column=8, sticky="ne", pady=(0, 5))
        self.info_grp_priceLow_name.item.grid(row=1, column=9, sticky="nw", pady=(0, 5))

        self.info_grp_priceHigh_txt.item.grid(row=2, column=7, sticky="nw", pady=(0, 5))
        self.info_grp_priceHigh.item.grid(row=2, column=8, sticky="ne", pady=(0, 5))
        self.info_grp_priceHigh_name.item.grid(row=2, column=9, sticky="nw", pady=(0, 5))

        # Grapf functions toolbar
        self.info_tool_frame = Frame(self.info_frame , width=200 , height=200, pady=0 , padx=0)
        self.info_tool_frame.grid(row=0, column=10, sticky="nes", rowspan=3)

        self.info_frame.grid_columnconfigure(10, weight=1)

        # Button to toggle the graph viewer
        self.info_toggle_graph = Button(self.info_tool_frame)
        self.info_toggle_graph.config(command=self.toggleGraphFrame, image=self.item_graph_ico, relief="groove")
        self.info_toggle_graph.grid(row=0, column=0)



    ######################
    # initGraph
    # --------------------
    def initGraph(self):
        self.graph_canvas.pack(expand=True, fill="both", padx=(0, 17), pady=(10,0))
        self.graph_canvas.bind("<Configure>", self.onGraphResiz)
        self.graph_frame.grid_forget()


    ######################
    # toggleGraphFrame
    # --------------------
    def toggleGraphFrame(self):
        if self.graph_frame.winfo_ismapped():
            self.graph_frame.grid_forget()
        else:
            self.graph_frame.grid(row=1, column=1, sticky="nwes")
            self.main_window.update()
            self.displayGraphs()


    ######################
    # initHotkeys
    # --------------------
    def initHotkeys(self):
        self.main_window.bind("<Control-f>", lambda x:self.pop_itemSearch.show())
        self.main_window.bind("<Control-d>", lambda x:self.pop_collectionDownload.show())
        self.main_window.bind("<Control-q>", lambda x:self.main_window.destroy())


    ######################
    # show
    # --------------------
    def show(self):
        # Read collection data
        self.readData()

        # Display collection data
        self.showData()

        # Show downloader when there is no data
        if len(self.collectionData.collection_items) == 0:
            self.pop_collectionDownload.show()

        # Run main loop
        self.main_window.mainloop()


    ######################
    # readData
    # --------------------
    def readData(self):

        # Read, parse and sum collection data
        #--------------------
        self.collectionData.readData()
        self.collectionData.parseData()
        self.collectionData.sumData()

        self.fillPlatformCombobox()
        self.fillRegionCombobox()
        self.fillGroupCombobox()
        self.fillOrderCombobox()


    ######################
    # showData
    # --------------------
    def showData(self, a = None):

        # Get user inputs
        displayFilter = self.getFilterInput()
        self.collectionData.setFilter(displayFilter)

        # Sum data acording to the user filter
        self.collectionData.sumData()

        # Show group column
        if len(displayFilter.groupItems):
            self.collectionData.groupData()
            self.item_view.column('#0', width=200, stretch="Yes")
        else:
            self.item_view.column('#0', width=0, stretch="No")

        # Display totals
        self.displayCollectionInfo()

        # Draw graphs
        if self.graph_frame.winfo_ismapped():
            self.displayGraphs()

        # Clear treeview
        self.item_view.delete(*self.item_view.get_children())

        # Show data
        tvIndex = 0

        if len(self.collectionData.getFilteredData()):

            if len(displayFilter.groupItems):
                # Group display

                # Show groups
                for group in sorted(self.collectionData.groups.keys()):

                    groupData = self.collectionData.groups[group]

                    self.item_view.insert(parent="",
                                          index = tvIndex,
                                          iid   = "#"+group,
                                          text  = group,
                                          values=("",
                                                  "[" + str(groupData.item_count) + " items]",
                                                  "",
                                                  "",
                                                  "[total price: " + "{:.2f}".format(groupData.total_price) + "]"))

                    tvIndex += 1

                # Add items to groups
                for group in sorted(self.collectionData.groups.keys()):
                    for item in self.sortViewItems(displayFilter, self.collectionData.groups[group].items):
                        self.insertViewItem(tvIndex, item, "#"+group)

                        tvIndex += 1

            else:
                # Normal display
                for item in self.sortViewItems(displayFilter, self.collectionData.getFilteredData()):
                    self.insertViewItem(tvIndex, item, "")
                    tvIndex += 1


    ######################
    # insertViewItem
    # --------------------
    def insertViewItem(self, index, item, parent = ""):
        self.item_view.insert(parent= parent,
                              index = index,
                              iid   = item.index,
                              text  = "",
                              values=self.itemToViewValues(item))


    ######################
    # updateViewItem
    # --------------------
    def updateViewItem(self, index, item):
        self.item_view.item(index, values=self.itemToViewValues(item))


    ######################
    # itemToViewValues
    # --------------------
    def itemToViewValues(self, item):
        return (item.index,
                item.name,
                item.platform,
                item.region,
                "{:.2f}".format(item.price),
                item.date,
                YNToX(item.cart),
                YNToX(item.box),
                YNToX(item.manual),
                YNToX(item.other),
                YNToX(item.getLocalData("bookmarked")),
                item.notes)


    ######################
    # sortViewItems
    # --------------------
    def sortViewItems(self, filterData, items):
        if len(filterData.orderItems) or filterData.orderItemsReverse:
            if filterData.orderItems.lower() == "name" or len(filterData.orderItems) == 0:
                return sorted(items, key=lambda item: item.name, reverse=filterData.orderItemsReverse)
            if filterData.orderItems.lower() == "price":
                return sorted(items, key=lambda item: item.price, reverse=filterData.orderItemsReverse)
            if filterData.orderItems.lower() == "date" :
                return sorted(items, key=lambda item: item.date, reverse=filterData.orderItemsReverse)
            if filterData.orderItems.lower() == "region" :
                return sorted(items, key=lambda item: item.region, reverse=filterData.orderItemsReverse)
            if filterData.orderItems.lower() == "platform" :
                return sorted(items, key=lambda item: item.platform, reverse=filterData.orderItemsReverse)
            if filterData.orderItems.lower() == "notes" :
                return sorted(items, key=lambda item: item.notes, reverse=filterData.orderItemsReverse)
        else:
            return items


    ######################
    # getFilterInput
    # --------------------
    def getFilterInput(self):
        filterInput = self.filterData
        filterInput.inputsToFilter(self.filterInputs)

        return filterInput


    ######################
    # resetFilter
    # --------------------
    def resetFilter(self):
        for key in self.filterInputs:
            if self.filterInputs[key].item.__class__.__name__ == "Entry":
                self.filterInputs[key].delete(0, END)
            if self.filterInputs[key].item.__class__.__name__ == "Combobox":
                self.filterInputs[key].set("")

        self.showData()


    ######################
    # openOnVGCollect
    # --------------------
    def openOnVGCollect(self):
        if self.activeItem.VGC_id > 0:
            openItemInBrowser(str(self.activeItem.VGC_id))


    ######################
    # toggleBookmark
    # --------------------
    def toggleBookmark(self):
        selection = self.item_view.focus()

        if len(self.activeItem.id()):
            self.updateViewItem(selection, self.activeItem)

            # Anzeigedaten aktualisieren
            self.collectionData.updateItem(self.activeItem)


    ######################
    # showAbout
    # --------------------
    def showAbout(self):
        print()


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


    ######################
    # selectViewItem
    # --------------------
    def selectViewItem(self, a = None):
        selection = self.item_view.focus()
        if len(self.item_view.item(selection)["values"]):
            index = str(self.item_view.item(selection)["values"][0])

            if len(index) and index == str(int(index)):
                self.activeItem = self.collectionData.collection_items[int(index)]

                thread = threading.Thread(target=self.selectViewItemThread, args=(self.activeItem,))
                thread.start()


    ######################
    # selectViewItemThread
    # --------------------
    def selectViewItemThread(self, item):
        self.item_title.set(item.name)
        self.item_date.set(item.date)
        self.item_price.set("{:.2f}".format(item.price))
        self.item_id.set("VGC ID: " + str(item.VGC_id))

        # display covers
        self.showCovers(item)

        # download covers
        downloadCovers(item.VGC_id)

        # display covers
        if item.VGC_id == self.activeItem.VGC_id:
            self.showCovers(item)


    ######################
    # displayCollectionInfo
    # --------------------
    def displayCollectionInfo(self):
        self.info_number.set(self.collectionData.totals.item_count)
        self.info_value.set("{:.2f}".format(self.collectionData.totals.total_price))
        if self.collectionData.totals.item_count:
            self.info_average.set("{:.2f}".format(self.collectionData.totals.total_price/self.collectionData.totals.item_count))
        else:
            self.info_average.set("{:.2f}".format(0))
        self.info_first.set(self.collectionData.totals.first.date + "  -  " +
                            self.collectionData.totals.first.name)
        self.info_last.set(self.collectionData.totals.last.date + "  -  " +
                            self.collectionData.totals.last.name)

        if os.path.exists(self.collectionData.csv_file):
            self.info_update.set(str(datetime.fromtimestamp(os.path.getmtime(self.collectionData.csv_file))).split(".")[0])

        if self.collectionData.filterData.groupItems:
            self.info_grp_number_txt.set("Group count:")
            self.info_grp_number.set(str(len(self.collectionData.groups)))

            self.info_grp_average_txt.set("Avg. group price:")
            self.info_grp_average.set("{:.2f}".format(self.collectionData.totals.total_price/len(self.collectionData.groups)))

            self.info_grp_priceLow_txt.set("Lowest group price:")
            self.info_grp_priceLow.set("{:.2f}".format(self.collectionData.getGroupPriceLow().total_price))
            self.info_grp_priceLow_name.set(" -  " + self.collectionData.groupKey_priceLow)

            self.info_grp_priceHigh_txt.set("Highest group price:")
            self.info_grp_priceHigh.set("{:.2f}".format(self.collectionData.getGroupPriceHigh().total_price))
            self.info_grp_priceHigh_name.set(" -  " + self.collectionData.groupKey_priceHigh)

            self.info_grp_countLow_txt.set("Least group items:")
            self.info_grp_countLow.set(self.collectionData.getGroupCountLow().item_count)
            self.info_grp_countLow_name.set(" -  " + self.collectionData.groupKey_countLow)

            self.info_grp_countHigh_txt.set("Most group items:")
            self.info_grp_countHigh.set(self.collectionData.getGroupCountHigh().item_count)
            self.info_grp_countHigh_name.set(" -  " + self.collectionData.groupKey_countHigh)
        else:
            self.info_grp_number_txt.set("")
            self.info_grp_number.set("")

            self.info_grp_average_txt.set("")
            self.info_grp_average.set("")

            self.info_grp_priceLow_txt.set("")
            self.info_grp_priceLow.set("")
            self.info_grp_priceLow_name.set("")

            self.info_grp_priceHigh_txt.set("")
            self.info_grp_priceHigh.set("")
            self.info_grp_priceHigh_name.set("")

            self.info_grp_countLow_txt.set("")
            self.info_grp_countLow.set("")
            self.info_grp_countLow_name.set("")

            self.info_grp_countHigh_txt.set("")
            self.info_grp_countHigh.set("")
            self.info_grp_countHigh_name.set("")


    ######################
    # displayGraphs
    # --------------------
    def displayGraphs(self):
        self.collectionData.groupGraphData("year")
        drawBarGraph(self.collectionData, self.graph_canvas, "price")


    ######################
    # showCovers
    # --------------------
    def showCovers(self, item):
        self.item_front.setImage(IMG_CASHE_FRONT + str(item.VGC_id) + ".jpg")
        self.item_back.setImage(IMG_CASHE_BACK + str(item.VGC_id) + ".jpg")
        self.item_cart.setImage(IMG_CASHE_CART + str(item.VGC_id) + ".jpg")

        self.showCoverToolbars(item)


    ######################
    # placeCoverToolbars
    # --------------------
    def placeCoverToolbars(self):
        # Front Cover
        self.item_front_upd.place(height=25, width=25, x=2, y=2)
        self.item_front_viw.place(height=25, width=25, x=29, y=2)

        # Back Cover
        self.item_back_upd.place(height=25, width=25, x=2, y=2)
        self.item_back_viw.place(height=25, width=25, x=29, y=2)

        # Cart Cover
        self.item_cart_upd.place(height=25, width=25, x=2, y=2)
        self.item_cart_viw.place(height=25, width=25, x=29, y=2)


    ######################
    # showCoverToolbars
    # --------------------
    def showCoverToolbars(self, item = None):
        # Front Cover
        self.item_front_upd.config(bg="white", image=self.item_refresh_ico, relief="groove", command=lambda:self.updateCover("front", item))
        self.item_front_viw.config(bg="white", image=self.item_view_ico, relief="groove", command=lambda:self.pop_coverViewer.show("front", item))

        #Back Cover
        self.item_back_upd.config(bg="white", image=self.item_refresh_ico, relief="groove", command=lambda:self.updateCover("back", item))
        self.item_back_viw.config(bg="white", image=self.item_view_ico, relief="groove", command=lambda:self.pop_coverViewer.show("back", item))

        #Cart Cover
        self.item_cart_upd.config(bg="white", image=self.item_refresh_ico, relief="groove", command=lambda:self.updateCover("cart", item))
        self.item_cart_viw.config(bg="white", image=self.item_view_ico, relief="groove", command=lambda:self.pop_coverViewer.show("cart", item))


    ######################
    # updateCover
    # --------------------
    def updateCover(self, coverType, item = None):
        if not item == None:
            downloadCovers(item.VGC_id, True, coverType)
            self.showCovers(item)


    ######################
    # collectionDownload_callback
    # --------------------
    def collectionDownload_callback(self, result, newPath):
        self.filterData.filePath = newPath

        self.collectionData.setFilter(self.filterData)
        self.readData()
        self.showData()
