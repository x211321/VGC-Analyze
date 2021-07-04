import os
import sys
import platform
import gettext
import locale
from datetime import datetime

from lib.Locale_Languages import languages
from lib.Locale_Countries import countries

# Asset vars
try:
    langDir = os.path.join(sys._MEIPASS, "assets", "locales", "")
except:
    langDir = os.path.join("assets", "locales", "")

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

        if platform.system() == "Darwin":
            # Python doesn't like the default locale
            # when running on darwin, for now
            # set to en_US so the app can run
            locale.setlocale(locale.LC_ALL, "en_US")
        else:
            locale.setlocale(locale.LC_ALL, "")


def locCurrency(value):
    return locale.currency(value, grouping=True)


def locCurrencySymbol():
    return locale.localeconv()["currency_symbol"]


def locStrToNum(str):
    return locale.atof(str)


def locStrToDate(str, showDay=False):

    # Handle invalid dates
    if len(str) >= 10:
        if str[0:5]  == "0000-" or str[4:7]  == "-00" or str[7:10] == "-00":
            return str

    # Convert locale date to iso date
    if showDay:
        return datetime.strptime(str, '%a, %x').isoformat()
    else:
        return datetime.strptime(str, '%x').isoformat()


def locDate(dateStr, showDay=False):
    if len(dateStr) > 10:
        dateStr = dateStr[0:10]

    if len(dateStr) == 10:
        # Format date
        if int(dateStr[0:4]) > 0 and int(dateStr[5:7]) > 0 and int(dateStr[8:10]) > 0:
            date = datetime.strptime(dateStr, "%Y-%m-%d")

            if showDay:
                return date.strftime('%a, %x')
            else:
                return date.strftime('%x')

    return dateStr


def locDateTime(dateTimeStr, showDay=False, showDate=True, showTime=True):
    # Deactivated for now
    # return dateStr

    if len(dateTimeStr) > 19:
        dateTimeStr = dateTimeStr[0:19]

    if len(dateTimeStr) == 19:
        # Format date
        if (int(dateTimeStr[0:4]) > 0 and int(dateTimeStr[5:7]) > 0 and int(dateTimeStr[8:10]) > 0):

            dateTime = datetime.strptime(dateTimeStr, "%Y-%m-%d %H:%M:%S")

            format = ""

            if showDay:
                format += "%a, "
            if showDate:
                format += "%x"
            if showTime:
                if len(format):
                    format += " - "
                format += "%X"

            return dateTime.strftime(format)

    return dateTimeStr


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
    if len(code) > 0 and "_" in code:
        parts = code.split("_")

        return getLanguageName(parts[0]) + " (" + getCountryName(parts[1]) + ")"
    return ""


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


def i18nToRaw(dict, i18n):
    for key in dict:
        if dict[key] == i18n:
            return key

    return i18n
