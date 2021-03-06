import platform
import subprocess
from lib.Locale import _

import webbrowser


######################
# openItemInBrowser
# --------------------
def openItemInBrowser(item):
    webbrowser.open("https://vgcollect.com/item/"+item, new=0, autoraise=True)


######################
# openVGCInBrowser
# --------------------
def openVGCInBrowser(subUrl):
    webbrowser.open("https://vgcollect.com/"+subUrl, new=0, autoraise=True)


######################
# openUserProfileInBrowser
# --------------------
def openUserProfileInBrowser(a):
    webbrowser.open("https://vgcollect.com/settings/", new=0, autoraise=True)


######################
# openGithub
# --------------------
def openGithub(a):
    webbrowser.open("https://github.com/x211321/VGC_Analyze", new=0, autoraise=True)


######################
# openBrowser
# --------------------
def openBrowser(url):
    webbrowser.open(url, new=0, autoraise=True)


######################
# openFileManager
# --------------------
def openFileManager(path):
    if platform.system() == "Linux":
        subprocess.Popen(["xdg-open", path])
    if platform.system() == "Windows":
        openBrowser(path)
    if platform.system() == "Darwin":
        subprocess.Popen(["open", path])
