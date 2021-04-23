from tkinter import *
from tkinter import ttk

from VGC_Widgets import Label_
from VGC_Var import IMG_COVER_NONE
from VGC_Var import COVER_WIDTH


######################
# initItemInfo
# --------------------
def initItemInfo(gui):

    # Item info
    # ------------------
    gui.item_spacer    = Label(gui.item_frame, width=2)

    gui.item_title_txt = Label_(gui.item_frame, text="Title", anchor="nw")
    gui.item_title     = Label_(gui.item_frame, anchor="nw", width=22, height=4, wraplength=135)
    gui.item_date_txt  = Label_(gui.item_frame, text="Purchase date", anchor="nw")
    gui.item_date      = Label_(gui.item_frame, anchor="nw", width=22)
    gui.item_price_txt = Label_(gui.item_frame, text="Purchase price", anchor="nw")
    gui.item_price     = Label_(gui.item_frame, anchor="nw", width=22)

    # Front cover widgets
    gui.item_front_txt  = Label_(gui.item_frame, text="Front cover", anchor="w")
    gui.item_front      = Label_(gui.item_frame, anchor="w", imgdef=IMG_COVER_NONE, imgwidth=COVER_WIDTH)
    gui.item_front_upd  = Button(gui.item_front)
    gui.item_front_viw  = Button(gui.item_front)

    # Back cover widgets
    gui.item_back_txt   = Label_(gui.item_frame, text="Back cover", anchor="w")
    gui.item_back       = Label_(gui.item_frame, anchor="w", imgdef=IMG_COVER_NONE, imgwidth=COVER_WIDTH)
    gui.item_back_upd   = Button(gui.item_back)
    gui.item_back_viw   = Button(gui.item_back)

    # Cart cover widgets
    gui.item_cart_txt   = Label_(gui.item_frame, text="Cart cover", anchor="w")
    gui.item_cart       = Label_(gui.item_frame, anchor="w", imgdef=IMG_COVER_NONE, imgwidth=COVER_WIDTH)
    gui.item_cart_upd   = Button(gui.item_cart)
    gui.item_cart_viw   = Button(gui.item_cart)

    gui.item_title_txt.grid(row=1, column=0, columnspan=2, sticky="nwe")
    gui.item_spacer.grid(row=2, column=0, sticky="nwe")
    gui.item_title.grid(row=2, column=1, sticky="nwe")

    gui.item_date_txt.grid(row=3, column=0, columnspan=2, sticky="nwe")
    gui.item_date.grid(row=4, column=1, sticky="nwe")

    gui.item_price_txt.grid(row=5, column=0, columnspan=2, sticky="nwe")
    gui.item_price.grid(row=6, column=1, sticky="nwe")

    gui.item_front_txt.grid(row=7, column=0, columnspan=2, sticky="nwe")
    gui.item_front.grid(row=8, column=1, sticky="nwe")

    gui.item_back_txt.grid(row=9, column=0, columnspan=2, sticky="nwe")
    gui.item_back.grid(row=10, column=1, sticky="nwe")

    gui.item_cart_txt.grid(row=11, column=0, columnspan=2, sticky="nwe")
    gui.item_cart.grid(row=12, column=1, sticky="nwe")

    # Frame for item toolbar
    gui.item_tool_frame = Frame(gui.item_frame , width=200 , height=10 , pady=0 , padx=0)
    gui.item_tool_frame.grid(row=0, column=0, sticky="nwe", columnspan=2)

    # Item Toolbar
    gui.item_open_website = Button(gui.item_tool_frame, relief="groove", image=gui.item_link_ico)
    gui.item_bookmark     = Button(gui.item_tool_frame, relief="groove", image=gui.item_bookmark_ico)
    gui.item_id           = Label_(gui.item_tool_frame)
    gui.item_id.grid(row=0, column=2, sticky="e")

    gui.item_open_website.config(command=gui.openOnVGCollect)
    gui.item_open_website.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

    gui.item_bookmark.config(command=gui.toggleBookmark)
    gui.item_bookmark.grid(row=0, column=1, sticky="nw", padx=(5, 25), pady=5)

    # Position cover toolbars
    gui.placeCoverToolbars()
    gui.showCoverToolbars()