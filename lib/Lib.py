from lib.Locale import _

import lib.Var as VAR

######################
# stringToYN
# --------------------
def stringToYN(s):
    s = s.lower()

    if s == "y" or s == "yes" or s == "j" or s == "1" or s == "true":
        return "Yes"
    else:
        return "No"


######################
# toggleYN
# --------------------
def toggleYN(currentState):
    if stringToYN(currentState) == "Yes":
        return "No"
    else:
        return "Yes"


######################
# YNToX
# --------------------
def YNToX(yn):
    yn = yn.lower()

    if yn == "yes":
        return "X"
    else:
        return " "

def _YesNoToYesNo(_value):
    result = ""

    if _value == VAR.ITEM_ATTRIBUTE_NO:
        result = "No"
    if _value == VAR.ITEM_ATTRIBUTE_YES:
        result = "Yes"

    return result

######################
# guessDate
# --------------------
def guessDate(date, mode):
    if len(date) == 10:
        return date
    if len(date) == 7:
        if mode == "start":
            return date + "-01"
        if mode == "end":
            return date + "-31"
    if len(date) == 4:
        if mode == "start":
            return date + "-01-01"
        if mode == "end":
            return date + "-12-31"

    return date