import os

# Cannot be dependent on VGC_Var.
# Settings must be read before
# VGC_Var is initialized since VGC_Var
# contains translatable strings.
SETTINGS_PATH = "./data/settings/"
SETTINGS_FILE = SETTINGS_PATH + "settings.json"

from VGC_Json import readJson
from VGC_Json import writeJson

settings_data = {}

def read():
    global settings_data

    if os.path.exists(SETTINGS_FILE):
        settings_data = readJson(SETTINGS_FILE)

def write():
    global settings_data

    writeJson(settings_data, SETTINGS_FILE)

def get(section, key, default):
    global settings_data

    if section in settings_data.keys():
        if key in settings_data[section].keys():
            return settings_data[section][key]
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

