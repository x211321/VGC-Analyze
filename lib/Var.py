import platform

from lib.Path import *
from lib.Locale import _


# Colors
BUTTON_COLOR_DEFAULT     = "white"
BUTTON_COLOR_HOVER       = "#E5F1FB"
BUTTON_COLOR_PRESSED     = "#CCE4F7"
BUTTON_COLOR_TOGGLED     = "#FFDD99"
BUTTON_COLOR_CONFIRM     = "#BDF593"
BUTTON_COLOR_CANCEL      = "#F59398"
BUTTON_COLOR_TOGGLE      = "#FFA90D"
LABEL_COLOR_WARN_TEXT    = "red"

MENU_BG_HOVER = "#0078D7"
MENU_FG_HOVER = "white"

if platform.system() == "Darwin":
    GUI_COLOR_PRIMARY    = "white"
    GUI_COLOR_SECONDARY  = "white"
else:
    GUI_COLOR_PRIMARY    = "white"
    GUI_COLOR_SECONDARY  = "#F0F0F0"

GUI_COLOR_WARNING = "#FF9999"

FRAME_STYLE_PRIMARY   = "frame_primary.TFrame"
FRAME_STYLE_SECONDARY = "frame_secondary.TFrame"

LABEL_STYLE_PRIMARY             = "label_primary.TLabel"
LABEL_STYLE_SECONDARY           = "label_secondary.TLabel"
LABEL_STYLE_WARNING             = "label_warning.TLabel"
LABEL_STYLE_WARN_TEXT_PRIMARY   = "label_warn_text_primary.TLabel"
LABEL_STYLE_WARN_TEXT_SECONDARY = "label_warn_text_secondary.TLabel"
LABEL_STYLE_LINK_PRIMARY        = "label_link_primary.TLabel"
LABEL_STYLE_LINK_SECONDARY      = "label_link_secondary.TLabel"

LABEL_STYLE_CAL_PRIMARY         = "label_cal_primary.TLabel"
LABEL_STYLE_CAL_SECONDARY       = "label_cal_secondary.TLabel"
LABEL_STYLE_CAL_HIGH_PRIMARY    = "label_cal_high_primary.TLabel"
LABEL_STYLE_CAL_HIGH_SECONDARY  = "label_cal_high_secondary.TLabel"
LABEL_STYLE_CAL_SELECTED        = "label_cal_selected.TLabel"

LABELBUTTON_STYLE         = "labelbutton.TLabel"
LABELBUTTON_STYLE_DEFAULT = "default." + LABELBUTTON_STYLE
LABELBUTTON_STYLE_HOVER   = "hover."   + LABELBUTTON_STYLE
LABELBUTTON_STYLE_PRESSED = "pressed." + LABELBUTTON_STYLE
LABELBUTTON_STYLE_TOGGLED = "toggled." + LABELBUTTON_STYLE
LABELBUTTON_STYLE_CONFIRM = "confirm." + LABELBUTTON_STYLE
LABELBUTTON_STYLE_CANCEL  = "cancel."  + LABELBUTTON_STYLE

CHECKBOX_STYLE_PRIMARY   = "checkbox_style_primary.TCheckbutton"
CHECKBOX_STYLE_SECUNDARY = "checkbox_style_secundary.TCheckbutton"

CAL_COLOR_PRIMARY        = "#EEEEEE"
CAL_COLOR_SECONDARY      = "#DDDDDD"
CAL_COLOR_HIGH_PRIMARY   = "#FFDD99"
CAL_COLOR_HIGH_SECONDARY = "#FFE2A8"
CAL_COLOR_SELECTED       = "#FFBF40"

GRAPH_BAR_COLOR          = "#FFD754"
GRAPH_BAR_COLOR_ACTIVE   = "#547CFF"

INPUT_COLOR              = "white"


# Categories
CAT_HARDWARE     = "Hardware"
CAT_ACCESSORY    = "Accessory"
CAT_ACCESSORIES  = "Accessories"


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

GRAPH_DATA_ITEMCOUNT        = _("Item count")
GRAPH_DATA_TOTALPRICE       = _("Total price")
GRAPH_DATA_ITEMCOUNTGROWTH  = _("Item count (growth)")
GRAPH_DATA_TOTALPRICEGROWTH = _("Total price (growth)")


# Group by
GROUP_BY = {}

GROUP_BY_YEAR           = "year (purchased)"
GROUP_BY_MONTH          = "month (purchased)"
GROUP_BY_DAY            = "day (purchased)"
GROUP_BY_YEAR_ADDED     = "year (added)"
GROUP_BY_MONTH_ADDED    = "month (added)"
GROUP_BY_DAY_ADDED      = "day (added)"
GROUP_BY_NAME           = "name"
GROUP_BY_REGION         = "region"
GROUP_BY_PLATFORM       = "platform"
GROUP_BY_PLATFORMHOLDER = "platform holder"
GROUP_BY_NOTES          = "notes"
GROUP_BY_VGCID          = "VGC ID"

GROUP_BY[GROUP_BY_YEAR          ] = _(GROUP_BY_YEAR          )
GROUP_BY[GROUP_BY_MONTH         ] = _(GROUP_BY_MONTH         )
GROUP_BY[GROUP_BY_DAY           ] = _(GROUP_BY_DAY           )
GROUP_BY[GROUP_BY_YEAR_ADDED    ] = _(GROUP_BY_YEAR_ADDED    )
GROUP_BY[GROUP_BY_MONTH_ADDED   ] = _(GROUP_BY_MONTH_ADDED   )
GROUP_BY[GROUP_BY_DAY_ADDED     ] = _(GROUP_BY_DAY_ADDED     )
GROUP_BY[GROUP_BY_NAME          ] = _(GROUP_BY_NAME          )
GROUP_BY[GROUP_BY_REGION        ] = _(GROUP_BY_REGION        )
GROUP_BY[GROUP_BY_PLATFORM      ] = _(GROUP_BY_PLATFORM      )
GROUP_BY[GROUP_BY_PLATFORMHOLDER] = _(GROUP_BY_PLATFORMHOLDER)
GROUP_BY[GROUP_BY_NOTES         ] = _(GROUP_BY_NOTES         )
GROUP_BY[GROUP_BY_VGCID         ] = _(GROUP_BY_VGCID         )



# Order by
ORDER_BY = {}

ORDER_BY_NAME       = "name"
ORDER_BY_PRICE      = "price"
ORDER_BY_DATE       = "date (purchased)"
ORDER_BY_DATE_ADDED = "date (added)"
ORDER_BY_REGION     = "region"
ORDER_BY_PLATFORM   = "platform"
ORDER_BY_NOTES      = "notes"

ORDER_BY[ORDER_BY_NAME      ] = _(ORDER_BY_NAME      )
ORDER_BY[ORDER_BY_PRICE     ] = _(ORDER_BY_PRICE     )
ORDER_BY[ORDER_BY_DATE      ] = _(ORDER_BY_DATE      )
ORDER_BY[ORDER_BY_DATE_ADDED] = _(ORDER_BY_DATE_ADDED)
ORDER_BY[ORDER_BY_REGION    ] = _(ORDER_BY_REGION    )
ORDER_BY[ORDER_BY_PLATFORM  ] = _(ORDER_BY_PLATFORM  )
ORDER_BY[ORDER_BY_NOTES     ] = _(ORDER_BY_NOTES     )


# Order direction
ORDER_DIRECTION = {}

ORDER_DIRECTION_ASCENDING  = "ascending"
ORDER_DIRECTION_DESCENDING = "descending"

ORDER_DIRECTION[ORDER_DIRECTION_ASCENDING ] = _(ORDER_DIRECTION_ASCENDING )
ORDER_DIRECTION[ORDER_DIRECTION_DESCENDING] = _(ORDER_DIRECTION_DESCENDING)


# Attribute Yes / No
ATTRIBUTE_YN = {}

ATTRIBUTE_YES = "Yes"
ATTRIBUTE_NO  = "No"

ATTRIBUTE_YN[ATTRIBUTE_YES] = _(ATTRIBUTE_YES)
ATTRIBUTE_YN[ATTRIBUTE_NO]  = _(ATTRIBUTE_NO)


# Treeview columns
VIEW_COLUMNS = {}

VIEW_COLUMNS["Title"]            = {"name": _("Title")           , "anchor": "w", "type": None , "grouptype": int  , "width": 200}
VIEW_COLUMNS["Platform"]         = {"name": _("Platform")        , "anchor": "w", "type": None , "grouptype": None , "width": 100}
VIEW_COLUMNS["Region"]           = {"name": _("Region")          , "anchor": "w", "type": None , "grouptype": None , "width":  30}
VIEW_COLUMNS["Price"]            = {"name": _("Price")           , "anchor": "e", "type": float, "grouptype": float, "width":  50}
VIEW_COLUMNS["Date (purchased)"] = {"name": _("Date (purchased)"), "anchor": "w", "type": None , "grouptype": None , "width":  50}
VIEW_COLUMNS["Date (added)"]     = {"name": _("Date (added)")    , "anchor": "w", "type": None , "grouptype": None , "width":  50}
VIEW_COLUMNS["Cart"]             = {"name": _("Cart")            , "anchor": "w", "type": None , "grouptype": None , "width":  30}
VIEW_COLUMNS["Box"]              = {"name": _("Box")             , "anchor": "w", "type": None , "grouptype": None , "width":  30}
VIEW_COLUMNS["Manual"]           = {"name": _("Manual")          , "anchor": "w", "type": None , "grouptype": None , "width":  30}
VIEW_COLUMNS["Other"]            = {"name": _("Other")           , "anchor": "w", "type": None , "grouptype": None , "width":  30}
VIEW_COLUMNS["Bookmark"]         = {"name": _("Bookmark")        , "anchor": "w", "type": None , "grouptype": None , "width":  30}
VIEW_COLUMNS["Finished"]         = {"name": _("Finished")        , "anchor": "w", "type": None , "grouptype": None , "width":  30}
VIEW_COLUMNS["Notes"]            = {"name": _("Notes")           , "anchor": "w", "type": None , "grouptype": None , "width": 100}


# Templates
TEMPLATE_CURRENT_CONFIG = _("[current configuration]")

# Icons
MIN_ICON_WIDTH  = 15
MIN_ICON_HEIGHT = 15
