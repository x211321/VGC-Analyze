import lib.Settings as settings
from lib.Locale import _
from lib.Locale import locCurrency
from lib.Locale import locDate

import os
import math
import threading
import platform

from tkinter import *
from tkinter import messagebox

from lib.Widgets    import Frame_
from lib.Widgets    import LabelButton_
from lib.Widgets    import Label_
from lib.Img        import loadIcon
from lib.Browser    import openItemInBrowser
from lib.Browser    import openVGCInBrowser
from lib.Download   import downloadCover
from gui.GUI_Popups import Pop_CoverViewer

import lib.Var as VAR


######################
# GUI_ItemInfo
# --------------------
class GUI_ItemInfo(Frame_):

    def __init__(self, master, width=0, height=0):
        super().__init__(master=master, width=width, height=height, style=VAR.FRAME_STYLE_SECONDARY)

        self.setDefaultLabelStyle(VAR.LABEL_STYLE_SECONDARY)

        # Icons
        # ------------------
        self.item_bookmark_ico = loadIcon("bookmark-outline", 15, 15)
        self.item_finished_ico = loadIcon("checkmark-circle-outline", 15, 15)
        self.item_link_ico     = loadIcon("link-outline", 15, 15)
        self.item_refresh_ico  = loadIcon("refresh-outline", 15, 15)
        self.item_view_ico     = loadIcon("eye-outline", 15, 15)

        self.activeItemIndex             = master.activeItemIndex
        self.activeItem                  = master.activeItem
        self.toggleBookmark              = master.toggleBookmark
        self.toggleFinished              = master.toggleFinished
        self.getOnlineCollectionListPage = master.getOnlineCollectionListPage

        self.pop_coverViewer = Pop_CoverViewer(self)

        self.init()


    def init(self):
        # Item info
        # ------------------
        self.item_spacer    = Label_(self, width=2)

        if platform.system() == "Linux":
            labelWidth = 16
        else:
            labelWidth = 22

        self.item_title_txt     = Label_(self, text=_("Title"), anchor="nw")
        self.item_title         = Label_(self, anchor="nw", width=labelWidth, wraplength=135)
        self.item_date_txt      = Label_(self, text=_("Date (purchased)"), anchor="nw")
        self.item_date          = Label_(self, anchor="nw", width=labelWidth)
        self.item_dateAdded_txt = Label_(self, text=_("Date (added)"), anchor="nw")
        self.item_dateAdded     = Label_(self, anchor="nw", width=labelWidth)
        self.item_price_txt     = Label_(self, text=_("Purchase price"), anchor="nw")
        self.item_price         = Label_(self, anchor="nw", width=labelWidth)

        # Front cover widgets
        self.item_front_txt  = Label_(self, text=_("Front cover"), anchor="w")
        self.item_front      = Label_(self, anchor="w", _imgdef=VAR.IMG_COVER_NONE, _imgwidth=VAR.COVER_WIDTH)
        self.item_front.bind("<Enter>", lambda x:self.onCoverEnter(self.item_front, VAR.COVER_TYPE_FRONT))
        self.item_front.bind("<Leave>", lambda x:self.onCoverLeave(self.item_front))

        # Back cover widgets
        self.item_back_txt   = Label_(self, text=_("Back cover"), anchor="w")
        self.item_back       = Label_(self, anchor="w", _imgdef=VAR.IMG_COVER_NONE, _imgwidth=VAR.COVER_WIDTH)
        self.item_back.bind("<Enter>", lambda x:self.onCoverEnter(self.item_back, VAR.COVER_TYPE_BACK))
        self.item_back.bind("<Leave>", lambda x:self.onCoverLeave(self.item_back))

        # Cart cover widgets
        self.item_cart_txt   = Label_(self, text=_("Cart cover"), anchor="w")
        self.item_cart       = Label_(self, anchor="w", _imgdef=VAR.IMG_COVER_NONE, _imgwidth=VAR.COVER_WIDTH)
        self.item_cart.bind("<Enter>", lambda x:self.onCoverEnter(self.item_cart, VAR.COVER_TYPE_CART))
        self.item_cart.bind("<Leave>", lambda x:self.onCoverLeave(self.item_cart))

        self.item_title_txt.grid(row=1, column=0, columnspan=2, sticky="nwe", pady=(5,0))
        self.item_spacer.grid(row=2, column=0, sticky="nwe")
        self.item_title.grid(row=2, column=1, sticky="nwe", padx=(0,10))

        self.item_date_txt.grid(row=3, column=0, columnspan=2, sticky="nwe", pady=(5,0))
        self.item_date.grid(row=4, column=1, sticky="nwe")

        self.item_dateAdded_txt.grid(row=5, column=0, columnspan=2, sticky="nwe", pady=(5,0))
        self.item_dateAdded.grid(row=6, column=1, sticky="nwe")

        self.item_price_txt.grid(row=7, column=0, columnspan=2, sticky="nwe", pady=(5,0))
        self.item_price.grid(row=8, column=1, sticky="nwe")

        self.item_front_txt.grid(row=9, column=0, columnspan=2, sticky="nwe", pady=(5,0))
        self.item_front.grid(row=10, column=1, sticky="nwe")

        self.item_back_txt.grid(row=11, column=0, columnspan=2, sticky="nwe", pady=(5,0))
        self.item_back.grid(row=12, column=1, sticky="nwe")

        self.item_cart_txt.grid(row=13, column=0, columnspan=2, sticky="nwe", pady=(5,0))
        self.item_cart.grid(row=14, column=1, sticky="nwe")

        # Frame for item toolbar
        self.item_tool_frame = Frame_(self , width=200 , height=10, style=VAR.FRAME_STYLE_SECONDARY)
        self.item_tool_frame.grid(row=0, column=0, sticky="nwe", columnspan=2, pady=0 , padx=(0,10))

        # Item Toolbar
        self.item_open_website = LabelButton_(self.item_tool_frame, image=self.item_link_ico, command=self.openOnVGCollect)
        self.item_bookmark     = LabelButton_(self.item_tool_frame, image=self.item_bookmark_ico, command=self.toggleBookmark)
        self.item_finished     = LabelButton_(self.item_tool_frame, image=self.item_finished_ico, command=self.toggleFinished)
        self.item_id           = Label_(self.item_tool_frame)
        self.item_spacer       = Label_(self.item_tool_frame)

        self.item_tool_frame.columnconfigure(0, weight=1)

        self.item_open_website.grid(row=0, column=1, sticky="ne", padx=3, pady=5)
        self.item_bookmark.grid(row=0, column=2, sticky="ne", padx=(3,0), pady=5)
        self.item_finished.grid(row=0, column=3, sticky="ne", padx=(3,0), pady=5)

        self.item_spacer.grid(row=1, column=0)
        self.item_id.grid(row=1, column=1, columnspan=4, sticky="e", padx=(3,0))


    ######################
    # update
    # --------------------
    def update(self, refresh = False):
        # Show basic item data
        self.item_title.set(self.activeItem().name)
        self.item_date.set(locDate(self.activeItem().date, showDay=True))
        self.item_dateAdded.set(locDate(self.activeItem().dateAdded, showDay=True))
        self.item_price.set(locCurrency(self.activeItem().price))
        self.item_id.set("VGC ID: " + str(self.activeItem().VGC_id))

        # Update front cover
        self.updateCover(self.activeItem(), VAR.COVER_TYPE_FRONT, self.item_front, refresh)

        # Update back cover
        self.updateCover(self.activeItem(), VAR.COVER_TYPE_BACK, self.item_back, refresh)

        # Update cart cover
        self.updateCover(self.activeItem(), VAR.COVER_TYPE_CART, self.item_cart, refresh)


    ######################
    # updateCover
    # --------------------
    def updateCover(self, item, coverType, widget, refresh = False):
        # Run cover update thread
        thread = threading.Thread(target=self.coverUpdateThread, args=(item, coverType, widget, refresh))
        thread.start()


    ######################
    # coverUpdateThread
    # --------------------
    def coverUpdateThread(self, item, coverType, widget, refresh):

        coverCached = False

        # Check if cover already cached
        if os.path.exists(VAR.getCoverPath(item, coverType)) or item.getLocalData("missingCover" + coverType):
            coverCached = True

        # Show currently known cover
        if coverCached or settings.get("display", "hideCoverLoadingAnimation", False):
            self.showCover(item, coverType, widget)

        # When the cover is not cached or shall be refreshed
        if coverCached == False or refresh:
            # Start loading animation
            if not settings.get("display", "hideCoverLoadingAnimation", False):
                widget.startAnimation(VAR.IMG_COVER_LOADING_120, 12, 100)

            # Download cover
            downloadCover(item, coverType, refresh)

            # Stop loading animation
            if not settings.get("display", "hideCoverLoadingAnimation", False):
                widget.stopAnimation()

        # Finally show the updated cover
        # but only if the user hasn not switched to another
        # entry since the download was initiated
        if item.VGC_id == self.activeItem().VGC_id:
            self.showCover(item, coverType, widget)


    ######################
    # onCoverEnter
    # --------------------
    def onCoverEnter(self, label, type):
        self.coverButton_coverViewer = LabelButton_(label, image=self.item_view_ico,
                                                    command=lambda:self.pop_coverViewer.show(type, self.activeItem()))
        self.coverButton_coverViewer.place(height=35, width=35, x=39, y=2)

        self.coverButton_coverUpdate = LabelButton_(label, image=self.item_refresh_ico,
                                                    command=lambda:self.updateCover(self.activeItem(), type, label, True))
        self.coverButton_coverUpdate.place(height=35, width=35, x=2, y=2)


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
    # openVGCollectCollectionList
    # --------------------
    def openVGCollectCollectionList(self):
        username = settings.get("vgc", "username", "")

        if self.activeItem().VGC_id > 0:
            if len(username) == 0:
                messagebox.showinfo("VGC Analyze",
                                  _("A VGCollect.com username is needed to access the online collection list.\n\n") +
                                  _("Please provide a username at File > Settings > VGC"))
            else:
                page     = math.ceil((self.activeItemIndex()+1) / 25)
                pageData = self.getOnlineCollectionListPage(username, str(page))

                idStart  = pageData.find("item_" + str(self.activeItem().VGC_id) + "_")
                idEnd    = pageData.find("\"", idStart)
                id       = pageData[idStart:idEnd]

                openVGCInBrowser(username + "/" + str(page) + "#" + id)


    ######################
    # showCover
    # --------------------
    def showCover(self, item, coverType, widget):
        widget.setImage(VAR.getCoverPath(item, coverType))

