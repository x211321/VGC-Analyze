import os
from datetime import datetime

from tkinter import *
from tkinter import ttk

from VGC_Widgets import Label_


######################
# initCollectionInfo
# --------------------
def initCollectionInfo(gui):
    # Collection info
    # ------------------

    # Collection info sub-frame
    gui.info_sub_frame = Frame(gui.info_frame)
    gui.info_sub_frame.grid(row=0, column=1, sticky="nws", padx=(0,10))

    # Graph functions sub-frame
    gui.info_tool_frame = Frame(gui.info_frame , width=200 , height=200, pady=0 , padx=0)
    gui.info_tool_frame.grid(row=0, column=2, sticky="nes")

    gui.info_frame.grid_columnconfigure(1, weight=1)

    # Info sub-frame widgets
    gui.info_number_txt = Label_(gui.info_sub_frame, text="Item count:")
    gui.info_number     = Label_(gui.info_sub_frame)

    gui.info_value_txt  = Label_(gui.info_sub_frame, text="Total price:")
    gui.info_value      = Label_(gui.info_sub_frame)

    gui.info_average_txt= Label_(gui.info_sub_frame, text="Avg. price:")
    gui.info_average    = Label_(gui.info_sub_frame)

    gui.info_first_txt  = Label_(gui.info_sub_frame, text="First purchase:")
    gui.info_first      = Label_(gui.info_sub_frame)

    gui.info_last_txt   = Label_(gui.info_sub_frame, text="Last purchase:")
    gui.info_last       = Label_(gui.info_sub_frame)

    gui.info_update_txt = Label_(gui.info_sub_frame, text="Database updated:")
    gui.info_update     = Label_(gui.info_sub_frame)

    gui.info_grp_number_txt     = Label_(gui.info_sub_frame)
    gui.info_grp_number         = Label_(gui.info_sub_frame)
    gui.info_grp_number_spacer  = Label_(gui.info_sub_frame)

    gui.info_grp_average_txt    = Label_(gui.info_sub_frame)
    gui.info_grp_average        = Label_(gui.info_sub_frame)
    gui.info_grp_average_spacer = Label_(gui.info_sub_frame)

    gui.info_grp_priceHigh_txt  = Label_(gui.info_sub_frame)
    gui.info_grp_priceHigh      = Label_(gui.info_sub_frame)
    gui.info_grp_priceHigh_name = Label_(gui.info_sub_frame)

    gui.info_grp_priceLow_txt   = Label_(gui.info_sub_frame)
    gui.info_grp_priceLow       = Label_(gui.info_sub_frame)
    gui.info_grp_priceLow_name  = Label_(gui.info_sub_frame)

    gui.info_grp_countHigh_txt  = Label_(gui.info_sub_frame)
    gui.info_grp_countHigh      = Label_(gui.info_sub_frame)
    gui.info_grp_countHigh_name = Label_(gui.info_sub_frame)

    gui.info_grp_countLow_txt   = Label_(gui.info_sub_frame)
    gui.info_grp_countLow       = Label_(gui.info_sub_frame)
    gui.info_grp_countLow_name  = Label_(gui.info_sub_frame)

    gui.info_number_txt.grid(row=0, column=0, sticky="nw", pady=(0, 5))
    gui.info_number.grid(row=0, column=1, sticky="ne", pady=(0, 5), padx=(0, 30))

    gui.info_value_txt.grid(row=1, column=0, sticky="nw")
    gui.info_value.grid(row=1, column=1, sticky="ne", pady=(0, 5), padx=(0, 30))

    gui.info_average_txt.grid(row=2, column=0, sticky="nw")
    gui.info_average.grid(row=2, column=1, sticky="ne", pady=(0, 5), padx=(0, 30))

    gui.info_first_txt.grid(row=0, column=2, sticky="nw", pady=(0, 5), padx=(0, 30))
    gui.info_first.grid(row=0, column=3, sticky="nw", pady=(0, 5), padx=(0, 30))

    gui.info_last_txt.grid(row=1, column=2, sticky="nw", pady=(0, 5), padx=(0, 30))
    gui.info_last.grid(row=1, column=3, sticky="nw", pady=(0, 5), padx=(0, 30))

    gui.info_update_txt.grid(row=2, column=2, sticky="nw", pady=(0, 5), padx=(0, 30))
    gui.info_update.grid(row=2, column=3, sticky="nw", pady=(0, 5), padx=(0, 30))


    gui.info_grp_number_txt.grid(row=0, column=4, sticky="nw", pady=(0, 5))
    gui.info_grp_number.grid(row=0, column=5, sticky="ne", pady=(0, 5))
    gui.info_grp_number_spacer.grid(row=0, column=6, sticky="ne", pady=(0, 5), padx=(0, 30))

    gui.info_grp_countLow_txt.grid(row=1, column=4, sticky="nw", pady=(0, 5))
    gui.info_grp_countLow.grid(row=1, column=5, sticky="ne", pady=(0, 5))
    gui.info_grp_countLow_name.grid(row=1, column=6, sticky="nw", pady=(0, 5), padx=(0, 30))

    gui.info_grp_countHigh_txt.grid(row=2, column=4, sticky="nw", pady=(0, 5))
    gui.info_grp_countHigh.grid(row=2, column=5, sticky="ne", pady=(0, 5))
    gui.info_grp_countHigh_name.grid(row=2, column=6, sticky="nw", pady=(0, 5), padx=(0, 30))

    gui.info_grp_average_txt.grid(row=0, column=7, sticky="nw")
    gui.info_grp_average.grid(row=0, column=8, sticky="ne", pady=(0, 5))
    gui.info_grp_average_spacer.grid(row=0, column=9, sticky="ne", pady=(0, 5))

    gui.info_grp_priceLow_txt.grid(row=1, column=7, sticky="nw", pady=(0, 5))
    gui.info_grp_priceLow.grid(row=1, column=8, sticky="ne", pady=(0, 5))
    gui.info_grp_priceLow_name.grid(row=1, column=9, sticky="nw", pady=(0, 5))

    gui.info_grp_priceHigh_txt.grid(row=2, column=7, sticky="nw", pady=(0, 5))
    gui.info_grp_priceHigh.grid(row=2, column=8, sticky="ne", pady=(0, 5))
    gui.info_grp_priceHigh_name.grid(row=2, column=9, sticky="nw", pady=(0, 5))


    # Graph functions sub-frame widgets
    gui.info_toggle_graph = Button(gui.info_tool_frame)
    gui.info_toggle_graph.config(command=gui.toggleGraphFrame, image=gui.item_graph_ico, relief="groove")
    gui.info_toggle_graph.grid(row=0, column=0)


######################
# displayCollectionInfo
# --------------------
def displayCollectionInfo(gui):
    gui.info_number.set(gui.collectionData.totals.item_count)
    gui.info_value.set("{:.2f}".format(gui.collectionData.totals.total_price))
    if gui.collectionData.totals.item_count:
        gui.info_average.set("{:.2f}".format(gui.collectionData.totals.total_price/gui.collectionData.totals.item_count))
    else:
        gui.info_average.set("{:.2f}".format(0))
    gui.info_first.set(gui.collectionData.totals.first.date + "  -  " +
                        gui.collectionData.totals.first.name)
    gui.info_last.set(gui.collectionData.totals.last.date + "  -  " +
                        gui.collectionData.totals.last.name)

    if os.path.exists(gui.collectionData.csv_file):
        gui.info_update.set(str(datetime.fromtimestamp(os.path.getmtime(gui.collectionData.csv_file))).split(".")[0])

    if gui.collectionData.filterData.groupItems:
        gui.info_grp_number_txt.set("Group count:")
        gui.info_grp_number.set(str(len(gui.collectionData.groups)))

        gui.info_grp_average_txt.set("Avg. group price:")
        gui.info_grp_average.set("{:.2f}".format(gui.collectionData.totals.total_price/len(gui.collectionData.groups)))

        gui.info_grp_priceLow_txt.set("Lowest group price:")
        gui.info_grp_priceLow.set("{:.2f}".format(gui.collectionData.getGroupPriceLow().total_price))
        gui.info_grp_priceLow_name.set(" -  " + gui.collectionData.groupKey_priceLow)

        gui.info_grp_priceHigh_txt.set("Highest group price:")
        gui.info_grp_priceHigh.set("{:.2f}".format(gui.collectionData.getGroupPriceHigh().total_price))
        gui.info_grp_priceHigh_name.set(" -  " + gui.collectionData.groupKey_priceHigh)

        gui.info_grp_countLow_txt.set("Least group items:")
        gui.info_grp_countLow.set(gui.collectionData.getGroupCountLow().item_count)
        gui.info_grp_countLow_name.set(" -  " + gui.collectionData.groupKey_countLow)

        gui.info_grp_countHigh_txt.set("Most group items:")
        gui.info_grp_countHigh.set(gui.collectionData.getGroupCountHigh().item_count)
        gui.info_grp_countHigh_name.set(" -  " + gui.collectionData.groupKey_countHigh)
    else:
        gui.info_grp_number_txt.set("")
        gui.info_grp_number.set("")

        gui.info_grp_average_txt.set("")
        gui.info_grp_average.set("")

        gui.info_grp_priceLow_txt.set("")
        gui.info_grp_priceLow.set("")
        gui.info_grp_priceLow_name.set("")

        gui.info_grp_priceHigh_txt.set("")
        gui.info_grp_priceHigh.set("")
        gui.info_grp_priceHigh_name.set("")

        gui.info_grp_countLow_txt.set("")
        gui.info_grp_countLow.set("")
        gui.info_grp_countLow_name.set("")

        gui.info_grp_countHigh_txt.set("")
        gui.info_grp_countHigh.set("")
        gui.info_grp_countHigh_name.set("")