import os
import shutil
from zipfile import ZipFile

baseTargetDir = "./build/dist/bundle/"
targetDir     = baseTargetDir + "pack/VGC_Analyze/"

if os.path.exists(baseTargetDir):
    shutil.rmtree(baseTargetDir)

if not os.path.exists(targetDir):
    os.makedirs(targetDir)

shutil.copytree("../assets/", targetDir + "assets/")
shutil.copytree("../gui/", targetDir + "gui/")
shutil.copytree("../lib/", targetDir + "lib/")
shutil.copy("../VGC_Analyze.py", targetDir + "VGC_Analyze.py")

shutil.rmtree(targetDir + "gui/__pycache__/")
shutil.rmtree(targetDir + "lib/__pycache__/")

os.chdir(targetDir + "..")

zip = ZipFile("../VGC_Analyze.zip", "w")

for root, dirs, files in os.walk("./"):
    for f in files:
        zip.write(os.path.join(root, f))

zip.close()