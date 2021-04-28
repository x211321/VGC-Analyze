import os
import sys
import shutil

languages = ["en", "de"]

pyToolPath = os.path.dirname(sys.executable).replace("\\", "/") + "/tools/"

files = []

path = "../"

file_list = os.listdir(path)

for file in file_list:
    if file.startswith("VGC_") and file.endswith(".py"):
        files.append(path+file)

path = "../gui/"

file_list = os.listdir(path)

for file in file_list:
    if file.startswith("VGC_") and file.endswith(".py"):
        files.append(path+file)

path = "../locales/"

if not os.path.exists(path):
    os.makedirs(path)

os.system("\""+pyToolPath + "i18n/pygettext.py\" -d base -o "+path+"base.po " + " ".join(files))

for language in languages:

    targetPath = path + language + "/LC_MESSAGES/"

    if not os.path.exists(targetPath):
        os.makedirs(targetPath)

    shutil.copyfile(path+"base.po", targetPath+"base.po")

