import os
import gettext

localedir = "./data/locales/"

_ = None

available_languages = os.listdir(localedir)

def setLocale(localeString = ""):
    global _
    global localedir

    if len(localeString):

        print("Loading locale:", localedir, localeString)

        locale = gettext.translation("base", localedir=localedir, languages=[localeString])
        locale.install()
        _ = locale.gettext
    else:
        _ = gettext.translation("base", localedir, languages=["en_US"], fallback=True).gettext