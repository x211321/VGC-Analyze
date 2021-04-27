import os

from tkinter import *
from tkinter import ttk

from VGC_Data     import CollectionData
from VGC_Data     import FilterData
from VGC_Lib      import YNToX
from VGC_Img      import loadIcon

from gui.VGC_GUI_ItemInfo       import GUI_ItemInfo
from gui.VGC_GUI_Filter         import initFilter
from gui.VGC_GUI_CollectionInfo import GUI_CollectionInfo
from gui.VGC_GUI_TreeView       import GUI_TreeView
from gui.VGC_GUI_Graph          import GUI_Graph
from gui.VGC_GUI_Menu           import initMainMenu
from gui.VGC_GUI_Hotkeys        import initHotkeys
from gui.VGC_GUI_Popups         import initPopups

from VGC_Var import LOCAL_DATA_FILE
from VGC_Var import DATA_PATH

from VGC_Var import GRAPH_TYPE_BAR
from VGC_Var import GRAPH_TYPE_PIE
from VGC_Var import GRAPH_TYPE_STACK
from VGC_Var import GRAPH_TYPE_LINE

from VGC_Lib import toggleYN

from VGC_Json import writeJson


class GUI(Tk):

    ######################
    # __init__
    # --------------------
    def __init__(self):

        super().__init__()


        # Data
        self.filterData     = FilterData()
        self.collectionData = CollectionData(self.filterData)
        self.index          = 0


        # Main window
        # ------------------
        # self = Tk()
        self.title('VGC Analyzer')
        self.geometry('1000x750')
        self.iconphoto(False, loadIcon("game-controller-outline", 15, 15))
        self.state('zoomed')
        self.protocol("WM_DELETE_WINDOW", self.onClose)


        # Frames
        # ------------------
        self.filter_frame = Frame(self, width=200 , height=550, pady=10, padx=10)
        self.view_frame   = GUI_TreeView(self, width=600 , height=550, pady=0 , padx=0)
        self.item_frame   = GUI_ItemInfo(self, width=200 , height=550, pady=0 , padx=0)
        self.graph_frame  = GUI_Graph(self, width=1000, height=200, pady=0 , padx=0)
        self.info_frame   = GUI_CollectionInfo(self, width=1000, height=200, pady=10, padx=10)


        self.filter_frame.grid(row=0, column=0, sticky="nws", rowspan=3)
        self.view_frame.grid(row=0, column=1, sticky="nwes")
        self.item_frame.grid(row=0, column=2, sticky="nes", rowspan=3)
        self.info_frame.grid(row=3, column=1, sticky="nwes")
        self.graph_frame.grid(row=2, column=1, sticky="nwes")
        self.graph_frame.grid_forget()


        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(1, weight=1)


        # Init
        self.init()


    ######################
    # init
    # --------------------
    def init(self):

        # Filter
        initFilter(self)

        # Hotkeys
        initHotkeys(self)

        # Popup dialogs
        initPopups(self)

        # Main menu
        initMainMenu(self)

    def onClose(self):
        self.collectionData.buildSaveData()
        writeJson(self.collectionData.localData_list, LOCAL_DATA_FILE)
        self.destroy()


    ######################
    # toggleGraphFrame
    # --------------------
    def toggleGraphFrame(self):
        if self.graph_frame.winfo_ismapped():
            self.graph_frame.grid_forget()
        else:
            self.graph_frame.grid(row=1, column=1, sticky="nwes")
            self.update()
            self.graph_frame.displayGraphs()


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
        self.mainloop()


    ######################
    # activeItem
    # --------------------
    def activeItem(self):
        return self.collectionData.collection_items[self.index]


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
        self.fillPlatformHolderCombobox()
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
            self.view_frame.item_view.column('#0', width=200, stretch="Yes")
        else:
            self.view_frame.item_view.column('#0', width=0, stretch="No")

        # Display totals
        self.info_frame.update(self)

        # Draw graphs
        if self.graph_frame.winfo_ismapped():
            self.graph_frame.displayGraphs()

        # Clear treeview
        self.view_frame.item_view.delete(*self.view_frame.item_view.get_children())

        # Show data
        tvIndex = 0

        if len(self.collectionData.getFilteredData()):

            if len(displayFilter.groupItems):
                # Group display

                # Show groups
                for group in sorted(self.collectionData.groups.keys()):

                    groupData = self.collectionData.groups[group]

                    self.view_frame.item_view.insert(parent="",
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
                for item in self.collectionData.getFilteredData():
                    self.insertViewItem(tvIndex, item, "")
                    tvIndex += 1

                self.view_frame.treeviewSort("Title", False)


    ######################
    # insertViewItem
    # --------------------
    def insertViewItem(self, index, item, parent = ""):
        self.view_frame.item_view.insert(parent= parent,
                              index = index,
                              iid   = item.index,
                              text  = "",
                              values=self.itemToViewValues(item))


    ######################
    # updateViewItem
    # --------------------
    def updateViewItem(self, index, item):
        self.view_frame.item_view.item(index, values=self.itemToViewValues(item))


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
                YNToX(item.getLocalData("finished")),
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


    ######################
    # selectViewItem
    # --------------------
    def selectViewItem(self, a = None):

        selection = self.view_frame.item_view.focus()

        # Item with text = Group item
        if not len(self.view_frame.item_view.item(selection)["text"]):
            if len(self.view_frame.item_view.item(selection)["values"]):
                self.index = self.view_frame.item_view.item(selection)["values"][0]

                if self.index >= 0:
                    # Update item info
                    self.item_frame.update()


    ######################
    # toggleBookmark
    # --------------------
    def toggleBookmark(self):
        selection = self.view_frame.item_view.focus()

        if len(self.activeItem().id()):
            self.activeItem().localData["bookmarked"] = toggleYN(self.activeItem().getLocalData("bookmarked"))

            self.updateViewItem(selection, self.activeItem())


    ######################
    # toggleFinished
    # --------------------
    def toggleFinished(self):
        selection = self.view_frame.item_view.focus()

        if len(self.activeItem().id()):
            self.activeItem().localData["finished"] = toggleYN(self.activeItem().getLocalData("finished"))

            self.updateViewItem(selection, self.activeItem())


    ######################
    # collectionDownload_callback
    # --------------------
    def collectionDownload_callback(self, result, newPath):
        self.filterData.filePath = newPath

        self.collectionData.setFilter(self.filterData)
        self.readData()
        self.showData()


    ######################
    # setCurrentVGCFile
    # --------------------
    def setCurrentVGCFile(self, event):
        self.collectionData.csv_file = DATA_PATH + self.view_frame.file_frame.item_select.get()
        self.readData()
        self.showData()