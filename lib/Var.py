from lib.Locale import _

FILE_PREFIX             = "collection-"

DATA_PATH               = "./data/"
EXPORT_PATH             = "./export/"
LOCAL_DATA              = DATA_PATH + "local/"
DOWNLOAD_PATH           = DATA_PATH
DOWNLOAD_FILE           = DOWNLOAD_PATH + FILE_PREFIX + "VGC-Analyze-Download.csv"
LOCAL_DATA_FILE         = LOCAL_DATA + "VGC-Local-Data.json"

# Colors
BUTTON_COLOR_GOOD = "#BDF593"
BUTTON_COLOR_BAD  = "#F59398"

GUI_COLOR_PRIMARY   = "white"
GUI_COLOR_SECONDARY = "#F0F0F0"

INPUT_COLOR = "white"

# Categories
CAT_HARDWARE     = "Hardware"
CAT_ACCESSORY    = "Accessory"
CAT_ACCESSORIES  = "Accessories"

# Img vars
IMG_PATH         = "./img/"
IMG_CACHE_PATH   = IMG_PATH + "cache/"
IMG_CACHE_FRONT  = IMG_CACHE_PATH + "front/"
IMG_CACHE_BACK   = IMG_CACHE_PATH + "back/"
IMG_CACHE_CART   = IMG_CACHE_PATH + "cart/"
COVER_WIDTH      = 120

# Asset vars
ASSETS_PATH      = "./assets/"
ICON_PATH        = ASSETS_PATH + "icons/"
IMG_COVER_NONE   = ASSETS_PATH + "cover_placeholder.jpg"

# Graph vars
GRAPH_TYPE_BAR                  = _("Bar")
GRAPH_TYPE_PIE                  = _("Pie")
GRAPH_TYPE_AREA                 = _("Area")
GRAPH_TYPE_LINE                 = _("Line")

GRAPH_CONTENT_YEARS             = _("Years (purchased)")
GRAPH_CONTENT_MONTHS            = _("Months (purchased)")
GRAPH_CONTENT_YEARS_ADDED       = _("Years (added)")
GRAPH_CONTENT_MONTHS_ADDED      = _("Months (added)")
GRAPH_CONTENT_PLATFORMS         = _("Platforms")
GRAPH_CONTENT_REGIONS           = _("Regions")
GRAPH_CONTENT_PLATFORM_HOLDERS  = _("Platform holders")

GRAPH_BAR_COLOR        = "#FFD754"
GRAPH_BAR_COLOR_ACTIVE = "#547CFF"

GRAPH_DATA_ITEMCOUNT        = _("Item count")
GRAPH_DATA_TOTALPRICE       = _("Total price")
GRAPH_DATA_ITEMCOUNTGROWTH  = _("Item count (growth)")
GRAPH_DATA_TOTALPRICEGROWTH = _("Total price (growth)")

# Group by
GROUP_BY_YEAR           = _("year (purchased)")
GROUP_BY_MONTH          = _("month (purchased)")
GROUP_BY_DAY            = _("day (purchased)")
GROUP_BY_YEAR_ADDED     = _("year (added)")
GROUP_BY_MONTH_ADDED    = _("month (added)")
GROUP_BY_DAY_ADDED      = _("day (added)")
GROUP_BY_NAME           = _("name")
GROUP_BY_REGION         = _("region")
GROUP_BY_PLATFORM       = _("platform")
GROUP_BY_PLATFORMHOLDER = _("platform holder")
GROUP_BY_NOTES          = _("notes")

# Order by
ORDER_BY_NAME       = _("name")
ORDER_BY_PRICE      = _("price")
ORDER_BY_DATE       = _("date (purchased)")
ORDER_BY_DATE_ADDED = _("date (added)")
ORDER_BY_REGION     = _("region")
ORDER_BY_PLATFORM   = _("platform")
ORDER_BY_NOTES      = _("notes")

# Order direction
ORDER_DIRECTION_ASCENDING  = _("ascending")
ORDER_DIRECTION_DESCENDING = _("descending")

ITEM_ATTRIBUTE_YES = _("Yes")
ITEM_ATTRIBUTE_NO  = _("No")

# Treeview columns
VIEW_COLUMNS = {}

VIEW_COLUMNS["Title"]            = {"name": _("Title")           , "anchor": "w", "type": None , "width": 200}
VIEW_COLUMNS["Platform"]         = {"name": _("Platform")        , "anchor": "w", "type": None , "width": 100}
VIEW_COLUMNS["Region"]           = {"name": _("Region")          , "anchor": "w", "type": None , "width":  30}
VIEW_COLUMNS["Price"]            = {"name": _("Price")           , "anchor": "e", "type": float, "width":  50}
VIEW_COLUMNS["Date (purchased)"] = {"name": _("Date (purchased)"), "anchor": "w", "type": None , "width":  50}
VIEW_COLUMNS["Date (added)"]     = {"name": _("Date (added)")    , "anchor": "w", "type": None , "width":  50}
VIEW_COLUMNS["Cart"]             = {"name": _("Cart")            , "anchor": "w", "type": None , "width":  30}
VIEW_COLUMNS["Box"]              = {"name": _("Box")             , "anchor": "w", "type": None , "width":  30}
VIEW_COLUMNS["Manual"]           = {"name": _("Manual")          , "anchor": "w", "type": None , "width":  30}
VIEW_COLUMNS["Other"]            = {"name": _("Other")           , "anchor": "w", "type": None , "width":  30}
VIEW_COLUMNS["Bookmark"]         = {"name": _("Bookmark")        , "anchor": "w", "type": None , "width":  30}
VIEW_COLUMNS["Finished"]         = {"name": _("Finished")        , "anchor": "w", "type": None , "width":  30}
VIEW_COLUMNS["Notes"]            = {"name": _("Notes")           , "anchor": "w", "type": None , "width": 100}

