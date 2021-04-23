import os
import json
from VGC_Var import LOCAL_DATA
from VGC_Var import LOCAL_DATA_FILE

######################
# readJson
# --------------------
def readJson(fileName):
    result = {}
    if os.path.exists(fileName) and os.path.getsize(fileName) > 0:
        file = open(fileName, "r")
        result = json.load(file)
        file.close()

    return result


######################
# writeJson
# --------------------
def writeJson(localDataList, fileName):

    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))

    file = open(fileName, "w")
    json.dump(localDataList, file, sort_keys=True, indent="\t")
    file.close()