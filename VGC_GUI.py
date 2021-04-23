import os
import threading

from tkinter import *
from tkinter import ttk

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


from gui.VGC_GUI_ItemInfo       import initItemInfo
from gui.VGC_GUI_Filter         import initFilter
from gui.VGC_GUI_CollectionInfo import initCollectionInfo
from gui.VGC_GUI_CollectionInfo import displayCollectionInfo
from gui.VGC_GUI_Treeview       import initTreeView
from gui.VGC_GUI_Graph          import initGraph
from gui.VGC_GUI_Graph          import drawBarGraph
from gui.VGC_GUI_Menu           import initMainMenu
from gui.VGC_GUI_Hotkeys        import initHotkeys
from gui.VGC_GUI_Popups         import initPopups
from gui.VGC_GUI_Popups         import Pop_CoverViewer
from gui.VGC_GUI_Popups         import Pop_CollectionDownload
from gui.VGC_GUI_Popups         import Pop_ItemSearch

from VGC_Var import IMG_CASHE_FRONT
from VGC_Var import IMG_CASHE_BACK
from VGC_Var import IMG_CASHE_CART
from VGC_Var import IMG_COVER_NONE
from VGC_Var import FILE_PREFIX
from VGC_Var import DOWNLOAD_FILE


class GUI(object):

    ######################
    # __init__
    # --------------------
    def __init__(self, filterData):
        # Main window
        # ------------------
        self.main_window = Tk()
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


        # Icons
        # ------------------
        self.item_refresh_ico  = loadIcon("refresh-outline", 15, 15)
        self.item_view_ico     = loadIcon("eye-outline", 15, 15)
        self.item_link_ico     = loadIcon("link-outline", 15, 15)
        self.item_bookmark_ico = loadIcon("bookmark-outline", 15, 15)
        self.item_graph_ico    = loadIcon("bar-chart-outline", 30, 30)


        # Data
        self.filterData = filterData
        self.collectionData        = CollectionData(self.filterData)
        self.activeItem            = CollectionItem()

        self.init()


    ######################
    # init
    # --------------------
    def init(self):

        # Item treeview
        initTreeView(self)

        # Item info
        initItemInfo(self)

        # Filter
        initFilter(self)

        # Collection info
        initCollectionInfo(self)

        # Graph
        initGraph(self)

        # Hotkeys
        initHotkeys(self)

        # Popup dialogs
        initPopups(self)

        # Main menu
        initMainMenu(self)


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
        displayCollectionInfo(self)

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
