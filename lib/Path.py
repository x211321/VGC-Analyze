import os
import sys
import pathlib

FILE_PREFIX = "collection-"

if sys.platform == "win32":
    DATA_PATH = os.path.expandvars("%APPDATA%") + "\VGC_Analyze_data\\"
else:
    DATA_PATH = "./VGC_Analyze_data/"

EXPORT_PATH             = DATA_PATH + "export/"
LOCAL_DATA              = DATA_PATH + "local/"
DOWNLOAD_PATH           = DATA_PATH
DOWNLOAD_FILE           = DOWNLOAD_PATH + FILE_PREFIX + "VGC-Analyze-Download.csv"
LOCAL_DATA_FILE         = LOCAL_DATA + "VGC-Local-Data.json"
ONLINE_DATA_FILE        = LOCAL_DATA + "VGC-Online-Data.json"

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)


# Img vars
IMG_PATH         = DATA_PATH + "img/"
IMG_CACHE_PATH   = IMG_PATH + "cache/"
IMG_CACHE_FRONT  = IMG_CACHE_PATH + "front/"
IMG_CACHE_BACK   = IMG_CACHE_PATH + "back/"
IMG_CACHE_CART   = IMG_CACHE_PATH + "cart/"
COVER_WIDTH      = 120


# Asset vars
try:
    ASSETS_PATH = os.path.join(sys._MEIPASS, "assets", "")
    print("Working from pyinstaller directory")
except:
    ASSETS_PATH = os.path.join("assets", "")
    print("Working locally")

ICON_PATH             = os.path.join(ASSETS_PATH, "icons", "")
IMG_COVER_NONE        = os.path.join(ASSETS_PATH, "cover_placeholder.png")
IMG_COVER_PIL_MISSING = os.path.join(ASSETS_PATH, "cover_placeholder_pillow.gif")


# Settings
SETTINGS_PATH         = DATA_PATH + "settings/"
SETTINGS_FILE         = SETTINGS_PATH + "settings.json"
PLATFORM_HOLDERS_FILE = SETTINGS_PATH + "platform_holders.json"
PLATFORMS_FILE        = SETTINGS_PATH + "platforms.json"
TEMPLATES_FILE        = SETTINGS_PATH + "templates.json"
