import VGC_Settings as settings
from VGC_Locale import setLanguage
from VGC_Locale import setLocale

# Read settings and set locale before any other module gets initialized
settings.read()
setLanguage(settings.get("locale", "language", ""))
setLocale(settings.get("locale", "locale", ""))

from VGC_GUI import GUI


######################
# main Function
# --------------------
def main():
    # Show GUI
    gui = GUI()
    gui.show()


# Call Main function
#--------------------
if __name__ == "__main__":
    main()
