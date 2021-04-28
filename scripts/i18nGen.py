import os
import sys
import shutil
import polib

languages = ["en_US", "de_DE"]

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

os.system("\""+pyToolPath + "i18n/pygettext.py\" -d base -o "+path+"base.pot " + " ".join(files))

for language in languages:

    targetPath = path + language + "/LC_MESSAGES/"

    if not os.path.exists(targetPath):
        os.makedirs(targetPath)

    if os.path.exists(targetPath+"base.po"):
        # Newly generated template
        pot_file = polib.pofile(path + "base.pot")

        # Existing translation
        po_file = polib.pofile(targetPath + "base.po")

        # Merge
        po_file.merge(pot_file)

        # Save
        po_file.save(targetPath + "base.po")
    else:
        # New translation
        # Copy
        shutil.copyfile(path+"base.pot", targetPath+"base.po")

