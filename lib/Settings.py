import os

# Cannot be dependent on VGC_Var.
# Settings must be read before
# VGC_Var is initialized since VGC_Var
# contains translatable strings.
SETTINGS_PATH         = "./VGC_Analyze_data/settings/"
SETTINGS_FILE         = SETTINGS_PATH + "settings.json"
PLATFORM_HOLDERS_FILE = SETTINGS_PATH + "platform_holders.json"
PLATFORMS_FILE        = SETTINGS_PATH + "platforms.json"

from lib.Json import readJson
from lib.Json import writeJson

settings_data         = {}
platform_holders_data = {}
platforms_data        = {}

def read():
    global settings_data

    if os.path.exists(SETTINGS_FILE):
        settings_data = readJson(SETTINGS_FILE)
    else:
        settings_data = defaultSettings()

def write():
    global settings_data

    writeJson(settings_data, SETTINGS_FILE)

def get(section, key, default):
    global settings_data

    if section in settings_data.keys():
        if key in settings_data[section].keys():
            return settings_data[section][key]
        else:
            if key in defaultSettings()[section].keys():
                return defaultSettings()[section][key]
            else:
                print("Unknown settings key")
    else:
        print("Unknown settings section")

    return default

def set(section, key, value):
    global settings_data

    if not section in settings_data.keys():
        print("New settings section")
        settings_data[section] = {}

    settings_data[section][key] = value

def defaultSettings():
    return {
                "locale": {
                    "language": "en_US"
                },
                "display": {
                    "detailsOnDoubleClick": 1,
                    "refreshOnFilterSelect": 1
                }
            }



def readPlatformHolders():
    global platform_holders_data

    if os.path.exists(PLATFORM_HOLDERS_FILE):
        platform_holders_data = readJson(PLATFORM_HOLDERS_FILE)
    else:
        platform_holders_data = defaultPlatformHolders()

def writePlatformHolders():
    global platform_holders_data

    writeJson(platform_holders_data, PLATFORM_HOLDERS_FILE)

def listPlatformHolders():
    global platform_holders_data

    return platform_holders_data.keys()

def getPlatformHolderKeywords(platformHolder):
    global platform_holders_data

    if platformHolder in platform_holders_data:
        return platform_holders_data[platformHolder]

    return []

def setPlatformHolderKeywords(platformHolder, keywords):
    global platform_holders_data

    platform_holders_data[platformHolder] = keywords

def removePlatformHolder(platformHolder):
    global platform_holders_data

    platform_holders_data.pop(platformHolder)

def defaultPlatformHolders():
    return {"Nintendo": ["nintendo", "gamecube", "game boy", "amiibo", "dsi", "e-reader", "famicom", "watch", "nes", "pokemon", "pokémon", "virtual boy", "wii"],
	        "Sony": ["playstation", "psone", "psp"],
	        "Microsoft": ["xbox", "kinect"],
	        "Sega": ["sega"],
	        "3DO": ["3do"],
	        "Amiga": ["amiga"],
	        "Amstrad": ["amstrad"],
	        "Apple": ["apple"],
	        "Atari": ["atari"],
	        "Philips": ["philips", "cd-i"],
	        "Coleco": ["coleco"],
	        "Commodore": ["commodore"],
	        "Fairchild": ["fairchild"],
	        "Fujitsu": ["fujitsu", "fm towns"],
	        "GOG.com": ["gog"],
	        "Google": ["google", "stadia"],
	        "Mattel": ["mattel", "intellivision"],
	        "Magnavox": ["magnavox"],
	        "NEC": ["nec", "pc-fx", "supergrafx", "turbografx"],
	        "SNK": ["snk", "neo geo"],
	        "Pioneer": ["pioneer"],
	        "Bandai": ["playdia", "swancrystal", "wonderswan"],
	        "Capcom": ["cp system"],
	        "Steam": ["steam"],
	        "Tiger": ["tiger"],
	        "VTech": ["vtech"]
           }



def readPlatforms():
    global platforms_data

    if os.path.exists(PLATFORMS_FILE):
        platforms_data = readJson(PLATFORMS_FILE)
    else:
        platforms_data = defaultPlatforms()

def writePlatforms():
    global platforms_data

    writeJson(platforms_data, PLATFORMS_FILE)

def listPlatforms():
    global platforms_data

    return platforms_data.keys()

def getPlatformOverwrite(platform):
    global platforms_data

    if platform in platforms_data:
        return platforms_data[platform]

    return ""

def setPlatformOverwrite(platform, overwrite):
    global platforms_data

    platforms_data[platform] = overwrite

def removePlatform(platform):
    global platforms_data

    platforms_data.pop(platform)

def defaultPlatforms():
    return {"Famicom": "NES/Famicom",
            "Nintendo Entertainment System": "NES/Famicom",
            "Sega Mega Drive": "Sega Genesis/Mega Drive",
            "Sega Genesis": "Sega Genesis/Mega Drive",
            "Super Famicom": "Super Nintendo/Super Famicom",
            "Super Nintendo": "Super Nintendo/Super Famicom"
           }