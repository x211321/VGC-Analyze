import lib.Settings as settings

from lib.Style import initStyles
from lib.Locale import _
from lib.Locale import locCurrency
from lib.Locale import locDate

import os
import platform
import re
import urllib.request

from tkinter import *
from tkinter import messagebox

from lib.Version     import VERSION
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
from gui.GUI_Menu           import generateTemplateMenu
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

        # Init styles
        initStyles()

        # Data
        self.filterData     = FilterData()
        self.collectionData = CollectionData(self.filterData)
        self.index          = 0

        # Main window
        # ------------------
        self.withdraw()
        self.title("VGC Analyze" + " " + VERSION)
        self.geometry("1000x750")
        self.configure(bg=VAR.GUI_COLOR_SECONDARY)
        self.iconphoto(False, loadIcon("icon", 128, 128))

        if platform.system() == "Darwin" or platform.system() == "Windows":
            self.state('zoomed')
        if platform.system() == "Linux":
            self.attributes('-zoomed', True)

        self.protocol("WM_DELETE_WINDOW", self.onClose)

        # Frames
        # ------------------
        self.filter_frame = GUI_Filter(self, width=200 , height=550)
        self.view_frame   = GUI_TreeView(self, width=600 , height=550)
        self.item_frame   = GUI_ItemInfo(self, width=200 , height=550)
        self.graph_frame  = GUI_Graph(self, width=1000, height=200)
        self.info_frame   = GUI_CollectionInfo(self, width=1000, height=200)

        self.filter_frame.grid(row=0, column=0, sticky="nws", rowspan=4, pady=0, padx=10)
        self.view_frame.grid(row=0, column=1, sticky="nwes", pady=0 , padx=0)
        self.item_frame.grid(row=0, column=2, sticky="nes", rowspan=4, pady=0 , padx=5)
        self.graph_frame.grid(row=2, column=1, sticky="nwes", pady=0 , padx=0)
        self.info_frame.grid(row=3, column=1, sticky="nwes", pady=10, padx=10)
        self.graph_frame.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # TreeView context menu
        self.treeMenu = Menu(self, tearoff=0)
        self.treeMenu.add_command(label=_("Item details"), command=self.showItemDetails)
        self.treeMenu.add_command(label=_("Toggle bookmark"), command=self.toggleBookmark)
        self.treeMenu.add_command(label=_("Toggle completed"), command=self.toggleFinished)
        self.treeMenu.add_command(label=_("Update cover art"), command=lambda:self.item_frame.update(True))
        self.treeMenu.add_command(label=_("Open on VGCollect.com"), command=self.item_frame.openOnVGCollect)
        self.treeMenu.add_command(label=_("Open VGCollect list at item position"), command=self.item_frame.openVGCollectCollectionList)

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
        if not len(self.collectionData.collection_items) and not self.collectionData.dataError:
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
            self.filter_frame.grid(row=0, column=0, sticky="nws", rowspan=4, padx=10)
            self.update()


    ######################
    # toggleItemInfoFrame
    # --------------------
    def toggleItemInfoFrame(self):
        if self.item_frame.winfo_ismapped():
            self.item_frame.grid_forget()
        else:
            self.item_frame.grid(row=0, column=2, sticky="nes", rowspan=4, padx=5)
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
    # activeItemIndex
    # --------------------
    def activeItemIndex(self):
        return self.index


    ######################
    # readData
    # --------------------
    def readData(self):

        # Read, parse and sum collection data
        #--------------------
        readErr, readErr_   = self.collectionData.readData()
        parseErr, parseErr_ = self.collectionData.parseData(self.view_frame.file_frame.combine_platforms.get())

        if not len(readErr) and not len(parseErr):
            self.collectionData.sumData()

            itemID = 0
            for item in self.collectionData.collection_items:
                if item.VGC_id == itemID:
                    item.localData["duplicate"] = "X"

                itemID = item.VGC_id

            self.filter_frame.fillGroupCombobox()
            self.filter_frame.fillOrderCombobox()
        else:
            messagebox.showerror(_("Data error"), (readErr + "\n" + str(readErr_) + "\n" + parseErr + "\n" + str(parseErr_)).strip(), parent=self)


    ######################
    # showData
    # --------------------
    def showData(self, a = None):

        # Get user inputs
        displayFilter = self.getFilterInput()
        self.collectionData.setFilter(displayFilter)

        # Sum data acording to the user filter
        self.collectionData.sumData()

        itemID = 0
        for item in self.collectionData.collection_items:
            if item.VGC_id == itemID:
                item.localData["duplicate"] = "X"

            itemID = item.VGC_id

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
                item.notes,
                item.getLocalData("finishedNotes"),
                item.getOnlineData("selfCreated"),
                item.getLocalData("duplicate"))

    def getSortDateFinishedNotes(self, item):
        finishedNote = item.getLocalData("finishedNotes")
        if finishedNote.find(" - ") != -1:
            dateStart = finishedNote.find(" - ") + 3
            date = finishedNote[dateStart:dateStart+10]
        else:
            date = finishedNote.replace('Abgeschlossen: ', '')[0:10]

        date = date[6:10] + "-" + date[3:5] + "-" + date[0:2]
        return date



    ######################
    # sortViewItems
    # --------------------
    def sortViewItems(self, filterData, items):
        if len(filterData.orderItems) or filterData.orderDirection:
            if filterData.orderItems == VAR.ORDER_BY_NAME or len(filterData.orderItems) == 0:
                return sorted(items, key=lambda item: item.name, reverse=(filterData.orderDirection == VAR.ORDER_DIRECTION_DESCENDING))
            if filterData.orderItems == VAR.ORDER_BY_PRICE:
                return sorted(items, key=lambda item: item.price, reverse=(filterData.orderDirection == VAR.ORDER_DIRECTION_DESCENDING))
            if filterData.orderItems == VAR.ORDER_BY_DATE :
                return sorted(items, key=lambda item: item.date, reverse=(filterData.orderDirection == VAR.ORDER_DIRECTION_DESCENDING))
            if filterData.orderItems == VAR.ORDER_BY_DATE_ADDED :
                return sorted(items, key=lambda item: item.dateAdded, reverse=(filterData.orderDirection == VAR.ORDER_DIRECTION_DESCENDING))
            if filterData.orderItems == VAR.ORDER_BY_REGION :
                return sorted(items, key=lambda item: item.region, reverse=(filterData.orderDirection == VAR.ORDER_DIRECTION_DESCENDING))
            if filterData.orderItems == VAR.ORDER_BY_PLATFORM :
                return sorted(items, key=lambda item: item.platform, reverse=(filterData.orderDirection == VAR.ORDER_DIRECTION_DESCENDING))
            if filterData.orderItems == VAR.ORDER_BY_NOTES :
                return sorted(items, key=lambda item: item.notes, reverse=(filterData.orderDirection == VAR.ORDER_DIRECTION_DESCENDING))
            if filterData.orderItems == VAR.ORDER_BY_FINISHED_DATE :
                return sorted(items, key=lambda item: self.getSortDateFinishedNotes(item) ,reverse=(filterData.orderDirection == VAR.ORDER_DIRECTION_DESCENDING))
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

            try:
                if not selection[0] == "#":
                    self.pop_itemDetails.show(self.activeItem())
            except:
                pass


    ######################
    # collectionDownload_callback
    # --------------------
    def collectionDownload_callback(self, result, newPath):
        self.filterData.filePath = newPath
        self.view_frame.file_frame.file_select.set(os.path.basename(newPath))

        self.collectionData.setFilter(self.filterData)
        self.readData()
        self.showData()


    ######################
    # templateManager_callback
    # --------------------
    def templateManager_callback(self, template=None):
        generateTemplateMenu(self)

        if template:
            self.filter_frame.restore(template)
            self.showData()


    ######################
    # loadTemplate
    # --------------------
    def loadTemplate(self, templateName):
        self.filter_frame.restore(settings.getTemplate(templateName))
        self.showData()


    ######################
    # setCurrentVGCFile
    # --------------------
    def setCurrentVGCFile(self, a = None):
        file = self.view_frame.file_frame.file_select.get()

        if len(file):
            self.collectionData.csv_file = VAR.DATA_PATH + file
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
    def getOnlineItemData(self, VGC_id = 0):
        result = {}

        if VGC_id == 0:
            VGC_id = self.activeItem().VGC_id

        url = "https://vgcollect.com/item/" + str(VGC_id)

        # Create request
        request = urllib.request.Request(url)


        # Get Page
        response = urllib.request.urlopen(request)

        responseText = str(response.read())
        createdByPosStart = responseText.find("<td>Created</td>")
        createdByPosStart = responseText.rfind("<tr>", 0, createdByPosStart)
        createdByPosEnd = responseText.find("</tr>", createdByPosStart)

        createdBy = responseText[createdByPosStart:createdByPosEnd]
        createdByList = re.findall("<td><a .+</td>", createdBy)
        if len(createdByList) > 0:
            createdBy = createdByList[0]
            createdBy = re.sub("<td><a href=.+\">", "", createdBy)
            createdBy = re.sub("</a></td>.*", "", createdBy)

        username = settings.get("vgc", "username", "")

        # Parsing page text
        tableBodies = responseText.split("<table class=\"table\">")

        # Remove all CR+LF
        tableBodies[1] = tableBodies[1].replace("\\r\\n", "")

        # Remove all LF
        tableBody = tableBodies[1].replace("\\n", "")

        # Split data at </tbody>
        data = re.split("</*tbody>", tableBody)

        responseSubData = re.sub(" +", " ", data[1])
        responseList = re.split("<tr> * *<td.*?>", responseSubData)
        # Split data at <tr><td>                # Replace one or more whitespaces with exactly one space
        for line in responseList:
            # Split data at </td><td> while ignoring possible whitespaces between them
            values = re.split("</td> * *<td>", line)

            if len(values) >= 2:
                key = values[0].strip(": ")
                value = values[1].replace("</td>", "").replace("</tr>", "").strip()
                if key == "Rating":
                    # Remove the Image data from ratings
                    value = re.sub('<img .*alt=\"', '', value)
                    value = re.sub('\">', '', value)

                result[key] = value

        if len(username) > 0 and createdBy.lower() == username.lower():
            result["selfCreated"] = "X"

        return result


    ######################
    # getOnlineCollectionListPage
    # --------------------
    def getOnlineCollectionListPage(self, username, page):
        result = {}
        url = "https://vgcollect.com/" + username + "/" + page

        # Create request
        request = urllib.request.Request(url)

        # Get Page
        response = urllib.request.urlopen(request)

        return str(response.read())


    ######################
    # getOnlineCollectionListPage
    # --------------------
    def updateAllCovers(self, refresh=False):
        if len(self.collectionData.collection_items) > 0:
            for item in self.collectionData.collection_items:
                GUI_ItemInfo.updateCoversOnly(self.item_frame, item, refresh)


    def updateAllInfos(self):
        if len(self.collectionData.collection_items) > 0:

            # Set a limit how many items should be updated
            # VGC has gets a call for every item to the corresponding item page
            itemsToUpdate = 10
            if len(settings.get("vgc", "vgc_data", "")):
                itemsToUpdate = int(settings.get("vgc", "vgc_data", ""))

            updatedItems = 0
            for item in self.collectionData.collection_items:
                if item.id() not in self.collectionData.onlineData_list.keys() and updatedItems < itemsToUpdate:
                    # Store the response data in the corresponding variables
                    item.onlineData = self.getOnlineItemData(item.VGC_id)
                    self.collectionData.onlineData_list[item.id()] = item.onlineData
                    updatedItems = updatedItems + 1
                    print(updatedItems, " / ", itemsToUpdate, " updated")

            # Set the Json
            writeJson(self.collectionData.onlineData_list, VAR.ONLINE_DATA_FILE)


    def showMissingInfos(self):
        missingInfos = self.getMissingInfos()
        for missingInfo in missingInfos:
            print(missingInfo)
        print(len(missingInfos))

    def getMissingInfos(self):
        count = 0
        missingInfos = []

        # The ignore list works but can't be populated without doing it in code.
        # There should be a way in VGCAnalyze itself to do so but that isn't implemented yet.
        ignoreList = {}

        #ignoreList[98317] = ["Rating"]
        #ignoreList[209778] = ["Item Number"]
        #ignoreList[247695] = ["Rating"]
        #ignoreList[183534] = ["Barcode"]
        #ignoreList[211076] = ["Release Date"]
        #ignoreList[173607] = ["Barcode"]
        #ignoreList[214135] = ["Barcode"]
        #ignoreList[96408] = ["Item Number"]
        #ignoreList[135833] = ["Release Date"]
        #ignoreList[178256] = ["Barcode"]
        #ignoreList[173619] = ["Barcode"]
        #ignoreList[191804] = ["Release Date"]
        #ignoreList[198019] = ["Box Text"]
        #ignoreList[138165] = ["Barcode", "Box Text"]
        #ignoreList[17080] = ["Barcode", "Box Text", "Rating"]

        combine_platforms = False
        if combine_platforms != self.view_frame.file_frame.combine_platforms.get():
            combine_platforms = self.view_frame.file_frame.combine_platforms.get()
            self.view_frame.file_frame.combine_platforms.set(False)
            self.setCurrentVGCFile()

        for item in self.collectionData.collection_items:

            platformFilterList = [VAR.CAT_HARDWARE, VAR.CAT_ACCESSORIES, VAR.CAT_ACCESSORY, VAR.CAT_CONSOLES]
            skipPlatform = False
            for filter in platformFilterList:
                if len(item.platform) > len(filter) and filter == item.platform[-len(filter):]:
                    skipPlatform = True

            if item.id() in self.collectionData.onlineData_list.keys() and not skipPlatform:
                if not os.path.exists(VAR.getCoverPath(item, VAR.COVER_TYPE_FRONT)):
                    missingInfos.append(str(item.VGC_id) + " " + item.name + " " + VAR.COVER_TYPE_FRONT)
                if not os.path.exists(VAR.getCoverPath(item, VAR.COVER_TYPE_BACK)):
                    missingInfos.append(str(item.VGC_id) + " " + item.name + " " + VAR.COVER_TYPE_BACK)
                if not os.path.exists(VAR.getCoverPath(item, VAR.COVER_TYPE_CART)):
                    missingInfos.append(str(item.VGC_id) + " " + item.name + " " + VAR.COVER_TYPE_CART)


                optionalKeylist = ["Alt-Name", "Description"]
                keylist = ["Barcode", "Box Text", "Developer(s)", "Genre", "Item Number", "Publisher(s)", "Rating", "Release Date", "Release Type"]
                for key in keylist:
                    if item.getOnlineData(key) == "NA" and (item.VGC_id not in ignoreList or key not in ignoreList[item.VGC_id]):
                        missingInfos.append(str(item.VGC_id) + " " + item.name + " " + key)
                        count = count + 1

        if combine_platforms == True:
            self.view_frame.file_frame.combine_platforms.set(combine_platforms)
            self.setCurrentVGCFile()

        return missingInfos

    def getFinishedPage(self, username, page):
        url = "https://vgcollect.com/finished/"+ username + "/" + str(page)

        # Create request
        request = urllib.request.Request(url)

        # Get Page
        response = urllib.request.urlopen(request)

        return str(response.read())

    def getLastPage(self, pageData):
        maxpage = 0
        pageNavigationStart = pageData.find("<div class=\"row-fluid paginate\"")
        pageStart = 0
        if pageNavigationStart != -1:
            pageNavigationEnd = pageData.find("<div class=\"clearfix\"", pageNavigationStart)
            pageNavigationData = pageData[pageNavigationStart:pageNavigationEnd]

            exitLoop = False
            while not exitLoop:
                pageStart = pageNavigationData.find("<a href=", pageStart)
                if pageStart == -1:
                    exitLoop = True
                else:
                    pageStart = pageNavigationData.find(">", pageStart) + 1
                    pageEnd = pageNavigationData.find("</a>", pageStart)
                    tempPage = pageNavigationData[pageStart:pageEnd]
                    if tempPage.find("class") == -1:
                        maxpage = max(maxpage, int(tempPage))

            page = maxpage
        else:
            empty = pageData.find("<div id=\"tutor\"")

            if empty != -1:
                page = 0
            else:
                page = 1

        return page



    def refreshFinished(self):
        username = settings.get("vgc", "username", "")
        page = 1
        lastPageReached = False
        itemByVGCID = {}

        for item in self.collectionData.collection_items:
            item.localData["finished"] = VAR.ATTRIBUTE_NO
            item.localData["finishedNotes"] = ""
            itemByVGCID[str(item.VGC_id)] = item.index

        while not lastPageReached:
            print("Working on page: ", page)
            itemStart = 0
            pageData = self.getFinishedPage(username, page)
            exitItemLoop = False

            while not exitItemLoop:
                itemStart = pageData.find("<div class=\"item\"", itemStart)
                if itemStart == -1:
                    exitItemLoop = True
                else:
                    itemEnd = pageData.find("</div>", itemStart)
                    htmlItem = pageData[itemStart:itemEnd]
                    id = htmlItem.split("_")[1]
                    if str(id) in itemByVGCID:
                        index = itemByVGCID[str(id)]
                        item = self.collectionData.collection_items[index]
                        item.localData["finished"] = toggleYN(item.getLocalData("finished"))

                        # Entering notes of finished list
                        notesItemStart = pageData.find("<div class=\"item-notes\"", itemEnd)
                        noteStart = pageData.find("<span>", notesItemStart) + len("<span>")
                        noteEnd = pageData.find("</span>", noteStart)
                        note = pageData[noteStart:noteEnd]
                        if note != "None":
                            item.localData["finishedNotes"] = note
                        self.updateViewItem(index, item)
                    itemStart += 1

            if self.getLastPage(pageData) <= page:
                lastPageReached = True

            page += 1