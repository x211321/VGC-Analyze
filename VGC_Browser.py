from VGC_Locale import _

import webbrowser


######################
# openItemInBrowser
# --------------------
def openItemInBrowser(item):
    webbrowser.open("https://vgcollect.com/item/"+item, new=0, autoraise=True)


######################
# openUserProfileInBrowser
# --------------------
def openUserProfileInBrowser(a):
    webbrowser.open("https://vgcollect.com/settings/", new=0, autoraise=True)


######################
# openBrowser
# --------------------
def openBrowser(url):
    webbrowser.open(url, new=0, autoraise=True)