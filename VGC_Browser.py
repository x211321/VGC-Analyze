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