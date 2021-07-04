from lib.Locale import _
from lib.Locale import i18nToRaw

import lib.Settings as settings

import re
import os

from enum        import IntEnum
from collections import OrderedDict
from os          import listdir

from lib.Json    import readJson
from lib.Lib     import guessDate

import lib.Var as VAR


######################
# CSVColumns
# --------------------
class CSVColumns(IntEnum):
    VGC_id   =  0
    name     =  1
    platform =  2
    notes    =  3
    cart     =  4
    box      =  5
    manual   =  6
    other    =  7
    price    =  8
    date     =  9
    added    = 10


######################
# CollectionItem
# --------------------
class CollectionItem(object):

    # Constructor
    # Parses csv-line to CollectionItem
    def __init__(self, csv_line = "", index = 0, localItemData_List = {}, onlineItemData_List = {}, combinePlatforms = False):
        csv_fields  = csv_line.split("\",\"")

        for index, field in enumerate(csv_fields):
            csv_fields[index] =field.strip(" ,\"\n")

        self.VGC_id     = 0
        self.name       = ""
        self.platform   = ""
        self.price      = 0.0
        self.date       = ""
        self.region     = ""
        self.cart       = ""
        self.box        = ""
        self.manual     = ""
        self.other      = ""
        self.notes      = ""
        self.dateAdded  = ""
        self.index      = index
        self.localData  = {}
        self.onlineData = {}

        if csv_line != "":
            self.VGC_id       = int(csv_fields[CSVColumns.VGC_id])
            self.name         = csv_fields[CSVColumns.name]
            self.platform     = self.getPlatformName(csv_fields[CSVColumns.platform], combinePlatforms)
            self.price        = float(csv_fields[CSVColumns.price])
            self.date         = csv_fields[CSVColumns.date]
            self.region       = self.getRegion(csv_fields[CSVColumns.platform])
            self.cart         = csv_fields[CSVColumns.cart]
            self.box          = csv_fields[CSVColumns.box]
            self.manual       = csv_fields[CSVColumns.manual]
            self.other        = csv_fields[CSVColumns.other]
            self.notes        = csv_fields[CSVColumns.notes]
            self.dateAdded    = csv_fields[CSVColumns.added].split(" ")[0]
            self.dateTimeAdded= csv_fields[CSVColumns.added]

            if len(self.region) == 0:
                self.region = _("[None]")

            # Check for platform overwrite
            if self.platform in settings.listPlatforms():
                self.platform = settings.getPlatformOverwrite(self.platform)

            # Find platform holder
            found = False

            for platformHolder in settings.listPlatformHolders():
                for keyword in settings.getPlatformHolderKeywords(platformHolder):
                    if keyword in self.platform.lower():
                        self.platformHolder = platformHolder
                        found = True
                        break
                if found:
                    break
            if found == False:
                self.platformHolder = _("[Other]")

            # Special case for categories that end on "Accessories" instead of "Accessory"
            if self.platform[-len(VAR.CAT_ACCESSORIES):] == VAR.CAT_ACCESSORIES:
                self.platform = self.platform[0:len(self.platform)-len(VAR.CAT_ACCESSORIES)] + VAR.CAT_ACCESSORY

            if self.id() in localItemData_List.keys():
                self.localData = localItemData_List[self.id()]
            if self.id() in onlineItemData_List.keys():
                self.onlineData = onlineItemData_List[self.id()]

    def getPlatformName(self, platformString, combinePlatforms):

        platformString = platformString.strip()

        if platformString[-4] == "[" and platformString[-1] == "]":
            platformString = platformString[0:len(platformString)-4].strip()
        else:
            platformString = platformString

        if combinePlatforms:
            if not platformString == VAR.CAT_HARDWARE:
                platformString = platformString.replace(VAR.CAT_HARDWARE, "").strip()
            if not platformString == VAR.CAT_ACCESSORY:
                platformString = platformString.replace(VAR.CAT_ACCESSORY, "").strip()
            if not platformString == VAR.CAT_ACCESSORIES:
                platformString = platformString.replace(VAR.CAT_ACCESSORIES, "").strip()

        return platformString

    def getRegion(self, platformString):
        platformString = platformString.strip()

        if platformString[-4] == "[" and platformString[-1] == "]":
            return platformString[-3:-1].strip()
        else:
            return ""

    def id(self):
        return str(self.VGC_id) + "-" + self.dateTimeAdded

    def getLocalData(self, key):
        value = ""

        if key in self.localData:
            value = self.localData[key]

        return value

    def getOnlineData(self, key):
        value = ""

        if key in self.onlineData:
            value = self.onlineData[key]

        return value

######################
# DataTotal
# --------------------
class DataTotal(object):

    # Constructor
    def __init__(self):
        self.items       = []
        self.item_count  = 0
        self.total_price = 0.0
        self.first       = CollectionItem()
        self.last        = CollectionItem()
        self.sub         = OrderedDict()


######################
# FilterData
# --------------------
class FilterData(object):

    # Constructor
    def __init__(self):
        self.itemFilter           = ""
        self.itemFilterRegEx      = False
        self.platformFilter       = []
        self.platformHolderFilter = []
        self.regionFilter         = ""
        self.notesFilter          = ""
        self.notesFilterRegEx     = False
        self.dateFilterStart      = ""
        self.dateFilterEnd        = ""
        self.dateAddedFilterStart = ""
        self.dateAddedFilterEnd   = ""
        self.priceFilterStart     = 0.0
        self.priceFilterEnd       = 0.0
        self.priceFilterStartSet  = False
        self.priceFilterEndSet    = False
        self.cartFilter           = ""
        self.boxFilter            = ""
        self.manualFilter         = ""
        self.otherFilter          = ""
        self.bookmarkedFilter     = ""
        self.finishedFilter       = ""

        self.orderItems           = ""
        self.orderDirection       = ""
        self.groupItems           = ""
        self.filePath             = ""
        self.graphStyle           = ""
        self.graphStepSize        = 0
        self.screenWidth          = 0
        self.skipCategories       = False
        self.listItems            = False
        self.listDetails          = False
        self.listVerbose          = False
        self.listCategories       = False
        self.listCategoriesDays   = False
        self.hideGraphs           = False
        self.graphIncludeZero     = False
        self.itemLines            = False
        self.categoryFilterList   = []
        self.guiMode              = False
        self.interactiveMode      = False

        self.filterList = {}


    def setFilterValue(self, key, value):
        self.filterList[key] = value
        return value


    def inputsToFilter(self, inputs, multiFilter):

        self.filterList = {}

        for key in multiFilter:
            if key == "platforms":
                self.platformFilter       = self.setFilterValue(key, multiFilter[key])
            if key == "platformHolders":
                self.platformHolderFilter = self.setFilterValue(key, multiFilter[key])
            if key == "regions":
                self.regionFilter         = self.setFilterValue(key, multiFilter[key])


        for key in inputs:
            if key == "name":
                self.itemFilter           = self.setFilterValue(key, inputs[key].get())
            if key =="name_regex":
                self.itemFilterRegEx      = self.setFilterValue(key, inputs[key]._toggleState)
            if key == "notes":
                self.notesFilter          = self.setFilterValue(key, inputs[key].get())
            if key =="notes_regex":
                self.notesFilterRegEx     = self.setFilterValue(key, inputs[key]._toggleState)
            if key == "dateStart":
                self.dateFilterStart      = self.setFilterValue(key, guessDate(inputs[key].get(), "start"))
            if key == "dateEnd":
                self.dateFilterEnd        = self.setFilterValue(key, guessDate(inputs[key].get(), "end"))
            if key == "dateAddedStart":
                self.dateAddedFilterStart = self.setFilterValue(key, guessDate(inputs[key].get(), "start"))
            if key == "dateAddedEnd":
                self.dateAddedFilterEnd   = self.setFilterValue(key, guessDate(inputs[key].get(), "end"))

            if key == "priceStart":
                if len(inputs[key].get()) > 0:
                    self.priceFilterStart    = self.setFilterValue(key, float(inputs[key].get()))
                    self.priceFilterStartSet = True
                else:
                    self.priceFilterStartSet = False
            if key == "priceEnd":
                if len(inputs[key].get()) > 0:
                    self.priceFilterEnd    = self.setFilterValue(key, float(inputs[key].get()))
                    self.priceFilterEndSet = True
                else:
                    self.priceFilterEndSet = False

            if key == "cart":
                self.cartFilter        = self.setFilterValue(key, i18nToRaw(VAR.ATTRIBUTE_YN, inputs[key].get()))
            if key == "box":
                self.boxFilter         = self.setFilterValue(key, i18nToRaw(VAR.ATTRIBUTE_YN, inputs[key].get()))
            if key == "manual":
                self.manualFilter      = self.setFilterValue(key, i18nToRaw(VAR.ATTRIBUTE_YN, inputs[key].get()))
            if key == "other":
                self.otherFilter       = self.setFilterValue(key, i18nToRaw(VAR.ATTRIBUTE_YN, inputs[key].get()))
            if key == "bookmarked":
                self.bookmarkedFilter  = self.setFilterValue(key, i18nToRaw(VAR.ATTRIBUTE_YN, inputs[key].get()))
            if key == "finished":
                self.finishedFilter    = self.setFilterValue(key, i18nToRaw(VAR.ATTRIBUTE_YN, inputs[key].get()))
            if key == "group":
                self.groupItems        = self.setFilterValue(key, i18nToRaw(VAR.GROUP_BY, inputs[key].get()))
            if key == "order":
                self.orderItems        = self.setFilterValue(key, i18nToRaw(VAR.ORDER_BY, inputs[key].get()))
            if key == "orderDirection":
                self.orderDirection    = self.setFilterValue(key, i18nToRaw(VAR.ORDER_DIRECTION, inputs[key].get()))


######################
# CollectionData
# --------------------
class CollectionData(object):
    csv_file   = ""
    csv_lines  = ""
    dataError  = False
    filterData = FilterData()
    collection_items = []

    # Sums
    groups             = OrderedDict()
    graph_groups       = OrderedDict()
    groupKey_priceHigh = ""
    groupKey_priceLow  = ""
    groupKey_countHigh = ""
    groupKey_countLow  = ""


    # Constructor
    def __init__(self, filterData):
        self.setFilter(filterData)
        self.localData_list  = readJson(VAR.LOCAL_DATA_FILE)
        self.onlineData_list = readJson(VAR.ONLINE_DATA_FILE)


    # setFilter
    def setFilter(self, filterData):
        self.filterData = filterData

        # Get newest csv-file
        if len(self.csv_file) == 0:
            self.csv_file = getCurrentVGCFile()


    # readData
    def readData(self):
        if len(self.csv_file) and os.path.exists(self.csv_file):
            try:
                # Open file
                file_handle    = open(self.csv_file, "r", encoding="utf-8")

                # Read lines
                self.csv_lines = file_handle.readlines()

                # Close file
                file_handle.close()

                return "", ""
            except Exception as err:
                self.dataError = True
                return _("Error opening collection file, please make sure the file is not locked by another application"), err

    # buildSaveData
    def buildSaveData(self):
        for item in self.collection_items:
            if item.localData:
                self.localData_list[item.id()] = item.localData
            if item.onlineData:
                self.onlineData_list[item.id()] = item.onlineData


    # parseData
    def parseData(self, combinePlatforms = False):
        settings.readPlatformHolders()
        settings.readPlatforms()
        self.collection_items = []

        index = 0

        try:
            for line in self.csv_lines[1:]:
                item = CollectionItem(line, localItemData_List=self.localData_list, onlineItemData_List=self.onlineData_list, combinePlatforms=combinePlatforms)

                item.index = index

                self.collection_items.append(item)

                index += 1
        except Exception as err:
            self.dataError = True
            self.collection_items = []
            return _("Error parsing collection data"), err

        if len(self.collection_items):
            self.dataError = False

        return "", ""


    # getFilteredData
    def getFilteredData(self):
        return list(filter(self.filter, self.collection_items))


    # filter
    def filter(self, item):
        if ((len(self.filterData.platformFilter) == 0 or item.platform in self.filterData.platformFilter) and
            (len(self.filterData.platformHolderFilter) == 0 or item.platformHolder in self.filterData.platformHolderFilter) and
            (len(self.filterData.regionFilter) == 0 or item.region in self.filterData.regionFilter) and
            (not self.filterData.itemFilterRegEx or self.searchFilter(self.filterData.itemFilter, item.name)) and
            (self.filterData.itemFilterRegEx or self.inStringFilter(self.filterData.itemFilter, item.name)) and
            (not self.filterData.notesFilterRegEx or self.searchFilter(self.filterData.notesFilter, item.notes)) and
            (self.filterData.notesFilterRegEx or self.inStringFilter(self.filterData.notesFilter, item.notes)) and
            self.stringGreater(self.filterData.dateFilterStart, item.date) and
            self.stringLess(self.filterData.dateFilterEnd, item.date) and
            self.stringGreater(self.filterData.dateAddedFilterStart, item.dateAdded) and
            self.stringLess(self.filterData.dateAddedFilterEnd, item.dateAdded) and
            self.priceGreater(self.filterData.priceFilterStart, item.price, self.filterData.priceFilterStartSet) and
            self.priceLess(self.filterData.priceFilterEnd, item.price, self.filterData.priceFilterEndSet) and
            self.stringEqual(self.filterData.cartFilter, item.cart) and
            self.stringEqual(self.filterData.boxFilter, item.box) and
            self.stringEqual(self.filterData.manualFilter, item.manual) and
            self.stringEqual(self.filterData.otherFilter, item.other) and
            self.stringEqual(self.filterData.bookmarkedFilter, item.getLocalData("bookmarked")) and
            self.stringEqual(self.filterData.finishedFilter, item.getLocalData("finished"))):

            return True
        else:
            return False


    # groupData
    def groupData(self):
        self.groups = self.group()

        self.groupKey_priceHigh = ""
        self.groupKey_priceLow  = ""
        self.groupKey_countHigh = ""
        self.groupKey_countLow  = ""

        for groupKey in self.groups.keys():
            if self.groupKey_priceHigh == "" or self.groups[groupKey].total_price > self.groups[self.groupKey_priceHigh].total_price:
                self.groupKey_priceHigh = groupKey
            if self.groupKey_priceLow == "" or self.groups[groupKey].total_price < self.groups[self.groupKey_priceLow].total_price:
                self.groupKey_priceLow  = groupKey
            if self.groupKey_countHigh == "" or self.groups[groupKey].item_count > self.groups[self.groupKey_countHigh].item_count:
                self.groupKey_countHigh = groupKey
            if self.groupKey_countLow == "" or self.groups[groupKey].item_count < self.groups[self.groupKey_countLow].item_count:
                self.groupKey_countLow  = groupKey


    # groupGraphData
    def groupGraphData(self, groupBy, subGroup = ""):
        self.graph_groups = self.group(groupBy, True, subGroup)


    # group
    def group(self, groupBy = "", sumOnly = False, subGroup = ""):

        result = OrderedDict()

        for item in self.getFilteredData():
            groupKey = self.getGroupKey(item, groupBy)

            if not groupKey in result.keys():
                result[groupKey] = DataTotal()

            result[groupKey].total_price += item.price
            result[groupKey].item_count  += 1

            if sumOnly == False:
                result[groupKey].items.append(item)

            if item.date < result[groupKey].first.date:
                result[groupKey].first.date = item.date

            if item.date > result[groupKey].last.date:
                result[groupKey].last.date = item.date

            if len(subGroup):
                subKey = self.getGroupKey(item, subGroup)

                if not subKey in result[groupKey].sub.keys():
                    result[groupKey].sub[subKey] = DataTotal()

                result[groupKey].sub[subKey].total_price += item.price
                result[groupKey].sub[subKey].item_count  += 1

                if sumOnly == False:
                    result[groupKey].sub[subKey].items.append(item)

                if item.date < result[groupKey].sub[subKey].first.date:
                    result[groupKey].sub[subKey].first.date = item.date

                if item.date > result[groupKey].sub[subKey].last.date:
                    result[groupKey].sub[subKey].last.date = item.date

        return result


    # getGroupKey
    def getGroupKey(self, item, groupBy):

        group = ""

        if not len(groupBy):
            groupBy = self.filterData.groupItems

        if groupBy == VAR.GROUP_BY_YEAR:
            group =  item.date[0:4]

        if groupBy == VAR.GROUP_BY_MONTH:
            group =  item.date[0:7]

        if groupBy == VAR.GROUP_BY_DAY:
            group =  item.date

        if groupBy == VAR.GROUP_BY_YEAR_ADDED:
            group =  item.dateAdded[0:4]

        if groupBy == VAR.GROUP_BY_MONTH_ADDED:
            group =  item.dateAdded[0:7]

        if groupBy == VAR.GROUP_BY_DAY_ADDED:
            group =  item.dateAdded

        if groupBy == VAR.GROUP_BY_REGION:
            group =  item.region

        if groupBy == VAR.GROUP_BY_NAME:
            group =  item.name

        if groupBy == VAR.GROUP_BY_PLATFORM:
            group =  item.platform

        if groupBy == VAR.GROUP_BY_PLATFORMHOLDER:
            group =  item.platformHolder

        if groupBy == VAR.GROUP_BY_NOTES:
            group =  item.notes

        if groupBy == VAR.GROUP_BY_VGCID:
            group =  str(item.VGC_id) + " (" + item.name + ")"

        if len(group.strip()) == 0:
            group = _("[None]")

        return group


    # getGroupPriceLow
    def getGroupPriceLow(self):
        return self.groups[self.groupKey_priceLow]


    # getGroupPriceHigh
    def getGroupPriceHigh(self):
        return self.groups[self.groupKey_priceHigh]


    # getGroupCountLow
    def getGroupCountLow(self):
        return self.groups[self.groupKey_countLow]


    # getGroupCountHigh
    def getGroupCountHigh(self):
        return self.groups[self.groupKey_countHigh]


    # searchFilter
    def searchFilter(self, filterVal, itemVal):
        if re.search(filterVal.lower(), itemVal.lower()) != None:
            return True
        else:
            return False


    # inStringFIlter
    def inStringFilter(self, filterVal, itemVal):
        if filterVal.lower() in itemVal.lower():
            return True
        else:
            return False


    # stringGreater
    def stringGreater(self, filterVal, itemVal):
        if len(filterVal) == 0 or itemVal >= filterVal:
            return True
        else:
            return False


    # stringLess
    def stringLess(self, filterVal, itemVal):
        if len(filterVal) == 0 or itemVal <= filterVal:
            return True
        else:
            return False


    #priceGreater
    def priceGreater(self, filterVal, itemVal, filterActive):
        if filterActive == False or itemVal >= filterVal:
            return True
        else:
            return False


    # priceLess
    def priceLess(self, filterVal, itemVal, filterActive):
        if filterActive == False or itemVal <= filterVal:
            return True
        else:
            return False


    # stringEqual
    def stringEqual(fself, filterVal, itemVal):
        if len(filterVal) == 0 or filterVal == itemVal or (not len(itemVal) and filterVal == "No"):
            return True
        else:
            return False


    # sumData
    def sumData(self):
        self.totals          = DataTotal()
        self.years           = OrderedDict()
        self.months          = OrderedDict()
        self.days            = OrderedDict()
        self.platforms       = OrderedDict()
        self.platformHolders = OrderedDict()
        self.categories      = OrderedDict()
        self.regions         = OrderedDict()

        self.platforms_all       = OrderedDict()
        self.platformHolders_all = OrderedDict()
        self.regions_all         = OrderedDict()

        # Sum filtered data
        #--------------------
        for item in self.getFilteredData():
            # Sum platforms
            self.sumDataDict(item.platform, self.platforms, item)

            # Sum platform holders
            self.sumDataDict(item.platformHolder, self.platformHolders, item)

            # Sum regions
            self.sumDataDict(item.region, self.regions, item)

            # Sum general hardware data
            if item.platform[-len(VAR.CAT_HARDWARE):] == VAR.CAT_HARDWARE:
                self.sumDataDict(VAR.CAT_HARDWARE, self.categories, item)

            # Sum general accessory data
            if item.platform[-len(VAR.CAT_ACCESSORY):] == VAR.CAT_ACCESSORY:
                self.sumDataDict(VAR.CAT_ACCESSORY, self.categories, item)

            # Sum years
            self.sumDataDict(item.date[0:4], self.years, item)

            # Sum months
            self.sumDataDict(item.date[0:7], self.months, item)

            # Sum days
            self.sumDataDict(item.date, self.days, item)

            # Sum totals
            self.sumTotals(self.totals, item)

        # Sum all
        for item in self.collection_items:
            # Sum platforms
            self.sumDataDict(item.platform, self.platforms_all, item)

            # Sum platform holders
            self.sumDataDict(item.platformHolder, self.platformHolders_all, item)

            # Sum regions
            self.sumDataDict(item.region, self.regions_all, item)


    # sumTotals
    def sumTotals(self, totalData, item):
        # Sum data
        totalData.item_count  += 1
        totalData.total_price += item.price

        if dateValid(item.date):
            if (item.date < totalData.first.date or totalData.first.date == ""):
                totalData.first = item

            if (item.date >= totalData.last.date):
                totalData.last = item


    # sumDataDict
    def sumDataDict(self, key, dataDict, item):
        # Remove whitespaces from key
        key = key.strip()

        # Init dictionary entry
        if key not in dataDict:
            dataDict[key] = DataTotal()

        # Sum data
        self.sumTotals(dataDict[key], item)


######################
# getCurrentVGCFile
# --------------------
def getCurrentVGCFile():
    current_file = ""

    if not os.path.exists(VAR.DATA_PATH):
        os.makedirs(VAR.DATA_PATH)

    file_list = listdir(VAR.DATA_PATH)

    # Search for newest file
    for file in file_list:
        # Ignore files that don't start with the correct prefix
        if file[0 : len(VAR.FILE_PREFIX)] == VAR.FILE_PREFIX:
            current_file = VAR.DATA_PATH + file

    return current_file



######################
# dateValid
# --------------------
def dateValid(date):
    if date != "0000-00-00":
        return True
    else:
        return False
