from VGC_Locale import _

FILE_PREFIX             = "collection-"

DATA_PATH               = "./data/"
SETTINGS_PATH           = DATA_PATH + "settings/"
LOCAL_DATA              = DATA_PATH + "local/"
DOWNLOAD_PATH           = DATA_PATH
DOWNLOAD_FILE           = DOWNLOAD_PATH + FILE_PREFIX + "VGC-Analyze-Download.csv"
LOCAL_DATA_FILE         = LOCAL_DATA + "VGC-Local-Data.json"
PLATFORM_KEYWORDS_FILE  = LOCAL_DATA + "VGC-Platform-Keywords.json"

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

# IMG Vars
IMG_PATH         = "./img/"
ICON_PATH        = IMG_PATH + "icons/"
IMG_CACHE_PATH   = IMG_PATH + "cache/"
IMG_CACHE_FRONT  = IMG_CACHE_PATH + "front/"
IMG_CACHE_BACK   = IMG_CACHE_PATH + "back/"
IMG_CACHE_CART   = IMG_CACHE_PATH + "cart/"
IMG_COVER_NONE   = IMG_PATH + "cover_placeholder.jpg"
COVER_WIDTH      = 120

# Graph vars
GRAPH_TYPE_BAR                  = _("Bar")
GRAPH_TYPE_PIE                  = _("Pie")
GRAPH_TYPE_AREA                 = _("Area")
GRAPH_TYPE_LINE                 = _("Line")

GRAPH_CONTENT_YEARS             = _("Years")
GRAPH_CONTENT_MONTHS            = _("Months")
GRAPH_CONTENT_PLATFORMS         = _("Platforms")
GRAPH_CONTENT_REGIONS           = _("Regions")
GRAPH_CONTENT_PLATFORM_HOLDERS  = _("Platform holders")

GRAPH_BAR_COLOR        = "#FFD754"
GRAPH_BAR_COLOR_ACTIVE = "#547CFF"

GRAPH_DATA_ITEMCOUNT        = _("Item count")
GRAPH_DATA_TOTALPRICE       = _("Total price")
GRAPH_DATA_ITEMCOUNTGROWTH  = _("Item count (growth)")
GRAPH_DATA_TOTALPRICEGROWTH = _("Total price (growth)")

GROUP_BY_YEAR           = _("year")
GROUP_BY_MONTH          = _("month")
GROUP_BY_DAY            = _("day")
GROUP_BY_NAME           = _("name")
GROUP_BY_REGION         = _("region")
GROUP_BY_PLATFORM       = _("platform")
GROUP_BY_PLATFORMHOLDER = _("platform holder")
GROUP_BY_NOTES          = _("notes")

ORDER_BY_NAME     = _("name")
ORDER_BY_PRICE    = _("price")
ORDER_BY_DATE     = _("date")
ORDER_BY_REGION   = _("region")
ORDER_BY_PLATFORM = _("platform")
ORDER_BY_NOTES    = _("notes")

ORDER_DIRECTION_ASCENDING  = _("ascending")
ORDER_DIRECTION_DESCENDING = _("descending")

ITEM_ATTRIBUTE_YES = _("Yes")
ITEM_ATTRIBUTE_NO  = _("No")