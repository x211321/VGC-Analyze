from VGC_Locale import _

import os
import json

######################
# readJson
# --------------------
def readJson(fileName):
    result = {}
    if os.path.exists(fileName) and os.path.getsize(fileName) > 0:
        file = open(fileName, "r", encoding="utf-8")
        result = json.load(file)
        file.close()

    return result


######################
# writeJson
# --------------------
def writeJson(data, fileName):

    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))

    file = open(fileName, "w", encoding="utf-8")
    json.dump(data, file, sort_keys=True, indent="\t")
    file.close()
