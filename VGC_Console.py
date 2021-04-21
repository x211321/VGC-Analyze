

# Load required python modules
import sys


# Import classes from VGC_Data
from VGC_Data import CollectionData


# Import functions from VGC_Lib
from VGC_Lib import userInputBool
from VGC_Lib import userInputString


# Import functions from VGC_Print
from VGC_Print import getTextOutput
from VGC_Print import printQuery
from VGC_Print import printSums
from VGC_Print import printCategories


######################
# main_console
# --------------------
def main_console(filterData):

    # Interactive mode
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


    # Read, parse and sum collection data
    #--------------------
    collectionData = CollectionData(filterData)
    collectionData.readData()
    collectionData.parseData()
    collectionData.sumData()


    # List categories
    #--------------------
    if filterData.listCategories:
        printCategories(filterData, collectionData)
        exit()


    # Print data
    #--------------------
    if filterData.skipCategories:
        # Print query data
        printQuery(filterData, collectionData)
    else:
        # Print sums
        printSums(filterData, collectionData)


    # Write text file
    #--------------------
    file = open("VGC_Analyze.txt", "w", encoding="utf-8")
    file.write(getTextOutput())
    file.close()


    # No result
    #--------------------
    if len(getTextOutput()) == 0:
        print("  No results for query")
