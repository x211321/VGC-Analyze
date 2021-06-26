from lib.Locale import _

import lib.Var as VAR


######################
# toggleYN
# --------------------
def toggleYN(currentState):
    if currentState == VAR.ATTRIBUTE_YES:
        return VAR.ATTRIBUTE_NO
    else:
        return VAR.ATTRIBUTE_YES


######################
# YNToX
# --------------------
def YNToX(yn):
    yn = yn.lower()

    if yn == "yes":
        return "X"
    else:
        return " "


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
            if date == "0000":
                return date + "-00-00"
            else:
                return date + "-01-01"
        if mode == "end":
            return date + "-12-31"

    return date
