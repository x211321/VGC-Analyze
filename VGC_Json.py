import os
import json
from VGC_Var import LOCAL_DATA
from VGC_Var import LOCAL_DATA_FILE

######################
# readJson
# --------------------
def readJson(filePath, fileName):
    result = {}
    if os.path.exists(filePath):
        file = open(fileName, "r")
        result = json.load(file)
        file.close()

    return result


######################
# writeJson
# --------------------
def writeJson(localDataList, filePath, fileName):

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    file = open(fileName, "w")
    json.dump(localDataList, file, sort_keys=True, indent="\t")
    file.close()