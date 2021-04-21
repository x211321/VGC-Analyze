

# Benötigte Python module importieren
import sys


# Klassen aus VGC_Lib importieren
from VGC_Data import CollectionData


# Funktionen aus VGC_Lib importieren
from VGC_Lib import userInputBool
from VGC_Lib import userInputString


# Funktionen aus VGC_Print importieren
from VGC_Print import getTextOutput
from VGC_Print import printQuery
from VGC_Print import printSums
from VGC_Print import printCategories


######################
# main_console Function
# --------------------   
def main_console(filterData):

    # Interaktiver Modus
    #--------------------
    if filterData.interactiveMode:
        print("  VGCollect-Analyzer - interactive mode\n")

        filterData.listItems          = userInputBool("  List items [Y/n]: ")
        filterData.listDetails        = userInputBool("  List details [Y/n]: ")
        filterData.itemFilter         = userInputString("  Item filter: ")
        filterData.platformFilter     = userInputString("  Platform filter: ")
        filterData.regionFilter       = userInputString("  Region filter [EU/NA/JP/...]: ")
        filterData.priceFilterStart   = float(userInputString("  Only items with prices greater then: ", "0"))
        filterData.priceFilterEnd     = float(userInputString("  Only items with prices less then: ", "0"))
        filterData.dateFilterStart    = userInputString("  Only items purchased after [YYYY-MM-DD]: ")
        filterData.dateFilterEnd      = userInputString("  Only items purchased before [YYYY-MM-DD]: ")
        filterData.orderItems         = userInputString("  Order items by [name, price, date, region, platform]: ")
        filterData.groupItems         = userInputString("  Group items by [year, month, day, name, region, platform]: ")
        filterData.skipCategories     = userInputBool("  Skip categories (combine all results) [y/N]: ", False)
        
        if filterData.skipCategories == False:
            filterData.categoryFilterList = userInputString("  Category filter (comma separated) [wii, 3ds, 2020, ...]: ").split(",")


    # Daten einlesen, parsen und summieren
    #--------------------
    collectionData = CollectionData(filterData)
    collectionData.readData()
    collectionData.parseData()
    collectionData.sumData()


    # Kategorien auflisten
    #--------------------
    if filterData.listCategories:
        printCategories(filterData, collectionData)
        exit()


    # Daten ausgeben
    #--------------------
    if filterData.skipCategories:
        # Query-Daten ausgeben
        printQuery(filterData, collectionData)
    else:
        # Summen ausgeben
        printSums(filterData, collectionData)


    # Textdatei ausgeben
    #--------------------
    file = open("VGC_Analyze.txt", "w", encoding="utf-8")
    file.write(getTextOutput())
    file.close()
    
    
    # Keine Daten gefunden?
    #--------------------
    if len(getTextOutput()) == 0:
        print("  No results for query")
