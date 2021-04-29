import os
import gettext
import locale
from datetime import datetime

langDir = "./data/locales/"

_ = None

available_languages = sorted(os.listdir(langDir))
available_locales   = []

if os.name == 'nt':
    temp = locale.windows_locale.values()
else:
    temp = locale.locale_alias.values()

for loc in sorted(temp):
    available_locales.append(loc)

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


def setLocale(localeString = ""):

    if len(localeString):

        print("Loading locale:", localeString)

        locale.setlocale(locale.LC_ALL, localeString)
    else:

        print("Loading default locale")

        locale.setlocale(locale.LC_ALL, None)


def locCurrency(value):
    return locale.currency(value, grouping=True)


def locCurrencySymbol():
    return locale.localeconv()["currency_symbol"]

def locStrToNum(str):
    return locale.atof(str)

def locDate(dateStr, showDay=False):

    # Deactivated for now
    return dateStr

    # Fix invalid dates
    if int(dateStr[0:4]) == 0:
        dateStr = dateStr.replace(dateStr[0:4], "1900")
    if int(dateStr[5:7]) == 0:
        dateStr = dateStr.replace(dateStr[5:7], "01")
    if int(dateStr[8:10]) == 0:
        dateStr = dateStr.replace(dateStr[8:10], "01")

    # Format date
    if int(dateStr[0:4]) > 0 and int(dateStr[5:7]) > 0 and int(dateStr[8:10]) > 0:
        date = datetime.strptime(dateStr, "%Y-%m-%d")

        if showDay:
            return date.strftime('%a, %x')
        else:
            return date.strftime('%x')
    else:
        return dateStr
