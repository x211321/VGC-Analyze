import threading

from tkinter import *
from tkinter import ttk

from VGC_Widgets        import Label_
from VGC_Img            import loadIcon
from VGC_Browser        import openItemInBrowser
from VGC_Download       import downloadCovers
from gui.VGC_GUI_Popups import Pop_CoverViewer

from VGC_Var import COVER_WIDTH
from VGC_Var import IMG_CACHE_FRONT
from VGC_Var import IMG_CACHE_BACK
from VGC_Var import IMG_CACHE_CART
from VGC_Var import IMG_COVER_NONE


######################
# GUI_ItemInfo
# --------------------
class GUI_ItemInfo(Frame):

    def __init__(self, master, width=0, height=0, pady=0, padx=0):
        super().__init__(master=master, width=width, height=height, pady=pady, padx=padx)

        # Icons
        # ------------------
        self.item_bookmark_ico = loadIcon("bookmark-outline", 15, 15)
        self.item_finished_ico = loadIcon("checkmark-circle-outline", 15, 15)
        self.item_refresh_ico  = loadIcon("refresh-outline", 15, 15)
        self.item_view_ico     = loadIcon("eye-outline", 15, 15)
        self.item_link_ico     = loadIcon("link-outline", 15, 15)

        self.activeItem     = master.activeItem
        self.toggleBookmark = master.toggleBookmark
        self.toggleFinished = master.toggleFinished

        self.pop_coverViewer = Pop_CoverViewer(self)

        self.init()


    def init(self):
        # Item info
        # ------------------
        self.item_spacer    = Label(self, width=2)

        self.item_title_txt = Label_(self, text="Title", anchor="nw")
        self.item_title     = Label_(self, anchor="nw", width=22, height=4, wraplength=135)
        self.item_date_txt  = Label_(self, text="Purchase date", anchor="nw")
        self.item_date      = Label_(self, anchor="nw", width=22)
        self.item_price_txt = Label_(self, text="Purchase price", anchor="nw")
        self.item_price     = Label_(self, anchor="nw", width=22)

        # Front cover widgets
        self.item_front_txt  = Label_(self, text="Front cover", anchor="w")
        self.item_front      = Label_(self, anchor="w", imgdef=IMG_COVER_NONE, imgwidth=COVER_WIDTH)
        self.item_front.bind("<Enter>", lambda x:self.onCoverEnter(self.item_front, "front"))
        self.item_front.bind("<Leave>", lambda x:self.onCoverLeave(self.item_front))

        # Back cover widgets
        self.item_back_txt   = Label_(self, text="Back cover", anchor="w")
        self.item_back       = Label_(self, anchor="w", imgdef=IMG_COVER_NONE, imgwidth=COVER_WIDTH)
        self.item_back.bind("<Enter>", lambda x:self.onCoverEnter(self.item_back, "back"))
        self.item_back.bind("<Leave>", lambda x:self.onCoverLeave(self.item_back))

        # Cart cover widgets
        self.item_cart_txt   = Label_(self, text="Cart cover", anchor="w")
        self.item_cart       = Label_(self, anchor="w", imgdef=IMG_COVER_NONE, imgwidth=COVER_WIDTH)
        self.item_cart.bind("<Enter>", lambda x:self.onCoverEnter(self.item_cart, "cart"))
        self.item_cart.bind("<Leave>", lambda x:self.onCoverLeave(self.item_cart))

        self.item_title_txt.grid(row=1, column=0, columnspan=2, sticky="nwe")
        self.item_spacer.grid(row=2, column=0, sticky="nwe")
        self.item_title.grid(row=2, column=1, sticky="nwe")

        self.item_date_txt.grid(row=3, column=0, columnspan=2, sticky="nwe")
        self.item_date.grid(row=4, column=1, sticky="nwe")

        self.item_price_txt.grid(row=5, column=0, columnspan=2, sticky="nwe")
        self.item_price.grid(row=6, column=1, sticky="nwe")

        self.item_front_txt.grid(row=7, column=0, columnspan=2, sticky="nwe")
        self.item_front.grid(row=8, column=1, sticky="nwe")

        self.item_back_txt.grid(row=9, column=0, columnspan=2, sticky="nwe")
        self.item_back.grid(row=10, column=1, sticky="nwe")

        self.item_cart_txt.grid(row=11, column=0, columnspan=2, sticky="nwe")
        self.item_cart.grid(row=12, column=1, sticky="nwe")

        # Frame for item toolbar
        self.item_tool_frame = Frame(self , width=200 , height=10 , pady=0 , padx=0)
        self.item_tool_frame.grid(row=0, column=0, sticky="nwe", columnspan=2)

        # Item Toolbar
        self.item_open_website = Button(self.item_tool_frame, relief="groove", image=self.item_link_ico)
        self.item_bookmark     = Button(self.item_tool_frame, relief="groove", image=self.item_bookmark_ico)
        self.item_finished     = Button(self.item_tool_frame, relief="groove", image=self.item_finished_ico)
        self.item_id           = Label_(self.item_tool_frame)
        self.item_id.grid(row=0, column=3, sticky="e")

        self.item_open_website.config(command=self.openOnVGCollect)
        self.item_open_website.grid(row=0, column=0, sticky="nw", padx=3, pady=5)

        self.item_bookmark.config(command=self.toggleBookmark)
        self.item_bookmark.grid(row=0, column=1, sticky="nw", padx=(3), pady=5)

        self.item_finished.config(command=self.toggleFinished)
        self.item_finished.grid(row=0, column=2, sticky="nw", padx=(3, 15), pady=5)


    def update(self):
        self.item_title.set(self.activeItem().name)
        self.item_date.set(self.activeItem().date)
        self.item_price.set("{:.2f}".format(self.activeItem().price))
        self.item_id.set("VGC ID: " + str(self.activeItem().VGC_id))

        thread = threading.Thread(target=self.coverUpdateThread, args=(self.activeItem(),))
        thread.start()


    ######################
    # coverUpdateThread
    # --------------------
    def coverUpdateThread(self, item):
        # Update covers
        self.showCovers(item)

        # download covers
        downloadCovers(item)

        if item.VGC_id == self.activeItem().VGC_id:
            # Update covers
            self.showCovers(item)


    ######################
    # onCoverEnter
    # --------------------
    def onCoverEnter(self, label, type):
        self.coverButton_coverViewer = Button(label, bg="white", image=self.item_view_ico,
                                              relief="groove", command=lambda:self.pop_coverViewer.show(type, self.activeItem()))
        self.coverButton_coverViewer.place(height=25, width=25, x=29, y=2)

        self.coverButton_coverUpdate = Button(label, bg="white", image=self.item_refresh_ico,
                                              relief="groove", command=lambda:self.updateCover(type, self.activeItem()))
        self.coverButton_coverUpdate.place(height=25, width=25, x=2, y=2)


    ######################
    # onCoverLeave
    # --------------------
    def onCoverLeave(self, label):
        self.coverButton_coverViewer.destroy()
        self.coverButton_coverUpdate.destroy()


    ######################
    # openOnVGCollect
    # --------------------
    def openOnVGCollect(self):
        if self.activeItem().VGC_id > 0:
            openItemInBrowser(str(self.activeItem().VGC_id))


    ######################
    # showCovers
    # --------------------
    def showCovers(self, item):
        self.item_front.setImage(IMG_CACHE_FRONT + str(item.VGC_id) + ".jpg")
        self.item_back.setImage(IMG_CACHE_BACK + str(item.VGC_id) + ".jpg")
        self.item_cart.setImage(IMG_CACHE_CART + str(item.VGC_id) + ".jpg")


    ######################
    # updateCover
    # --------------------
    def updateCover(self, coverType, item = None):
        if not item == None:
            downloadCovers(item, True, coverType)
            self.update()

