

import webbrowser


######################
# openItemInBrowser Function
# --------------------   
def openItemInBrowser(item):
    webbrowser.open("https://vgcollect.com/item/"+item, new=0, autoraise=True)
    
def openUserProfileInBrowser(a):
    webbrowser.open("https://vgcollect.com/settings/", new=0, autoraise=True)