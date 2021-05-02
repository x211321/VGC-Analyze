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
