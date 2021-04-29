import os
import gettext
import locale

langDir = "./data/locales/"

_ = None

available_languages = os.listdir(langDir)

def setLanguage(langString = ""):
    global _
    global langDir

    if len(langString):

        print("Loading language:", langDir, langString)

        lang = gettext.translation("base", localedir=langDir, languages=[langString])
        lang.install()
        _ = lang.gettext
    else:
        _ = gettext.translation("base", localedir=langDir, languages=["en_US"], fallback=True).gettext