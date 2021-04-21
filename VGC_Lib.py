
import sys
import getopt

from VGC_Data       import FilterData
from VGC_Data       import options
from VGC_Data       import guessDate
from VGC_Print      import setScreenWidth
from VGC_Print      import printHelp
from VGC_Download   import downloadCollection
from VGC_Browser    import openItemInBrowser


######################
# userInputBool Function
# --------------------
def userInputBool(query, default = True):
    value = input(query)
    
    if default and len(value.strip()) == 0:
        return True
    if value.lower()[0:1] == "y" or value.lower()[0:1] == "j" or value == "1":
        return True
        

######################
# userInputString Function
# --------------------
def userInputString(query, default = ""):
    value = input(query)
    
    if len(value) == 0:
        return default
    else:
        return value


######################
# getArgumentValue Function
# --------------------
def getArgumentValue(argument, argv, default = ""):
    value = getListString(argument, argv)
        
    if len(value.split("=")) > 1:
        value = value.split("=")[1]
        
        if len(value):
            return value
        else:
            return default
    else:
        return default


######################
# getListIndex Function
# --------------------
def getListString(string, list):
    for item in list:
        if item.lower()[0:len(string)] == string.lower():
            return item
    
    return ""
  
    
######################
# stringToYN Function
# --------------------
def stringToYN(s):
    s = s.lower()

    if s == "y" or s == "yes" or s == "j" or s == "1" or s == "true":
        return "Yes"
    else:
        return "No"


######################
# addOption Function
# --------------------
def addOption(short, long, description, descriptionValue = "", argument = False, default = ""):
    option = {}

    option["short"]             = short
    option["long"]              = long
    option["description"]       = description
    option["descriptionValue"]  = descriptionValue
    option["argument"]          = argument
    option["default"]           = default
    
    options.append(option)
    
    
######################
# initOptions Function
# --------------------
def initOptions():
    addOption("h", "help"           , "Show this help screen")
    addOption("",  "interactive"    , "Run VGC_Analyze in interactive-mode (console)")
    addOption("f", "file"           , "File to analyze (optional)\n" + 
                                      "VGC_Analyze will search for latest file in directory", 
                                      "path/to/file.csv", True)
    addOption("i", "items"          , "Show individual items")
    addOption("d", "details"        , "Show item details (purchase date, price)")
    addOption("v", "verbose"        , "Show even more item details")
    addOption("" , "categories"     , "Show all available categories and exit")
    addOption("" , "categories-days", "Include days in category list")
    addOption("c", "custom"         , "Combine all results in one category")
    addOption("", "item-lines"      , "Show horizontal lines between items")
    addOption("" , "price-greater"  , "Only include items with a purchase price greater than", 
                                      "float", True)
    addOption("" , "price-less"     , "Only include items with a purchase price less than", 
                                      "float", True)
    addOption("" , "date-after"     , "Only include items purchased after date", 
                                      "YYYY[-MM][-DD]", True)
    addOption("" , "date-before"    , "Only include items purchased before date", 
                                      "YYYY[-MM][-DD]", True)
    addOption("n", "item-name"      , "Only include items if item name matches filter",
                                      "string/RegEx", True)
    addOption("p", "item-platform"  , "Only include items if item platform matches filter",
                                      "string/RegEx", True)
    addOption("r", "item-region"    , "Only include items if item region matches filter",
                                      "string/RegEx", True)
    addOption("", "item-cart"       , "Only include items if item cart-attribute matches filter",
                                      "y/n", True)
    addOption("", "item-box"        , "Only include items if item box-attribute matches filter",
                                      "y/n", True)
    addOption("", "item-manual"     , "Only include items if item manual-attribute matches filter",
                                      "y/n", True)
    addOption("", "item-other"      , "Only include items if item other-attribute matches filter",
                                      "y/n", True)
    addOption("", "item-notes"      , "Only include items if item notes match filter",
                                      "string/RegEx", True)
    addOption("o", "item-order"     , "Order items by specified attribute",
                                      "[name, price, date, region, platform]:[a, d]", True)
    addOption("g", "item-group"     , "Group items by specified attribute\n" + 
                                      "Combine with -o for best results",
                                      "[year, month, day, name, region, platform]", True)
    addOption("" , "graph-style"    , "Set graph style (default: outline)",
                                      "[outline, fill]", True)
    addOption("" , "graph-steps"    , "Set step size for graphs",
                                      "integer", True)
    addOption("" , "graph-hide"     , "Hide graphs in date-categories")
    addOption("" , "graph-zero"     , "Show \"zero\"-units in graphs\n" + 
                                      "e.g. year 0000 or month 00\n" + 
                                      "those will include data with missing or incomplete dates")
    addOption("" , "screen-width"   , "Set screen width in columns",
                                      "integer", True)
    addOption("" , "open"           , "Open Item in web browser",
                                      "id", True)
    addOption("" , "download"       , "Download current colleciton file from vgcollect.com")
    

######################
# readOptions Function
# --------------------       
def readOptions():
    global options

    filterData = FilterData()

    if len(sys.argv) == 1:
        filterData.guiMode = True
    else:
        shortOptions = ""
        longOption   = ""
        longOptions  = []
        
        
        for option in options:
            longOption = ""

            if len(option["short"]):
                shortOptions += option["short"]
                if option["argument"]:
                    shortOptions += ":"
            if len(option["long"]):
                longOption += option["long"]
                if option["argument"]:
                    longOption += "="
                    
                longOptions.append(longOption)
        
        try:
            opts, args = getopt.gnu_getopt(sys.argv[1:],shortOptions,longOptions)
        except getopt.GetoptError:
            printHelp()
            sys.exit(2)

        for opt, arg in opts:
            if opt in ["", "--interactive"]:
                filterData.interactiveMode      = True
            if opt in ["-n", "--item-name"]:
                filterData.itemFilter           = arg
            if opt in ["-p", "--item-platform"]:
                filterData.platformFilter       = arg
            if opt in ["-r", "--item-region"]:
                filterData.regionFilter         = arg
            if opt in ["", "--item-cart"]:
                filterData.cartFilter           = stringToYN(arg)
            if opt in ["", "--item-box"]:
                filterData.boxFilter            = stringToYN(arg)
            if opt in ["", "--item-manual"]:
                filterData.manualFilter         = stringToYN(arg)
            if opt in ["", "--item-other"]:
                filterData.otherFilter          = stringToYN(arg)
            if opt in ["", "--item-notes"]:
                filterData.notesFilter          = arg
            if opt in ["--price-greater"]:
                filterData.priceFilterStart     = float(arg)
                filterData.priceFilterStartSet  = True
            if opt in ["--price-less"]:
                filterData.priceFilterEnd       = float(arg)
                filterData.priceFilterEndSet    = True
            if opt in ["--date-after"]:
                filterData.dateFilterStart      = guessDate(arg, "start")
            if opt in ["--date-before"]:
                filterData.dateFilterEnd        = guessDate(arg, "end")
            if opt in ["-o", "--item-order"]:
                if ":" in arg:
                    filterData.orderItems       = arg[0:arg.find(":")]
                    filterData.orderItemsReverse= (arg[arg.find(":")+1:len(arg)].lower() == "d")
                else:
                    filterData.orderItems       = arg
            if opt in ["-g", "--item-group"]:
                filterData.groupItems           = arg
            if opt in ["-f", "--file"]:
                if len(filterData.filePath) == 0:
                    filterData.filePath         = arg
            if opt in ["--graph-style"]:
                filterData.graphStyle           = arg
            if opt in ["--graph-steps"]:
                filterData.graphStepSize        = int(arg)
            if opt in ["-c", "--custom"]:
                filterData.skipCategories       = True
            if opt in ["--categories"]:
                filterData.listCategories       = True
            if opt in ["--categories-days"]:
                filterData.listCategoriesDays   = True
            if opt in ["-i", "--items"]:
                filterData.listItems            = True
            if opt in ["-d", "--details"]:
                filterData.listItems            = True
                filterData.listDetails          = True
            if opt in ["-v", "--verbose"]:
                filterData.listItems            = True
                filterData.listDetails          = True
                filterData.listVerbose          = True
            if opt in ["--graph-hide"]:
                filterData.hideGraphs           = True
            if opt in ["--graph-zero"]:
                filterData.graphIncludeZero     = True
            if opt in ["--item-lines"]:
                filterData.itemLines            = True
            if opt in ["--screen-width"]:
                filterData.screenWidth          = int(arg)

            if opt in ["-h", "--help"]:
                # Print help
                printHelp()
                sys.exit()
            if opt in ["--open"]:
                openItemInBrowser(arg)
                sys.exit()
            if opt in ["--download"]:
                downloadCollection(filterData)

        # Read categories
        filterData.categoryFilterList = args
        
        # Set screen width
        if not filterData.guiMode:
            setScreenWidth(filterData.screenWidth)

    # Return settings
    return filterData
            
            


            