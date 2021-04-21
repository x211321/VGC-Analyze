

from VGC_Console import main_console
from VGC_GUI     import GUI
from VGC_Lib     import initOptions
from VGC_Lib     import readOptions


######################
# main Function
# --------------------   
def main():
    # Define options
    #--------------------
    initOptions()
                                      

    # Read options
    #--------------------
    filterData = readOptions()
    
    # Start selected mode
    #--------------------
    if filterData.guiMode == True:
        gui = GUI(filterData)
        gui.show()
    else:
        main_console(filterData)


# Call Main function
#--------------------
if __name__ == "__main__":
    main()
