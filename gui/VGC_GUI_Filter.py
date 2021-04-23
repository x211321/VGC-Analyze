from tkinter import *
from tkinter import ttk

from VGC_Widgets import Label_
from VGC_Widgets import Entry_
from VGC_Widgets import Combobox_


######################
# initFilter
# --------------------
def initFilter(gui):

    # Filter inputs
    # ------------------
    gui.filterInputs = {}

    gui.filterInputs["name_txt"]       = Label_(gui.filter_frame, width=25, text="Title")
    gui.filterInputs["name"]           = Entry_(gui.filter_frame, width=30)
    gui.filterInputs["platform_txt"]   = Label_(gui.filter_frame, width=25, text="Platform")
    gui.filterInputs["platform"]       = Combobox_(gui.filter_frame, width=27)
    gui.filterInputs["region_txt"]     = Label_(gui.filter_frame, width=25, text="Region")
    gui.filterInputs["region"]         = Combobox_(gui.filter_frame, width=27)
    gui.filterInputs["notes_txt"]      = Label_(gui.filter_frame, width=25, text="Notes")
    gui.filterInputs["notes"]          = Entry_(gui.filter_frame, width=30)
    gui.filterInputs["dateStart_txt"]  = Label_(gui.filter_frame, width=25, text="Min. date")
    gui.filterInputs["dateStart"]      = Entry_(gui.filter_frame, width=30)
    gui.filterInputs["dateEnd_txt"]    = Label_(gui.filter_frame, width=25, text="Max. date")
    gui.filterInputs["dateEnd"]        = Entry_(gui.filter_frame, width=30)
    gui.filterInputs["priceStart_txt"] = Label_(gui.filter_frame, width=25, text="Min. price")
    gui.filterInputs["priceStart"]     = Entry_(gui.filter_frame, width=30)
    gui.filterInputs["priceEnd_txt"]   = Label_(gui.filter_frame, width=25, text="Max. price")
    gui.filterInputs["priceEnd"]       = Entry_(gui.filter_frame, width=30)
    gui.filterInputs["cart_txt"]       = Label_(gui.filter_frame, width=10, text="Cart")
    gui.filterInputs["box_txt"]        = Label_(gui.filter_frame, width=10, text="Box")
    gui.filterInputs["cart"]           = Combobox_(gui.filter_frame, values=("", "Yes", "No"), state="readonly", width=10)
    gui.filterInputs["box"]            = Combobox_(gui.filter_frame, values=("", "Yes", "No"), state="readonly", width=10)
    gui.filterInputs["manual_txt"]     = Label_(gui.filter_frame, width=10, text="Manual")
    gui.filterInputs["other_txt"]      = Label_(gui.filter_frame, width=10, text="Other")
    gui.filterInputs["manual"]         = Combobox_(gui.filter_frame, values=("", "Yes", "No"), state="readonly", width=10)
    gui.filterInputs["other"]          = Combobox_(gui.filter_frame, values=("", "Yes", "No"), state="readonly", width=10)
    gui.filterInputs["bookmarked_txt"] = Label_(gui.filter_frame, text="Bookmarked", width=10)
    gui.filterInputs["finished_txt"]   = Label_(gui.filter_frame, text="Finished", width=10)
    gui.filterInputs["bookmarked"]     = Combobox_(gui.filter_frame, values=("", "Yes", "No"), state="readonly", width=10)
    gui.filterInputs["finished"]       = Combobox_(gui.filter_frame, values=("", "Yes", "No"), state="readonly", width=10)
    gui.filterInputs["group_txt"]      = Label_(gui.filter_frame, text="Group by", width=10)
    gui.filterInputs["order_txt"]      = Label_(gui.filter_frame, text="Sort by", width=10)
    gui.filterInputs["group"]          = Combobox_(gui.filter_frame, state="readonly", width=10)
    gui.filterInputs["order"]          = Combobox_(gui.filter_frame, state="readonly", width=10)
    gui.filterInputs["order_dir_txt"]  = Label_(gui.filter_frame, text="Sort direction", width=10)
    gui.filterInputs["dummy_txt"]      = Label_(gui.filter_frame, text="", width=10)
    gui.filterInputs["orderDirection"] = Combobox_(gui.filter_frame, values=("", "ascending", "descending"), state="readonly", width=10)

    gui.filter_apply = Button(gui.filter_frame, width=10, relief="groove", bg="#BDF593")
    gui.filter_reset = Button(gui.filter_frame, width=10, relief="groove", bg="#F59398")

    row = 0
    col = 0

    itemWidth        = 0
    colspan          = 0
    rowWidth         = 25
    rowWidth_current = 0

    for key in gui.filterInputs:
        itemWidth = gui.filterInputs[key]['width']

        if rowWidth_current and (rowWidth_current + itemWidth <= rowWidth):
            col +=1

        rowWidth_current += itemWidth

        if rowWidth_current >= rowWidth:
            rowWidth_current = itemWidth
            row += 1
            col  = 0

        if itemWidth >= rowWidth:
            colspan = 2
        else:
            colspan = 1
            if col == 0:
                gui.filterInputs[key].grid(padx=(0, 18))

        gui.filterInputs[key].grid(row=row, column=col, sticky="nw", columnspan=colspan)

        if (row) % 2 == 0:
            gui.filterInputs[key].grid(pady=(0,5))

        gui.filterInputs[key].bind('<Return>', gui.showData)

    gui.filter_reset.config(text="Reset filter", command=lambda:resetFilter(gui))
    gui.filter_reset.grid(row=100, column=0, sticky="nw", pady=(20, 5))

    gui.filter_apply.config(text="Apply filter", command=gui.showData)
    gui.filter_apply.grid(row=100, column=1, sticky="nw", pady=(20, 5))


######################
# resetFilter
# --------------------
def resetFilter(gui):
    for key in gui.filterInputs:
        print(key, gui.filterInputs[key].__class__.__name__)
        if gui.filterInputs[key].__class__.__name__ == "Entry_":
            gui.filterInputs[key].delete(0, END)
        if gui.filterInputs[key].__class__.__name__ == "Combobox_":
            gui.filterInputs[key].set("")

    gui.showData()
