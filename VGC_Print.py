
import math
import re
import struct
import sys

from VGC_Data import DataTotal
from VGC_Data import CollectionItem
from VGC_Data import options

from VGC_Var import CONSOLE_COLUMNS
from VGC_Var import CONSOLE_OVERHEAD


# Global variable to collect
# text file output
textOutput = ""


######################
# setScreenWidth
# --------------------
def setScreenWidth(width):
    global CONSOLE_COLUMNS

    if width > 0:
        CONSOLE_COLUMNS = width
    else:
        CONSOLE_COLUMNS, h = getTerminalSize_Windows()
        CONSOLE_COLUMNS = CONSOLE_COLUMNS - CONSOLE_OVERHEAD


######################
# getTerminalSize_Windows
# https://gist.github.com/jtriley/1108174
# --------------------
def getTerminalSize_Windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        return 0, 0
        pass


######################
# getTextOutput
# --------------------
def getTextOutput():
    return textOutput


######################
# printCategories
# --------------------
def printCategories(filterData, collectionData):
    printSubCategories({}             , "Collection", True)
    printSubCategories(collectionData.platforms , "Platforms")
    printSubCategories(collectionData.categories, "Generic")
    printSubCategories(collectionData.years     , "Years"     , False, 4)
    printSubCategories(collectionData.months    , "Months"    , False, 4)
    if filterData.listCategoriesDays:
        printSubCategories(collectionData.days  , "Days"      , False, 4)


######################
# printSubCategories
# --------------------
def printSubCategories(data, title, buildIn = False, columns = 2):
    count        = 0
    categoryLine = ""

    consoleStartBlock("Listing categories (" + title + ")")

    for category, dummy in sorted(data.items()):
        categoryLine += (" - " + category).ljust(int(CONSOLE_COLUMNS/columns))
        count        += 1

        if count % columns == 0:
            consoleLine(categoryLine)
            categoryLine = ""

    if len(categoryLine):
        consoleLine(categoryLine)

    if buildIn:
        consoleLine(" - collection")

    consoleEndBlock()


######################
# printQuery
# --------------------
def printQuery(filterData, collectionData):
    title = getCategoryTitle("Custom query result", filterData)

    printSum(title, collectionData.totals, collectionData.collection_items, filterData.hideGraphs == False, filterData, "", "all")

    if filterData.hideGraphs == False:
        # Data over multiple years -> Show year graph
        if collectionData.totals.first.date[0:4] != collectionData.totals.last.date[0:4]:
            drawTimeGraph("Yearly spending", "total_price", "", collectionData.years, collectionData.totals, "total", filterData.graphStyle, filterData.graphStepSize, True, False, filterData.graphIncludeZero)
            drawTimeGraph("Yearly items", "item_count", "", collectionData.years, collectionData.totals, "total", filterData.graphStyle, filterData.graphStepSize, False, False, filterData.graphIncludeZero)
        # Data over less then one month -> Show day graph
        elif collectionData.totals.first.date[0:7] == collectionData.totals.last.date[0:7]:
            drawTimeGraph("Daily spending", "total_price", collectionData.totals.first.date[0:7], collectionData.days, collectionData.totals, "month", filterData.graphStyle, filterData.graphStepSize, True, False, filterData.graphIncludeZero)
            drawTimeGraph("Daily items", "item_count", collectionData.totals.first.date[0:7], collectionData.days, collectionData.totals, "month", filterData.graphStyle, filterData.graphStepSize, False, False, filterData.graphIncludeZero)
        # Data over more than one month but less than one year -> Show month graph
        elif collectionData.totals.first.date[0:4] == collectionData.totals.last.date[0:4]:
            drawTimeGraph("Monthly spending", "total_price", collectionData.totals.first.date[0:4], collectionData.months, collectionData.totals, "year", filterData.graphStyle, filterData.graphStepSize, True, False, filterData.graphIncludeZero)
            drawTimeGraph("Monthly items", "item_count", collectionData.totals.first.date[0:4], collectionData.months, collectionData.totals, "year", filterData.graphStyle, filterData.graphStepSize, False, False, filterData.graphIncludeZero)


######################
# printSums Function
# --------------------
def printSums(filterData, collectionData):
    # Print platform data
    for platform, data in sorted(collectionData.platforms.items()):
        title = getCategoryTitle(platform, filterData)

        if len(filterData.categoryFilterList) == 0 or searchListInString(filterData.categoryFilterList, platform):
            printSum(title, data, collectionData.collection_items, False, filterData, platform, "platform")


    # Print general data
    for category, data in sorted(collectionData.categories.items()):
        title = getCategoryTitle(category + " totals", filterData)

        if len(filterData.categoryFilterList) == 0 or searchListInString(filterData.categoryFilterList, category + " totals"):
            printSum(title, data, collectionData.collection_items, False, filterData, category, "platform-right")


    # Print yearly data
    for year, data in sorted(collectionData.years.items()):
        title = getCategoryTitle(year, filterData)

        if len(filterData.categoryFilterList) == 0 or searchListInString(filterData.categoryFilterList, year):
            printSum(title, data, collectionData.collection_items, filterData.hideGraphs == False, filterData, year, "year")

            if filterData.hideGraphs == False:
                drawTimeGraph("Monthly spending", "total_price", year, collectionData.months, data, "year", filterData.graphStyle, filterData.graphStepSize, True)
                drawTimeGraph("Monthly items", "item_count", year, collectionData.months, data, "year", filterData.graphStyle, filterData.graphStepSize)


    # Print monthly data
    for month, data in sorted(collectionData.months.items()):
        title = getCategoryTitle(month, filterData)
        if searchListInString(filterData.categoryFilterList, month, True):
            printSum(title, data, collectionData.collection_items, filterData.hideGraphs == False, filterData, month, "month")

            if filterData.hideGraphs == False:
                drawTimeGraph("Daily spending", "total_price", month, collectionData.days, data, "month", filterData.graphStyle, filterData.graphStepSize, True)
                drawTimeGraph("Daily items", "item_count", month, collectionData.days, data, "month", filterData.graphStyle, filterData.graphStepSize)


    # Print daily data
    for day, data in sorted(collectionData.days.items()):
        title = getCategoryTitle(day, filterData)
        if searchListInString(filterData.categoryFilterList, day, True):
            printSum(title, data, collectionData.collection_items, False, filterData, day, "day")


    # Print total sums
    if len(filterData.categoryFilterList) == 0 or searchListInString(filterData.categoryFilterList, "Collection totals"):
        title = getCategoryTitle("Collection totals", filterData)
        printSum(title, collectionData.totals, collectionData.collection_items, filterData.hideGraphs == False, filterData)

        if filterData.hideGraphs == False:
            drawTimeGraph("Yearly spending", "total_price", "", collectionData.years, collectionData.totals, "total", filterData.graphStyle, filterData.graphStepSize, True, False, filterData.graphIncludeZero)
            drawTimeGraph("Yearly items", "item_count", "", collectionData.years, collectionData.totals, "total", filterData.graphStyle, filterData.graphStepSize, True, False, filterData.graphIncludeZero)
            drawTimeGraph("Collection growth (value)", "total_price", "", collectionData.years, collectionData.totals, "total", filterData.graphStyle, filterData.graphStepSize, True, True, filterData.graphIncludeZero)
            drawTimeGraph("Collection growth (items)", "item_count", "", collectionData.years, collectionData.totals, "total", filterData.graphStyle, filterData.graphStepSize, False, True, filterData.graphIncludeZero)


######################
# printSum
# --------------------
def printSum(title, data, items, noEndLine, filterData, itemCategoryFilter = "", itemCategoryFilterValue = ""):
    outputLine()

    consoleStartBlock(title)
    consoleLine("  - Number of items: " + str(data.item_count))
    consoleLine("  - Total value    : " + format(data.total_price, ".2f"))
    consoleLine("  - First purchase : " + data.first.date)
    consoleLine("                     " + data.first.name)
    consoleLine("                     " + data.first.platform + " " + data.first.region)
    consoleLine("  - Last purchase  : " + data.last.date)
    consoleLine("                     " + data.last.name)
    consoleLine("                     " + data.last.platform + " " + data.last.region)

    if filterData.listItems:
        consoleLine()
        consoleMidBlock("Items")

        totalPrice          = 0.0
        totalCount          = 0
        sectionPrice        = 0.0
        sectionCount        = 0
        idWidth             = 10
        notesWidth          = 30
        platformWidth       = 40
        sectionSumPrinted   = False
        details             = ""
        verbose             = ""
        verboseAttr         = ""
        lastItem            = CollectionItem()

        if len(filterData.orderItems):
            if filterData.orderItems.lower() == "name" :
                items = sorted(items, key=lambda item: item.name, reverse=filterData.orderItemsReverse)
            if filterData.orderItems.lower() == "price":
                items = sorted(items, key=lambda item: item.price, reverse=filterData.orderItemsReverse)
            if filterData.orderItems.lower() == "date" :
                items = sorted(items, key=lambda item: item.date, reverse=filterData.orderItemsReverse)
            if filterData.orderItems.lower() == "region" :
                items = sorted(items, key=lambda item: item.region, reverse=filterData.orderItemsReverse)
            if filterData.orderItems.lower() == "platform" :
                items = sorted(items, key=lambda item: item.platform, reverse=filterData.orderItemsReverse)

        for item in items:
            if itemFilterValid(item, itemCategoryFilter, itemCategoryFilterValue):

                if filterData.listVerbose:
                    verboseAttr = ("  " + YNToX(item.cart) + " " +
                                   "  " + YNToX(item.box) + " " +
                                   "  " + YNToX(item.manual) + " " +
                                   "  " + YNToX(item.other) + " " +
                                   "   ")
                    verbose = str(item.id)[0:idWidth].ljust(idWidth) + item.platform[0:platformWidth].ljust(platformWidth) + verboseAttr + item.notes[0:notesWidth].ljust(notesWidth)

                if filterData.listDetails:
                    details = verbose + item.region.ljust(2) + "  " + item.date + "  " + format(item.price, ".2f").rjust(7) + " "

                itemTextLen = CONSOLE_COLUMNS-len(details)

                if filterData.listVerbose and totalCount == 0:
                    consoleLine("  Title".ljust(itemTextLen) + "ID".ljust(idWidth) + "Platform".ljust(platformWidth) + "  C   B   M   O    " + "Notes".ljust(notesWidth) + "RE  " + "Date".ljust(10) + "  " + "Price".rjust(7) + " ")
                    consoleLine("  " + "─" * (CONSOLE_COLUMNS-3) + " ")

                if sectionChange(item, lastItem, filterData.groupItems) and totalCount > 0:
                    printItemSum(getSectionTitle(lastItem, filterData.groupItems) + " total: ", sectionPrice, sectionCount, filterData.listDetails)
                    consoleLine()
                    sectionSumPrinted = True
                    sectionPrice      = 0.0
                    sectionCount      = 0

                if totalCount > 0 and filterData.itemLines:
                    consoleLine("  " + "─" * (CONSOLE_COLUMNS-3) + " ")

                consoleLine((("  - " + item.name)[0:itemTextLen-2] + "  ").ljust(itemTextLen) + details)

                totalPrice   += item.price
                totalCount   += 1
                sectionPrice += item.price
                sectionCount += 1

                lastItem = item

        if sectionSumPrinted:
            printItemSum(getSectionTitle(lastItem, filterData.groupItems) + " total: ", sectionPrice, sectionCount, filterData.listDetails)
            consoleLine()

        if filterData.listDetails:
            printItemSum("Sum total: ", totalPrice, totalCount, filterData.listDetails, True)

    if noEndLine == False:
        consoleEndBlock()


######################
# printItemSum
# --------------------
def printItemSum(text, price, count, showPrice, printAverage = False):
    itemsString   = ""
    sumString     = ""
    averageString = ""
    sections      = 2
    priceFormated = format(price, ".2f")

    # Item count
    itemsString = "    " + str(count) + " item" + ("s" if count > 1 else "")

    # Sum and average
    if showPrice == True:
        consoleLine(("─" * len(priceFormated) + " ").rjust(CONSOLE_COLUMNS))

        if printAverage:
            if count > 0:
                averageString = "Average price: " + format(price/count, ".2f")

        sumString = text + "  " + priceFormated + " "
    else:
        consoleLine()

    # Split available width in multiple section
    if printAverage:
        sections += 1

    sectionLen    = int(CONSOLE_COLUMNS/sections)
    sectionLenSum = CONSOLE_COLUMNS - (sectionLen * (sections-1))

    consoleLine(itemsString.ljust(sectionLen) + (averageString.center(sectionLen) if len(averageString) else "") + sumString.rjust(sectionLenSum))



######################
# itemFilterValid
# --------------------
def itemFilterValid(item, itemFilter, itemFilterValue):
    if itemFilterValue == "all":
        return True
    if itemFilterValue == "platform":
        return item.platform.lower() == itemFilter.lower()
    if itemFilterValue == "platform-right":
        return item.platform[-len(itemFilter):len(item.platform)].lower() == itemFilter.lower()
    if itemFilterValue == "platform-left":
        return item.platform[0:len(itemFilter)].lower() == itemFilter.lower()
    if itemFilterValue == "year":
        return item.date[0:4] == itemFilter
    if itemFilterValue == "month":
        return item.date[0:7] == itemFilter
    if itemFilterValue == "day":
        return item.date == itemFilter


######################
# sectionChange
# --------------------
def sectionChange(item, lastItem, group):

    if group == "year" and item.date[0:4] != lastItem.date[0:4]:
        return True

    if group == "month" and item.date[0:7] != lastItem.date[0:7]:
        return True

    if group == "day" and item.date != lastItem.date:
        return True

    if group == "region" and item.region != lastItem.region:
        return True

    if group == "name" and item.name != lastItem.name:
        return True

    if group == "platform" and item.platform != lastItem.platform:
        return True


######################
# getCategoryTitle
# --------------------
def getCategoryTitle(text, filterData):
    title = text

    if len(filterData.itemFilter):
        title += " [Item: " + filterData.itemFilter + "]"

    if len(filterData.platformFilter):
        title += " [Platform: " + filterData.platformFilter + "]"

    if len(filterData.regionFilter):
        title += " [Region: " + filterData.regionFilter + "]"

    return title


######################
# YNToX
# --------------------
def YNToX(yn):
    yn = yn.lower()

    if yn == "yes":
        return "X"
    else:
        return " "


######################
# outputLine
# --------------------
def outputLine(line = ""):
    global textOutput
    textOutput += line + "\n"
    print(line)


######################
# consoleStartBlock
# --------------------
def consoleStartBlock(title = ""):
    outputLine(" ┌" + ("─" + title[0:CONSOLE_COLUMNS]).ljust(CONSOLE_COLUMNS, "─") + "┐ ")
    consoleLine()


######################
# consoleEndBlock
# --------------------
def consoleEndBlock():
    consoleLine()
    outputLine(" └" + "─" * (CONSOLE_COLUMNS) + "┘")


######################
# consoleMidBlock
# --------------------
def consoleMidBlock(title = ""):
    outputLine(" ├" + ("─" + title[0:CONSOLE_COLUMNS]).ljust(CONSOLE_COLUMNS, "─") + "┤ ")
    consoleLine()


######################
# consoleLine
# --------------------
def consoleLine(text = ""):
    outputLine(" │" + text[0:CONSOLE_COLUMNS].ljust(CONSOLE_COLUMNS) + "│ ")


######################
# drawTimeGraph
# --------------------
def drawTimeGraph(title, attribute, group, units, groupData, mode, graphStyle, stepSize = 0, noEndLine = False, addUp = False, includeZero = False):
    unitsOfGroup           = {}
    rows                   = {}
    highestUnit            = DataTotal()
    lowestUnit             = DataTotal()
    startUnit              = ""
    endUnit                = ""
    unitCount              = 0
    totalSum               = 0.0
    graphPadding           = 3

    if len(graphStyle) == 0:
        graphStyle = "outline"

    # Check if group is valid
    if mode != "total" and len(group[0:4]) and int(group[0:4]) == 0:
        if noEndLine == False:
            consoleEndBlock()
            return

    # Init mode
    if mode == "total":
        groupLen      = 0
        unitLen       = 4
        if len(groupData.first.date):
            startRange = int(groupData.first.date[0:4])
        else:
            startRange = 0
        if len(groupData.last.date):
            endRange   = int(groupData.last.date[0:4])
        else:
            endRange   = 0
        unitPartLen   =  4
    if mode == "year":
        groupLen      =  4
        unitLen       =  7
        startRange    =  1
        endRange      = 12
        unitPartLen   =  2
    if mode == "month":
        groupLen      =  7
        unitLen       = 10
        startRange    =  1
        endRange      = 31
        unitPartLen   =  2

    # Generate dummy entries
    for i in range(startRange, endRange+1):
        unitsOfGroup[group + ("-" if len(group) else "") + format(i, "02")] = DataTotal()

    if includeZero:
        unitsOfGroup[group + ("-" if len(group) else "") + "0" * unitPartLen] = DataTotal()

    # Find units for each group
    for unit, data in sorted(unitsOfGroup.items()):
        currentGroup = unit[0:groupLen]
        currentUnit  = unit[-unitPartLen:len(unit)]

        # Ignore invalid units
        if int(currentUnit) == 0 and includeZero != True:
            continue

        # Include all data that belongs to the current group
        if currentGroup == group:
            if unit in units.keys():
                unitsOfGroup[unit] = units[unit]

            endUnit   = unit
            unitCount += 1
            totalSum  += getattr(unitsOfGroup[unit], attribute)

            if addUp:
                setattr(unitsOfGroup[unit], attribute, totalSum)

            if len(startUnit) == 0:
                startUnit = unit

            # Find highest output
            # to calculate upper limit
            if getattr(unitsOfGroup[unit], attribute) > getattr(highestUnit, attribute):
                highestUnit = unitsOfGroup[unit]

            # Find lowest output
            if (getattr(unitsOfGroup[unit], attribute) > 0 and getattr(unitsOfGroup[unit], attribute) < getattr(lowestUnit, attribute)) or getattr(lowestUnit, attribute) == 0:
                lowestUnit  = unitsOfGroup[unit]

        if currentGroup > group:
            break

    # Calculate required whidth for y-axis labels
    yCaptionWidth = max(len(str(int(getattr(highestUnit, attribute)))), len(str(stepSize))) + 1

    # Check whether screen is wide enough to draw the graph
    # Min width per bar = 2
    if (endRange - startRange + 1) * 2 > CONSOLE_COLUMNS-(yCaptionWidth+(graphPadding*2)):
        consoleMidBlock("GRAPH ERROR")
        consoleLine(" - not enough screen width to draw graph")
        if noEndLine == False:
            consoleEndBlock()
        return

    # Calculate max number of units
    maxUnits = endRange - startRange + 1

    # Calculate graph bar with
    outerBarWidth = int((CONSOLE_COLUMNS-(yCaptionWidth+(graphPadding*2)))/maxUnits)
    barWidth      = outerBarWidth - 2

    # Check whether a valid unit range was found
    if len(startUnit) == 0 or len(endUnit) == 0:
        if noEndLine == False:
            consoleEndBlock()
        return

    # Calculate upper limit for the graph
    upperBound = int(math.ceil(getattr(highestUnit, attribute) / 10.0)) * 10

    # Calculate step size
    if stepSize == 0:
        if len(str(int(getattr(highestUnit, attribute)))) == 1:
            stepSize = 1
        else:
            stepSize = int(int(10 ** (len(str(int(getattr(highestUnit, attribute))))-1))/5)

        # Making sure the step size isnt too fine
        if upperBound / stepSize > 20:
            stepSize = int(upperBound/20)

    # Making sure the upper limit fits the step size
    if upperBound % stepSize != 0:
        # Extend limit so it can be devided cleanly by the step size
        upperBound += stepSize - (upperBound % stepSize)

    # Calculate the lower limit for the meta data
    lowerBound = (stepSize*-1)-1

    # Init data list
    for i in range(upperBound, lowerBound, stepSize*-1):
        rows[i] = ""

    # Make room for axis label in list
    rows[(stepSize*-2)] = ""

    # Contruct graph row-wise
    for unit, data in sorted(unitsOfGroup.items()):
        b = False

        for i in range(upperBound, lowerBound, stepSize*-1):

            if i < 0:
                # X-axis labels
                if mode == "total":
                    unitDescription = translateGraphUnit(unit[groupLen:len(unit)], mode, barWidth)
                else:
                    unitDescription = translateGraphUnit(unit[groupLen+1:len(unit)], mode, barWidth)

                if len(unitDescription) <= barWidth:
                    rows[i] += unitDescription.center(outerBarWidth)
                else:
                    if len(unitDescription) / 2 <= barWidth:
                        # When the label fits in two rows
                        rows[i]             += unitDescription[0:max(barWidth, 1)].center(outerBarWidth)
                        rows[i+stepSize*-1] += unitDescription[max(barWidth, 1):max(barWidth, 1)+max(barWidth, 1)].center(outerBarWidth)
                    else:
                        # When the label doesnt fit in two rows
                        # only print the last two characters
                        rows[i]             += unitDescription[-2:-1].center(outerBarWidth)
                        rows[i+stepSize*-1] += unitDescription[-1:len(unitDescription)].center(outerBarWidth)
            else:
                # Graph lines
                if getattr(data, attribute) <= i and getattr(data, attribute) > i - stepSize and getattr(data, attribute) != 0:
                    if graphStyle == "outline":
                        rows[i] += "┌"+"─"*barWidth+"┐"
                    if graphStyle == "fill":
                        rows[i] += "█"*outerBarWidth
                    b = True
                else:
                    if b:
                        if graphStyle == "outline":
                            if i == 0:
                                rows[i] += "┘"+" "*barWidth+"└"
                            else:
                                rows[i] += "│"+" "*barWidth+"│"
                        if graphStyle == "fill":
                            rows[i] += "█"*outerBarWidth
                    else:
                        if i == 0:
                            if graphStyle == "outline":
                                rows[i] += "─"+"─"*barWidth+"─"
                            if graphStyle == "fill":
                                rows[i] += "█"*outerBarWidth
                        else:
                            rows[i] += " "+" "*barWidth+" "

    # Print graph
    consoleLine()
    consoleMidBlock(title)

    for row, data in rows.items():
        if row < 0:
            # Print x-axis labels
            if len(data):
                consoleLine(" " * (graphPadding + yCaptionWidth) + data)
        else:
            # Print graph
            consoleLine(" " + str(row).rjust(yCaptionWidth-1) + " " * graphPadding + data)

    consoleLine()
    consoleLine("  - Lowest: " + format(getattr(lowestUnit, attribute), " .2f") + " (" + lowestUnit.first.date[0:unitLen].rjust(unitPartLen, "0") + ")" +
                "  - Highest: " + format(getattr(highestUnit, attribute), ".2f") + " (" + highestUnit.first.date[0:unitLen].rjust(unitPartLen, "0") + ")" +
                "  - Average: " + format(getattr(groupData, attribute)/unitCount, ".2f"))
    if noEndLine == False:
        consoleEndBlock()


######################
# translateGraphUnit
# --------------------
def translateGraphUnit(unit, mode, maxWidth):
    if mode == "year":

        short = {
            "01": "JA", "02": "FE", "03": "MR",
            "04": "AP", "05": "MY", "06": "JN",
            "07": "JL", "08": "AU", "09": "SE",
            "10": "OC", "11": "NV", "12": "DE"
        }

        long = {
            "01": "January", "02": "February", "03": "March",
            "04": "April"  , "05": "May"     , "06": "June",
            "07": "July"   , "08": "August"  , "09": "September",
            "10": "October", "11": "November", "12": "December"
        }

        if maxWidth >= 9:
            return long.get(unit)
        if maxWidth >= 3:
            return long.get(unit)[0:3]
        else:
            return short.get(unit)

    return unit


######################
# searchListInString
# --------------------
def searchListInString(list, string, exact = False):
    for item in list:
        if exact == True:
            if item.lower().strip() == string.lower().strip():
                return True
        else:
            if re.search(item.lower().strip(), string.lower()) != None:
                return True

    return False


######################
# searchStringInList
# --------------------
def searchStringInList(string, list):
    for item in list:
        if item.lower() == string.lower():
            return True

    return False


######################
# getSectionTitle
# --------------------
def getSectionTitle(lastItem, group):

    if group == "year":
        return lastItem.date[0:4]

    if group == "month":
        return lastItem.date[0:7]

    if group == "day":
        return lastItem.date

    if group == "region":
        return lastItem.region

    if group == "name":
        return lastItem.name

    if group == "platform":
        return lastItem.platform

    return ""


######################
# printHelp
# --------------------
def printHelp():
    global options

    print()
    print("  Usage: VGC_Analyze.py <options> <categories>")
    print()
    print("  Options")

    for option in options:
        helpString = "    "

        if len(option["short"]):
            helpString += "-" + option["short"]
            if option["argument"]:
                helpString += " <" + option["descriptionValue"] + ">"
        if len(option["short"]) and len(option["long"]):
            helpString += "\n    "
        if len(option["long"]):
            helpString += "--" + option["long"]
            if option["argument"]:
                helpString += "=<" + option["descriptionValue"] + ">"
        if len(helpString):
            helpString += "\n"
            helpString += "         " + option["description"].replace("\n", "\n         ")

        if len(helpString.strip()):
            print(helpString + "\n")

    print()
    print("  Categories")
    print("    - Platforms: (wii, switch, playstation, ...)")
    print("    - Generic: (collection, hardware, accessories, totals)")
    print("    - Years: (2020, 1995, 2003, ...)")
    print("    - Months: (2020-12, 1995-03, 2003-07, ...)")
    print("    - Days: (2020-12-25, 1995-03-17, 2003-07-11, ...)")
    print()
    print("    All given arguments without leading - or -- are treated as category names to search for")
    print()
    print("    Categories are based on VGC-Categories")
    print("    Additional categories (e.g. yearly totals) are generated during execution")
    print()
    print("    Example")
    print("      View Playstation 2 categories")
    print("      > VGC_Analyze.py \"playstation 2\"")
    print()
    print("    Run \"--categories\" for possible categories")
    print("      - Individual days are only listed when --categories-days is stated")
    print()
    print("    Multiple categories can be queried simultaneously")
    print()
    print("    Example")
    print("      > VGC_Analyze.py 2020 2020-06 2019 2018 \"wii u\"")
    print()
    print("    Categories support RegEx and quotation marks for exact results")
    print("      - e.g. \"playstation 2$\"")
    print()
    print("  Custom queries")
    print("    Categories are ignored when the -c or --custom option is given")
    print("    By default VGC_Analyze lists all data organized in categories")
    print("    Using the -c option creates a custom query including all results in a single category")
    print()
    print("    Example")
    print("      Custom query to lists all items with missing prices")
    print("      > VGC_Analyze.py -idc --price-less=0")
    print()
    print("  Regular Expressions (RegEx)")
    print("    Python style RegEx can be used with various options")
    print("    Compatible options are marked above")
    print("    Visit https://www.w3schools.com/python/python_regex.asp for details about Python RegEx")
    print()
    print("    Example")
    print("      View all items that start with \"Y\" and end with \"n\"")
    print("      > VGC_Analyze.py -idc -n \"^Y.*n$\"")
    print()
    print("  Filters")
    print("    Filters limit what data is analyzed")
    print("    Filters apply to categories as well as custom queries")
    print()
    print("    Example")
    print("      > VGC_Analyze.py -i --date-after=2016 --date-before=2016 \"xbox 360\" ")
    print("      > VGC_Analyze.py -i --item-platform=\"xbox 360\" 2016")
    print("      > VGC_Analyze.py -i --custom --item-platform=\"xbox 360\" --date-after=2016 --date-before=2016")
    print("      These three statements would analyze the same data but depict the results slightly differently")
    print()
    print("  Graphs")
    print("    All date-based categories as well as totals and custom queries will draw graphs by default")
    print("    The specific graph that is drawn depends on the context")
    print()
    print("      \"Collection totals\" will draw four different graphs")
    print("        - Yearly spending")
    print("        - Yearly items")
    print("        - Collection growth (value)")
    print("        - Collection growth (items)")
    print("        Example")
    print("          > VGC_Analyze.py collection")
    print()
    print("      Year-Categories will draw two graphs depicting monthly spending and monthly item count")
    print("        Example")
    print("          > VGC_Analyze.py 2020")
    print()
    print("      Month-Categories will draw two graphs depicting daily spending and daily item count")
    print("        Example")
    print("          > VGC_Analyze.py 2020-12")
    print()
    print("      Custom queries will draw two graphs depicting spending and item count based on the query result")
    print("      The depicted range (yearly, monthly, daily) depends on the date-range of the query result")
    print("        Example")
    print("          > VGC_Analyze.py -c --date-after=2012 --date-before=2018")
    print()
    print("    Graphs can be disabled with the --graph-hide option")
