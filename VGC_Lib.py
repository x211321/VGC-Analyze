from VGC_Locale import _

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
        return stringToYN("No")
    else:
        return stringToYN("Yes")


######################
# YNToX
# --------------------
def YNToX(yn):
    yn = yn.lower()

    if yn == "yes":
        return "X"
    else:
        return " "
