import os
from datetime import datetime

from tkinter import *
from tkinter import ttk

from VGC_Widgets import Label_
from VGC_Img     import loadIcon


######################
# GUI_CollectionInfo
# --------------------
class GUI_CollectionInfo(Frame):
    def __init__(self, master, gui, width=0, height=0, pady=0, padx=0):
        super().__init__(master=master, width=width, height=height, pady=pady, padx=padx)

        self.toggleGraphFrame = gui.toggleGraphFrame
        self.toggleGraphIcon  = loadIcon("bar-chart-outline", 30, 30)

        self.init()


    def init(self):
        # Collection info
        # ------------------

        # Collection info sub-frame
        self.info_sub_frame = Frame(self)
        self.info_sub_frame.grid(row=0, column=1, sticky="nws", padx=(0,10))

        # Graph functions sub-frame
        self.info_tool_frame = Frame(self , width=200 , height=200, pady=0 , padx=0)
        self.info_tool_frame.grid(row=0, column=2, sticky="nes")

        self.grid_columnconfigure(1, weight=1)

        # Info sub-frame widgets
        self.info_number_txt = Label_(self.info_sub_frame, text="Item count:")
        self.info_number     = Label_(self.info_sub_frame)

        self.info_value_txt  = Label_(self.info_sub_frame, text="Total price:")
        self.info_value      = Label_(self.info_sub_frame)

        self.info_average_txt= Label_(self.info_sub_frame, text="Avg. price:")
        self.info_average    = Label_(self.info_sub_frame)

        self.info_first_txt  = Label_(self.info_sub_frame, text="First purchase:")
        self.info_first      = Label_(self.info_sub_frame)

        self.info_last_txt   = Label_(self.info_sub_frame, text="Last purchase:")
        self.info_last       = Label_(self.info_sub_frame)

        self.info_update_txt = Label_(self.info_sub_frame, text="Database updated:")
        self.info_update     = Label_(self.info_sub_frame)

        self.info_grp_number_txt     = Label_(self.info_sub_frame)
        self.info_grp_number         = Label_(self.info_sub_frame)
        self.info_grp_number_spacer  = Label_(self.info_sub_frame)

        self.info_grp_average_txt    = Label_(self.info_sub_frame)
        self.info_grp_average        = Label_(self.info_sub_frame)
        self.info_grp_average_spacer = Label_(self.info_sub_frame)

        self.info_grp_priceHigh_txt  = Label_(self.info_sub_frame)
        self.info_grp_priceHigh      = Label_(self.info_sub_frame)
        self.info_grp_priceHigh_name = Label_(self.info_sub_frame)

        self.info_grp_priceLow_txt   = Label_(self.info_sub_frame)
        self.info_grp_priceLow       = Label_(self.info_sub_frame)
        self.info_grp_priceLow_name  = Label_(self.info_sub_frame)

        self.info_grp_countHigh_txt  = Label_(self.info_sub_frame)
        self.info_grp_countHigh      = Label_(self.info_sub_frame)
        self.info_grp_countHigh_name = Label_(self.info_sub_frame)

        self.info_grp_countLow_txt   = Label_(self.info_sub_frame)
        self.info_grp_countLow       = Label_(self.info_sub_frame)
        self.info_grp_countLow_name  = Label_(self.info_sub_frame)

        self.info_number_txt.grid(row=0, column=0, sticky="nw", pady=(0, 5))
        self.info_number.grid(row=0, column=1, sticky="ne", pady=(0, 5), padx=(0, 30))

        self.info_value_txt.grid(row=1, column=0, sticky="nw")
        self.info_value.grid(row=1, column=1, sticky="ne", pady=(0, 5), padx=(0, 30))

        self.info_average_txt.grid(row=2, column=0, sticky="nw")
        self.info_average.grid(row=2, column=1, sticky="ne", pady=(0, 5), padx=(0, 30))

        self.info_first_txt.grid(row=0, column=2, sticky="nw", pady=(0, 5), padx=(0, 30))
        self.info_first.grid(row=0, column=3, sticky="nw", pady=(0, 5), padx=(0, 30))

        self.info_last_txt.grid(row=1, column=2, sticky="nw", pady=(0, 5), padx=(0, 30))
        self.info_last.grid(row=1, column=3, sticky="nw", pady=(0, 5), padx=(0, 30))

        self.info_update_txt.grid(row=2, column=2, sticky="nw", pady=(0, 5), padx=(0, 30))
        self.info_update.grid(row=2, column=3, sticky="nw", pady=(0, 5), padx=(0, 30))


        self.info_grp_number_txt.grid(row=0, column=4, sticky="nw", pady=(0, 5))
        self.info_grp_number.grid(row=0, column=5, sticky="ne", pady=(0, 5))
        self.info_grp_number_spacer.grid(row=0, column=6, sticky="ne", pady=(0, 5), padx=(0, 30))

        self.info_grp_countLow_txt.grid(row=1, column=4, sticky="nw", pady=(0, 5))
        self.info_grp_countLow.grid(row=1, column=5, sticky="ne", pady=(0, 5))
        self.info_grp_countLow_name.grid(row=1, column=6, sticky="nw", pady=(0, 5), padx=(0, 30))

        self.info_grp_countHigh_txt.grid(row=2, column=4, sticky="nw", pady=(0, 5))
        self.info_grp_countHigh.grid(row=2, column=5, sticky="ne", pady=(0, 5))
        self.info_grp_countHigh_name.grid(row=2, column=6, sticky="nw", pady=(0, 5), padx=(0, 30))

        self.info_grp_average_txt.grid(row=0, column=7, sticky="nw")
        self.info_grp_average.grid(row=0, column=8, sticky="ne", pady=(0, 5))
        self.info_grp_average_spacer.grid(row=0, column=9, sticky="ne", pady=(0, 5))

        self.info_grp_priceLow_txt.grid(row=1, column=7, sticky="nw", pady=(0, 5))
        self.info_grp_priceLow.grid(row=1, column=8, sticky="ne", pady=(0, 5))
        self.info_grp_priceLow_name.grid(row=1, column=9, sticky="nw", pady=(0, 5))

        self.info_grp_priceHigh_txt.grid(row=2, column=7, sticky="nw", pady=(0, 5))
        self.info_grp_priceHigh.grid(row=2, column=8, sticky="ne", pady=(0, 5))
        self.info_grp_priceHigh_name.grid(row=2, column=9, sticky="nw", pady=(0, 5))


        # Graph functions sub-frame widgets
        self.info_toggle_graph = Button(self.info_tool_frame)
        self.info_toggle_graph.config(command=self.toggleGraphFrame, image=self.toggleGraphIcon, relief="groove")
        self.info_toggle_graph.grid(row=0, column=0, padx=6)


    def update(self, gui):
        self.info_number.set(gui.collectionData.totals.item_count)
        self.info_value.set("{:.2f}".format(gui.collectionData.totals.total_price))

        if gui.collectionData.totals.item_count:
            self.info_average.set("{:.2f}".format(gui.collectionData.totals.total_price/gui.collectionData.totals.item_count))
        else:
            self.info_average.set("{:.2f}".format(0))

        self.info_first.set(gui.collectionData.totals.first.date + "  -  " +
                            gui.collectionData.totals.first.name)
        self.info_last.set(gui.collectionData.totals.last.date + "  -  " +
                            gui.collectionData.totals.last.name)

        if os.path.exists(gui.collectionData.csv_file):
            self.info_update.set(str(datetime.fromtimestamp(os.path.getmtime(gui.collectionData.csv_file))).split(".")[0])

        if gui.collectionData.filterData.groupItems:
            self.info_grp_number_txt.set("Group count:")
            self.info_grp_number.set(str(len(gui.collectionData.groups)))

            self.info_grp_average_txt.set("Avg. group price:")
            self.info_grp_average.set("{:.2f}".format(gui.collectionData.totals.total_price/len(gui.collectionData.groups)))

            self.info_grp_priceLow_txt.set("Lowest group price:")
            self.info_grp_priceLow.set("{:.2f}".format(gui.collectionData.getGroupPriceLow().total_price))
            self.info_grp_priceLow_name.set(" -  " + gui.collectionData.groupKey_priceLow)

            self.info_grp_priceHigh_txt.set("Highest group price:")
            self.info_grp_priceHigh.set("{:.2f}".format(gui.collectionData.getGroupPriceHigh().total_price))
            self.info_grp_priceHigh_name.set(" -  " + gui.collectionData.groupKey_priceHigh)

            self.info_grp_countLow_txt.set("Least group items:")
            self.info_grp_countLow.set(gui.collectionData.getGroupCountLow().item_count)
            self.info_grp_countLow_name.set(" -  " + gui.collectionData.groupKey_countLow)

            self.info_grp_countHigh_txt.set("Most group items:")
            self.info_grp_countHigh.set(gui.collectionData.getGroupCountHigh().item_count)
            self.info_grp_countHigh_name.set(" -  " + gui.collectionData.groupKey_countHigh)
        else:
            self.info_grp_number_txt.set("")
            self.info_grp_number.set("")

            self.info_grp_average_txt.set("")
            self.info_grp_average.set("")

            self.info_grp_priceLow_txt.set("")
            self.info_grp_priceLow.set("")
            self.info_grp_priceLow_name.set("")

            self.info_grp_priceHigh_txt.set("")
            self.info_grp_priceHigh.set("")
            self.info_grp_priceHigh_name.set("")

            self.info_grp_countLow_txt.set("")
            self.info_grp_countLow.set("")
            self.info_grp_countLow_name.set("")

            self.info_grp_countHigh_txt.set("")
            self.info_grp_countHigh.set("")
            self.info_grp_countHigh_name.set("")
