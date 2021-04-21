

import re
import os

from enum        import IntEnum
from collections import OrderedDict
from os          import listdir

from VGC_Var     import FILE_PREFIX

# Globale liste zum definieren
# der möglichen Konsolenparameter
options    = []

CAT_HARDWARE     = "Hardware"
CAT_ACCESSORY    = "Accessory"
CAT_ACCESSORIES  = "Accessories"


######################
# guessDate Function
# --------------------
def guessDate(date, mode):
    if len(date) == 10:
        return date
    if len(date) == 7:
        if mode == "start":
            return date + "-01"
        if mode == "end":
            return date + "-31"
    if len(date) == 4:
        if mode == "start":
            return date + "-01-01"
        if mode == "end":
            return date + "-12-31"
    
    return date
    

######################
# CSVColumns Enum
# --------------------
class CSVColumns(IntEnum):
    id       =  0
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
# CollectionItem Class
# --------------------
class CollectionItem(object):

    # Constructor - Teilt CSV-Zeile in Object-Member auf
    def __init__(self, csv_line = "", index = 0):
        csv_fields  = csv_line.split("\",\"")

        self.id         = 0
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
        self.bookmarked = ""
        self.index      = index

        if csv_line != "":
            self.id       = int(csv_fields[CSVColumns.id][1:].strip())
            self.name     = csv_fields[CSVColumns.name].strip()
            self.platform = self.getPlatformName(csv_fields[CSVColumns.platform].strip())
            self.price    = float(csv_fields[CSVColumns.price].strip())
            self.date     = csv_fields[CSVColumns.date].strip()
            self.region   = self.getRegion(csv_fields[CSVColumns.platform].strip())
            self.cart     = csv_fields[CSVColumns.cart].strip()
            self.box      = csv_fields[CSVColumns.box].strip()
            self.manual   = csv_fields[CSVColumns.manual].strip()
            self.other    = csv_fields[CSVColumns.other].strip()
            self.notes    = csv_fields[CSVColumns.notes].strip()
            
            # Fix für Platformen die auf "Accessories" anstelle "Accessory" enden
            if self.platform[-len(CAT_ACCESSORIES):] == CAT_ACCESSORIES:
                self.platform = self.platform[0:len(self.platform)-len(CAT_ACCESSORIES)] + CAT_ACCESSORY
                
    def getPlatformName(self, platformString):
        platformString = platformString.strip()
        if platformString[-4] == "[" and platformString[-1] == "]":
            return platformString[0:len(platformString)-4].strip()
        else:
            return platformString
            
    def getRegion(self, platformString):
        platformString = platformString.strip()
        
        if platformString[-4] == "[" and platformString[-1] == "]":
            return platformString[-3:-1].strip()
        else:
            return ""
            

######################
# DataTotal Class
# --------------------
class DataTotal(object):

    # Constructor
    def __init__(self):
        self.items       = []
        self.item_count  = 0
        self.total_price = 0.0
        self.first       = CollectionItem()
        self.last        = CollectionItem()


######################
# FilterData Class
# --------------------
class FilterData(object):

    # Constructor
    def __init__(self):
        self.itemFilter         = ""
        self.platformFilter     = ""
        self.regionFilter       = ""
        self.notesFilter        = ""
        self.dateFilterStart    = ""
        self.dateFilterEnd      = ""
        self.priceFilterStart   = 0.0
        self.priceFilterEnd     = 0.0
        self.priceFilterStartSet= False
        self.priceFilterEndSet  = False
        self.cartFilter         = ""
        self.boxFilter          = ""
        self.manualFilter       = ""
        self.otherFilter        = ""
        self.bookmarkedFilter   = ""
        
        self.orderItems         = ""
        self.orderItemsReverse  = False
        self.groupItems         = ""
        self.filePath           = ""
        self.graphStyle         = ""
        self.graphStepSize      = 0
        self.screenWidth        = 0
        self.skipCategories     = False
        self.listItems          = False
        self.listDetails        = False
        self.listVerbose        = False
        self.listCategories     = False
        self.listCategoriesDays = False
        self.hideGraphs         = False
        self.graphIncludeZero   = False
        self.itemLines          = False
        self.categoryFilterList = []
        self.guiMode            = False
        self.interactiveMode    = False

        
    def inputsToFilter(self, inputs):
        for key in inputs:
            if key == "name":
                self.itemFilter      = inputs[key].get()
            if key == "platform":
                self.platformFilter  = inputs[key].get()
            if key == "region":
                self.regionFilter    = inputs[key].get()
            if key == "notes":
                self.notesFilter     = inputs[key].get()
            if key == "dateStart":
                self.dateFilterStart = guessDate(inputs[key].get(), "start")
            if key == "dateEnd":
                self.dateFilterEnd   = guessDate(inputs[key].get(), "end")

            if key == "priceStart":
                if len(inputs[key].get()) > 0:
                    self.priceFilterStart    = float(inputs[key].get())
                    self.priceFilterStartSet = True
                else:
                    self.priceFilterStartSet = False
            if key == "priceEnd":
                if len(inputs[key].get()) > 0:
                    self.priceFilterEnd    = float(inputs[key].get())
                    self.priceFilterEndSet = True
                else:
                    self.priceFilterEndSet = False

            if key == "cart":
                self.cartFilter        = inputs[key].get()
            if key == "box":
                self.boxFilter         = inputs[key].get()
            if key == "manual":
                self.manualFilter      = inputs[key].get()
            if key == "other":
                self.otherFilter       = inputs[key].get()
            if key == "bookmarked":
                self.bookmarkedFilter  = inputs[key].get()
            if key == "group":
                self.groupItems        = inputs[key].get()
            if key == "order":
                self.orderItems        = inputs[key].get()
            if key == "orderDirection":
                self.orderItemsReverse = (inputs[key].get() == "descending")
               

######################
# CollectionData Class
# --------------------
class CollectionData(object):
    csv_file   = ""
    csv_lines  = ""
    filterData = FilterData()
    collection_items = []
    
    # Summen
    totals     = DataTotal()
    years      = OrderedDict()
    months     = OrderedDict()
    days       = OrderedDict()
    platforms  = OrderedDict()
    categories = OrderedDict()
    regions    = OrderedDict()
    
    groups        = OrderedDict()
    groupKey_priceHigh = ""
    groupKey_priceLow  = ""
    groupKey_countHigh = ""
    groupKey_countLow  = ""
    
    # Constructor
    def __init__(self, filterData):
        self.setFilter(filterData)

    # setFilter
    def setFilter(self, filterData):
        self.filterData = filterData
        self.csv_file   = filterData.filePath
        
        # Aktuelle Datei ermitteln
        if len(self.csv_file) == 0:
            self.csv_file = getCurrentVGCFile()

    # readData
    def readData(self):    
        if len(self.csv_file) and os.path.exists(self.csv_file):
            # Info Ausgabe aktuelle Datei
            print("\n  Analyzing File: " + self.csv_file + "\n")

            # Datei öffnen
            file_handle    = open(self.csv_file, "r", encoding="utf-8")

            # Zeilen einlesen
            self.csv_lines = file_handle.readlines()

            # Datei schließen
            file_handle.close()
    
    
    # parseData 
    def parseData(self, bookmarks = []):    
        self.collection_items = []
        
        index = 0
    
        for line in self.csv_lines[1:]:
            item = CollectionItem(line)
            
            if len(bookmarks) and item.id in bookmarks:
                item.bookmarked = "Yes"
            else:
                item.bookmarked = "No"

            if (self.searchFilter(self.filterData.itemFilter, item.name) and 
               self.searchFilter(self.filterData.platformFilter, item.platform) and 
               self.searchFilter(self.filterData.notesFilter, item.notes) and 
               self.searchFilter(self.filterData.regionFilter, item.region) and
               self.stringGreater(self.filterData.dateFilterStart, item.date) and 
               self.stringLess(self.filterData.dateFilterEnd, item.date) and 
               self.priceGreater(self.filterData.priceFilterStart, item.price, self.filterData.priceFilterStartSet) and 
               self.priceLess(self.filterData.priceFilterEnd, item.price, self.filterData.priceFilterEndSet) and 
               self.stringEqual(self.filterData.cartFilter, item.cart) and
               self.stringEqual(self.filterData.boxFilter, item.box) and
               self.stringEqual(self.filterData.manualFilter, item.manual) and 
               self.stringEqual(self.filterData.otherFilter, item.other) and 
               self.stringEqual(self.filterData.bookmarkedFilter, item.bookmarked)):
               
               item.index = index
               
               self.collection_items.append(item)
               
               index += 1
               
               
    def groupData(self):
        
        self.groups = OrderedDict()
        self.groupKey_priceHigh = ""
        self.groupKey_priceLow  = ""
        self.groupKey_countHigh = ""
        self.groupKey_countLow  = ""
        
        for item in self.collection_items:
            groupKey = self.getGroupKey(item)
            
            if not groupKey in self.groups.keys():
                self.groups[groupKey] = DataTotal()
                
            self.groups[groupKey].items.append(item)
            self.groups[groupKey].total_price += item.price
            self.groups[groupKey].item_count  += 1
            
            if item.date < self.groups[groupKey].first.date:
                self.groups[groupKey].first.date = item.date
            
            if item.date > self.groups[groupKey].last.date:
                self.groups[groupKey].last.date = item.date
                
        for groupKey in self.groups.keys():
            if self.groupKey_priceHigh == "" or self.groups[groupKey].total_price > self.groups[self.groupKey_priceHigh].total_price:
                self.groupKey_priceHigh = groupKey
            if self.groupKey_priceLow == "" or self.groups[groupKey].total_price < self.groups[self.groupKey_priceLow].total_price:
                self.groupKey_priceLow  = groupKey
            if self.groupKey_countHigh == "" or self.groups[groupKey].item_count > self.groups[self.groupKey_countHigh].item_count:
                self.groupKey_countHigh = groupKey
            if self.groupKey_countLow == "" or self.groups[groupKey].item_count < self.groups[self.groupKey_countLow].item_count:
                self.groupKey_countLow  = groupKey
        

    def getGroupKey(self, item):
    
        if self.filterData.groupItems == "year":
            group =  item.date[0:4]
        
        if self.filterData.groupItems == "month":
            group =  item.date[0:7]
            
        if self.filterData.groupItems == "day":
            group =  item.date
            
        if self.filterData.groupItems == "region":
            group =  item.region
            
        if self.filterData.groupItems == "name":
            group =  item.name
            
        if self.filterData.groupItems == "platform":
            group =  item.platform
            
        if self.filterData.groupItems == "notes":
            group =  item.notes
            
        if len(group.strip()) == 0:
            group = "[None]"
            
        return group

    def getGroupPriceLow(self):
        return self.groups[self.groupKey_priceLow]

    def getGroupPriceHigh(self):
        return self.groups[self.groupKey_priceHigh]

    def getGroupCountLow(self):
        return self.groups[self.groupKey_countLow]

    def getGroupCountHigh(self):
        return self.groups[self.groupKey_countHigh]

    def searchFilter(self, filterVal, itemVal):
        if re.search(filterVal.lower(), itemVal.lower()) != None:
            return True
        else:
            return False
            
    def stringGreater(self, filterVal, itemVal):
        if len(filterVal) == 0 or itemVal >= filterVal:
            return True
        else:
            return False
            
    def stringLess(self, filterVal, itemVal):
        if len(filterVal) == 0 or itemVal <= filterVal:
            return True
        else:
            return False
         
    def priceGreater(self, filterVal, itemVal, filterActive):
        if filterActive == False or itemVal >= filterVal:
            return True
        else:
            return False
         
    def priceLess(self, filterVal, itemVal, filterActive):
        if filterActive == False or itemVal <= filterVal:
            return True
        else:
            return False

    def stringEqual(fself, filterVal, itemVal):
        if len(filterVal) == 0 or filterVal == itemVal:
            return True
        else:
            return False


    # sumData
    def sumData(self):
        self.totals = DataTotal()
    
        # Daten auswerten
        #--------------------
        for item in self.collection_items:

            # Platformdaten aufsummieren
            self.sumDataDict(item.platform, self.platforms, item)
            
            # Regiondaten aufsummieren
            self.sumDataDict(item.region, self.regions, item)
            
            # Allgemeine Daten (Hardware) aufsummieren
            if item.platform[-len(CAT_HARDWARE):] == CAT_HARDWARE:
                self.sumDataDict(CAT_HARDWARE, self.categories, item)

            # Allgemeine Daten (Accessories) aufsummieren
            if item.platform[-len(CAT_ACCESSORY):] == CAT_ACCESSORY:
                self.sumDataDict(CAT_ACCESSORY, self.categories, item)

            # Jahre aufsummieren
            self.sumDataDict(item.date[0:4], self.years, item)
            
            # Monate aufsummieren
            self.sumDataDict(item.date[0:7], self.months, item)

            # Tage aufsummieren
            self.sumDataDict(item.date, self.days, item)

            # Gesamtdaten aufsummieren
            self.sumTotals(self.totals, item)
            
            
    # sumTotals Function
    def sumTotals(self, totalData, item):       
        # Daten summieren
        totalData.item_count  += 1
        totalData.total_price += item.price
        
        if dateValid(item.date):
            if (item.date < totalData.first.date or totalData.first.date == ""):
                totalData.first = item
                
            if (item.date >= totalData.last.date):
                totalData.last = item


    # sumDataDict
    def sumDataDict(self, key, dataDict, item):
        # Leerzeichen im Schlüssel entfernen
        key = key.strip()

        # Eintrag im Dictionary initialisieren
        # Wenn noch nicht vorhanden
        if key not in dataDict:
            dataDict[key] = DataTotal()
            
        # Daten summieren
        self.sumTotals(dataDict[key], item)


    # updateItem
    def updateItem(self, updatedItem):
        for item in self.collection_items:
            if item.id == updatedItem.id:
                item = updatedItem
                break                
    
    
######################
# getCurrentVGCFile 
# --------------------
def getCurrentVGCFile():
    file_list    = listdir()
    current_file = ""

    # Aktuelle Datei ermitteln
    for file in file_list:
        # Nur Dateien die mit dem korrekten Präfix anfangen
        if file[0 : len(FILE_PREFIX)] == FILE_PREFIX:
            current_file = file

    return current_file
    

######################
# dateValid Function
# --------------------
def dateValid(date):
    if date != "0000-00-00":
        return True
    else:
        return False