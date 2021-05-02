import os
import gettext
import locale
from datetime import datetime

from lib.Locale_Languages import languages
from lib.Locale_Countries import countries

langDir = "./assets/locales/"

_ = None


def setLanguage(langString = ""):
    global _
    global langDir

    if len(langString) and os.path.exists(langDir + langString):

        print("Loading language:", langDir, langString)

        lang = gettext.translation("base", localedir=langDir, languages=[langString])
        lang.install()
        _ = lang.gettext
    else:
        _ = gettext.gettext


def setLocale(localeString = ""):

    if len(localeString):

        print("Loading locale:", localeString)

        locale.setlocale(locale.LC_ALL, localeString)
    else:

        print("Loading default locale")

        locale.setlocale(locale.LC_ALL, "en_US")


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


def getLanguageName(code, native = False):
    for language in languages:
        if language["code"] == code:
            if native:
                return language["native"]
            else:
                return language["name"]

    return code


def getLanguageCode(name, native = False):
    for language in languages:
        if native:
            if language["native"] == name:
                return language["code"]
        else:
            if language["name"] == name:
                return language["code"]


def getCountryName(code):
    for country in countries:
        if country["code"] == code:
            return country["name"]

    return code


def getCountryCode(name):
    for country in countries:
        if country["name"] == name:
            return country["code"]

def getLocaleName(code):
    parts = code.split("_")

    return getLanguageName(parts[0]) + " (" + getCountryName(parts[1]) + ")"

def getLocaleCode(name):
    parts = name.strip(")").split(" (")

    return getLanguageCode(parts[0]) + "_" + getCountryCode(parts[1])

def getAvailableLanguageCodes():
    global langDir

    return sorted(os.listdir(langDir))

def getAvailableLanguageNames():
    languageNames = []

    for code in getAvailableLanguageCodes():
        languageNames.append(getLocaleName(code))

    return languageNames

def getAvailableLocaleCodes():
    locales = []

    if os.name == 'nt':
        temp = locale.windows_locale.values()
    else:
        temp = locale.locale_alias.values()

    for loc in sorted(temp):
        locales.append(loc)

    return locales

def getAvailableLocaleNames():
    localeNames = []

    for code in getAvailableLocaleCodes():
        localeNames.append(getLocaleName(code))

    return localeNames


