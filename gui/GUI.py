import lib.Settings as settings
from lib.Locale import _
from lib.Locale import locCurrency
from lib.Locale import locDate

import os
import platform
import re
import urllib.request

from tkinter import *
from tkinter import ttk
from tkinter import ttk

from lib.Data        import CollectionData
from lib.Data        import FilterData
from lib.Lib         import YNToX
from lib.Lib         import toggleYN
from lib.Img         import loadIcon
from lib.Export_HTML import Export_HTML

from gui.GUI_ItemInfo       import GUI_ItemInfo
from gui.GUI_Filter         import GUI_Filter
from gui.GUI_CollectionInfo import GUI_CollectionInfo
from gui.GUI_TreeView       import GUI_TreeView
from gui.GUI_Graph          import GUI_Graph
from gui.GUI_Settings       import GUI_Settings
from gui.GUI_Menu           import initMainMenu
from gui.GUI_Hotkeys        import initHotkeys
from gui.GUI_Popups         import initPopups

import lib.Var as VAR

from lib.Json import writeJson


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
        self.withdraw()
        self.title('VGC Analyzer')
        self.geometry('1000x750')
        self.iconphoto(False, loadIcon("game-controller-outline", 15, 15))

        if platform.system() == "Darwin" or platform.system() == "Windows":
            self.state('zoomed')
        if platform.system() == "Linux":
            self.style = ttk.Style()
            if len(self.style.theme_names()):
                print("Using theme", self.style.theme_names()[0])
                self.style.theme_use(self.style.theme_names()[0])

        self.protocol("WM_DELETE_WINDOW", self.onClose)

        # Frames
        # ------------------
        self.filter_frame = GUI_Filter(self, width=200 , height=550, pady=0, padx=10)
        self.view_frame   = GUI_TreeView(self, width=600 , height=550, pady=0 , padx=0)
        self.item_frame   = GUI_ItemInfo(self, width=200 , height=550, pady=0 , padx=0)
        self.graph_frame  = GUI_Graph(self, width=1000, height=200, pady=0 , padx=0)
        self.info_frame   = GUI_CollectionInfo(self, width=1000, height=200, pady=10, padx=10)

        self.filter_frame.grid(row=0, column=0, sticky="nws", rowspan=4)
        self.view_frame.grid(row=0, column=1, sticky="nwes")
        self.item_frame.grid(row=0, column=2, sticky="nes", rowspan=4)
        self.info_frame.grid(row=3, column=1, sticky="nwes")
        self.graph_frame.grid(row=2, column=1, sticky="nwes")
        self.graph_frame.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # TreeView context menu
        self.treeMenu = Menu(self, tearoff=0)
        self.treeMenu.add_command(label=_("Item details"), command=self.showItemDetails)
        self.treeMenu.add_command(label=_("Toggle bookmark"), command=self.toggleBookmark)
        self.treeMenu.add_command(label=_("Toggle completed"), command=self.toggleFinished)
        self.treeMenu.add_command(label=_("Update cover art"), command=self.item_frame.updateCover)
        self.treeMenu.add_command(label=_("Open on VGCollect.com"), command=self.item_frame.openOnVGCollect)

        # Init
        self.init()

        # Show window
        self.deiconify()


    ######################
    # init
    # --------------------
    def init(self):
        # Hotkeys
        initHotkeys(self)

        # Popup dialogs
        initPopups(self)

        # Main menu
        initMainMenu(self)


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
    # onClose
    # --------------------
    def onClose(self):
        self.collectionData.buildSaveData()
        writeJson(self.collectionData.localData_list, VAR.LOCAL_DATA_FILE)
        writeJson(self.collectionData.onlineData_list, VAR.ONLINE_DATA_FILE)
        self.destroy()


    ######################
    # toggleFilterFrame
    # --------------------
    def toggleFilterFrame(self):
        if self.filter_frame.winfo_ismapped():
            self.filter_frame.grid_forget()
        else:
            self.filter_frame.grid(row=0, column=0, sticky="nws", rowspan=4)
            self.update()


    ######################
    # toggleItemInfoFrame
    # --------------------
    def toggleItemInfoFrame(self):
        if self.item_frame.winfo_ismapped():
            self.item_frame.grid_forget()
        else:
            self.item_frame.grid(row=0, column=2, sticky="nes", rowspan=4)
            self.update()


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
        self.collectionData.parseData(self.view_frame.file_frame.combine_platforms.get())
        self.collectionData.sumData()

        self.filter_frame.fillGroupCombobox()
        self.filter_frame.fillOrderCombobox()


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
            self.view_frame.item_view.column("#0", width=200, stretch="Yes")
        else:
            self.view_frame.item_view.column("#0", width=0, stretch="No")

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
                                                  "",
                                                  "[" + str(groupData.item_count) + " " + _("items") + "]",
                                                  "",
                                                  "",
                                                  "[" + _("total price: ") + locCurrency(groupData.total_price) + "]"))

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

                # self.view_frame.treeviewSort("Title", False)


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
                item.VGC_id,
                item.name,
                item.platform,
                item.region,
                locCurrency(item.price),
                locDate(item.date),
                locDate(item.dateAdded),
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
            if filterData.orderItems == VAR.ORDER_BY_NAME or len(filterData.orderItems) == 0:
                return sorted(items, key=lambda item: item.name, reverse=filterData.orderItemsReverse)
            if filterData.orderItems == VAR.ORDER_BY_PRICE:
                return sorted(items, key=lambda item: item.price, reverse=filterData.orderItemsReverse)
            if filterData.orderItems == VAR.ORDER_BY_DATE :
                return sorted(items, key=lambda item: item.date, reverse=filterData.orderItemsReverse)
            if filterData.orderItems == VAR.ORDER_BY_DATE_ADDED :
                return sorted(items, key=lambda item: item.dateAdded, reverse=filterData.orderItemsReverse)
            if filterData.orderItems == VAR.ORDER_BY_REGION :
                return sorted(items, key=lambda item: item.region, reverse=filterData.orderItemsReverse)
            if filterData.orderItems == VAR.ORDER_BY_PLATFORM :
                return sorted(items, key=lambda item: item.platform, reverse=filterData.orderItemsReverse)
            if filterData.orderItems == VAR.ORDER_BY_NOTES :
                return sorted(items, key=lambda item: item.notes, reverse=filterData.orderItemsReverse)
        else:
            return items


    ######################
    # showViewContextMenu
    # --------------------
    def showViewContextMenu(self, event = None):
        try:
            # Get row under cursor
            row = self.view_frame.item_view.identify_row(event.y)

            if len(row):
                # Get row data
                rowData = self.view_frame.item_view.set(row)

                # Select row
                self.view_frame.item_view.focus(row)
                self.view_frame.item_view.selection_set(row)

                # Show menu
                self.treeMenu.selection = rowData
                self.treeMenu.post(event.x_root, event.y_root)
        finally:
            self.treeMenu.grab_release()


    ######################
    # getFilterInput
    # --------------------
    def getFilterInput(self):
        filterInput = self.filterData
        filterInput.inputsToFilter(self.filter_frame.filterInputs, self.filter_frame.multiFilter)

        return filterInput


    ######################
    # showAbout
    # --------------------
    def showAbout(self):
        self.pop_about.show()


    ######################
    # showSettings
    # --------------------
    def showSettings(self):
        self.settings = GUI_Settings(self, self.showSettingsCallback)


    ######################
    # showSettingsCallback
    # --------------------
    def showSettingsCallback(self):

        # Set column display
        self.view_frame.setColumnDisplay(resize=True)

        # Filter bindings
        if settings.get("display", "refreshOnFilterSelect", True):
            self.filter_frame.bindComboboxes()
        else:
            self.filter_frame.unbindComboboxes()

        # Read collection data
        self.readData()

        # Display collection data
        self.showData()


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
    # showItemDetails
    # --------------------
    def showItemDetails(self, a = None):
        if a == None or settings.get("display", "detailsOnDoubleClick", True):

            selection = self.view_frame.item_view.focus()

            if not selection[0] == "#":
                self.pop_itemDetails.show(self.activeItem())


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
    def setCurrentVGCFile(self, a = None):
        self.collectionData.csv_file = VAR.DATA_PATH + self.view_frame.file_frame.file_select.get()
        self.readData()
        self.showData()


    ######################
    # export
    # --------------------
    def export(self):
        e = Export_HTML(self.view_frame.item_view)

        e.export()


    ######################
    # getOnlineItemData
    # --------------------
    def getOnlineItemData(self):
        result = {}
        url = "https://vgcollect.com/item/" + str(self.activeItem().VGC_id)

        # Create request
        request = urllib.request.Request(url)


        # Get Page
        response = urllib.request.urlopen(request)

        # Parsing page text
        tableBodies = str(response.read()).split("<table class=\"table\">")
        tableBody = tableBodies[1].replace("\\r\\n", "")

        data = re.split("</*tbody>", tableBody)

        for line in re.split("<tr> * *<td.*?>", re.sub(" +", " ", data[1])):
            values = re.split("</td> * *<td>", line)

            if len(values) >= 2:
                result[values[0].strip(": ")] = values[1].replace("</td>", "").replace("</tr>", "").strip()

        return result
