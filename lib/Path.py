import os
import sys
import platform
import pathlib

FILE_PREFIX = "collection-"

DATA_FODLER = "VGC_Analyze_data"
DATA_PATH   = "./"+DATA_FODLER+"/"

if platform.system() == "Windows":
    DATA_PATH = os.path.expandvars("%APPDATA%") + "\\"+DATA_FODLER+"\\"
elif platform.system() == "Linux":
    DATA_PATH = str(pathlib.Path.home()) + "/."+DATA_FODLER+"/"
elif platform.system() == "Darwin":
    DATA_PATH = str(pathlib.Path.home()) + "/Library/Application Support/" + DATA_FODLER + "/"

EXPORT_PATH             = DATA_PATH + "export/"
LOCAL_DATA              = DATA_PATH + "local/"
DOWNLOAD_PATH           = DATA_PATH
DOWNLOAD_FILE           = DOWNLOAD_PATH + FILE_PREFIX + "VGC-Analyze-Download.csv"
LOCAL_DATA_FILE         = LOCAL_DATA + "VGC-Local-Data.json"
ONLINE_DATA_FILE        = LOCAL_DATA + "VGC-Online-Data.json"

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)


# Cover types
COVER_TYPE_FRONT = "front-box"
COVER_TYPE_BACK  = "back-box"
COVER_TYPE_CART  = "cart"


# Img vars
IMG_PATH         = DATA_PATH + "img/"
IMG_CACHE_PATH   = IMG_PATH + "cache/"
IMG_CACHE_FRONT  = IMG_CACHE_PATH + COVER_TYPE_FRONT + "/"
IMG_CACHE_BACK   = IMG_CACHE_PATH + COVER_TYPE_BACK  + "/"
IMG_CACHE_CART   = IMG_CACHE_PATH + COVER_TYPE_CART  + "/"
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
IMG_COVER_LOADING_120 = os.path.join(ASSETS_PATH, "loading_120.gif")


def getCoverPath(item, coverType):
    return IMG_CACHE_PATH + coverType + "/" + str(item.VGC_id) + ".jpg"


# Settings
SETTINGS_PATH         = DATA_PATH + "settings/"
SETTINGS_FILE         = SETTINGS_PATH + "settings.json"
PLATFORM_HOLDERS_FILE = SETTINGS_PATH + "platform_holders.json"
PLATFORMS_FILE        = SETTINGS_PATH + "platforms.json"
TEMPLATES_FILE        = SETTINGS_PATH + "templates.json"
