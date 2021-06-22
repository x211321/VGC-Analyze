from lib.Locale import _

import os
import platform

from tkinter import *
from tkinter import messagebox

from datetime import date
import calendar

import lib.Var as VAR

from lib.Img import loadIcon

from lib.Widgets  import Label_
from lib.Widgets  import Entry_
from lib.Widgets  import Button_
from lib.Widgets  import BorderButton_
from lib.Browser  import openUserProfileInBrowser
from lib.Browser  import openGithub
from lib.Download import downloadCollection


######################
# initPopups
# --------------------
def initPopups(gui):
    gui.pop_collectionDownload = Pop_CollectionDownload(gui, gui.collectionDownload_callback)
    gui.pop_itemSearch         = Pop_ItemSearch(gui, gui.view_frame.item_view)
    gui.pop_itemDetails        = Pop_ItemDetails(gui)
    gui.pop_about              = Pop_About(gui)


######################
# centerPopup
# --------------------
def centerPopup(window, parent):
    # Update window
    window.update()

    # Get window size
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()

    # Calculate position relative to main parent
    x = int(parent.winfo_x() + (parent.winfo_width() / 2) - (w / 2))
    y = int(parent.winfo_y() + (parent.winfo_height() / 2) - (h / 2))

    # Position window
    window.geometry("{0}x{1}+{2}+{3}".format(w, h, x, y))


######################
# Pop_CoverViewer
# --------------------
class Pop_CoverViewer(object):

    window = None

    def __init__(self, parent):
        self.parent    = parent
        self.coverSize = 500

    def show(self, coverType, item = None):

        self.close()

        if not item == None:
            # Get cover path
            if coverType == "front":
                img = VAR.IMG_CACHE_FRONT + str(item.VGC_id) + ".jpg"
                title = _("front cover")
            if coverType == "back":
                img = VAR.IMG_CACHE_BACK + str(item.VGC_id) + ".jpg"
                title = _("back cover")
            if coverType == "cart":
                img = VAR.IMG_CACHE_CART + str(item.VGC_id) + ".jpg"
                title = _("cart cover")

            if os.path.exists(img):

                # Calculate position relative to main parent
                x = self.parent.winfo_x() + self.parent.winfo_width() - 210 - self.coverSize
                y = self.parent.winfo_y() + 50

                # Create new window
                self.window = Toplevel(bg=VAR.GUI_COLOR_PRIMARY)
                self.window.wm_title(item.name + " - " + title)
                self.window.geometry("+"+str(x)+"+"+str(y))
                self.window.resizable(False, False)

                if not platform.system() == "Darwin":
                    self.window.iconphoto(False, loadIcon("eye-outline", 512, 512))
                self.window.bind('<Escape>', lambda x:self.close())
                self.window.focus_force()

                # Create and place cover label
                coverViewer_cover = Label_(self.window, img=img, imgwidth=self.coverSize)
                coverViewer_cover.pack(expand="Yes")

                # Run main loop of new window
                self.window.mainloop()

    def close(self):
        if not self.window == None:
            self.window.destroy()


######################
# Pop_CollectionDownload
# --------------------
class Pop_CollectionDownload(object):

    window   = None
    parent   = None
    callback = None

    def __init__(self, parent, callback = None):
        self.parent   = parent
        self.callback = callback

    def show(self):

        self.close()

        # Create new window
        self.window = Toplevel(bg=VAR.GUI_COLOR_PRIMARY)
        self.window.withdraw()
        self.window.wm_title(_("Download collection"))
        self.window.resizable(False, False)

        if not platform.system() == "Darwin":
            self.window.iconphoto(False, loadIcon("cloud-download-outline", 512, 512))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        self.window.columnconfigure(0, weight=1)

        # Functions
        # ------------------
        self.input_frame  = Frame(self.window, bg=VAR.GUI_COLOR_PRIMARY)
        self.button_frame = Frame(self.window, bg=VAR.GUI_COLOR_SECONDARY)

        self.input_frame.grid(row=0, column=0, sticky="nwse")
        self.button_frame.grid(row=1, column=0, sticky="nwse")

        self.button_frame.columnconfigure(1, weight=1)

        self.label_user       = Label_(self.input_frame, anchor="w", text=_("VGC Username"), bg=VAR.GUI_COLOR_PRIMARY)
        self.input_user       = Entry_(self.input_frame, width=31, relief="solid")
        self.label_pass       = Label_(self.input_frame, anchor="w", text=_("Password"), bg=VAR.GUI_COLOR_PRIMARY)
        self.input_pass       = Entry_(self.input_frame, width=31, relief="solid", show="*")
        self.btn_cancel       = Button_(self.button_frame, width=18, text=_("Cancel"), relief="groove", bg=VAR.BUTTON_COLOR_BAD, command=self.close)
        self.btn_spacer       = Label_(self.button_frame, bg=VAR.GUI_COLOR_SECONDARY)
        self.btn_download     = Button_(self.button_frame, width=18, text=_("Download"), relief="groove", bg=VAR.BUTTON_COLOR_GOOD, command=self.download)
        self.label_disclaimer = Label_(self.button_frame, width=35, bg=VAR.GUI_COLOR_SECONDARY)
        self.label_info       = Label_(self.button_frame, width=35, bg=VAR.GUI_COLOR_SECONDARY)
        self.label_link       = Label_(self.button_frame, width=35, anchor="center", bg=VAR.GUI_COLOR_SECONDARY)

        self.label_user.grid(row=0, column=0, pady=(15,10), padx=10, sticky="w")
        self.input_user.grid(row=0, column=1, pady=(15,10), padx=10, sticky="w")

        self.label_pass.grid(row=1, column=0, pady=(0,10), padx=10, sticky="w")
        self.input_pass.grid(row=1, column=1, pady=(0,15), padx=10, sticky="w")

        self.btn_cancel.grid(row=0, column=0, pady=20, padx=10, sticky="e")
        self.btn_spacer.grid(row=0, column=1)
        self.btn_download.grid(row=0, column=2, pady=20, padx=10, sticky="w")

        self.label_disclaimer.grid(row=1, column=0, pady=0, padx=10, sticky="nwse", columnspan=3)
        self.label_info.grid(row=2, column=0, pady=0, padx=10, sticky="nwse", columnspan=3)
        self.label_link.grid(row=3, column=0, pady=(5, 10), padx=10, sticky="nwse", columnspan=3)

        self.label_disclaimer.set(_("VGC Analyze is an unofficial project, \nnot affiliated with or endorsed by VGCollect.com."))
        self.label_disclaimer.config(fg="red")

        self.label_info.set(_("The provided login credentials will be used to\n"
                              "download a backup of your collection from\n"
                              "your VGCollect.com user profile.\n\n"
                              "Your login information will not be saved or used\n"
                              "for any other purpose.\n\n"
                              "You can also provide your collection data manually:\n\n"
                              " 1) \tExport your collection from your\n"
                              "\tVGCollect.com user profile\n\n"
                              " 2) \tPlace the resulting file into the\n"
                              "\tVGC Analyze data folder\n\n"
                              " 3) \tRestart VGC Analyzer"))

        self.label_link.set(_("VGCollect.com user profile"))
        self.label_link.config(fg="blue", cursor="hand2")
        self.label_link.bind("<Button-1>", openUserProfileInBrowser)

        self.input_pass.bind('<Return>', self.download)

        self.input_user.focus()

        self.center()

        self.window.deiconify()

        # Run main loop of new window
        self.window.mainloop()

    def center(self):
        centerPopup(self.window, self.parent)

    def close(self):
        if not self.window == None:
            self.window.destroy()

    def setCallback(self, callback):
        self.callback = callback

    def download(self, a = None):
        user     = self.input_user.get()
        password = self.input_pass.get()

        if len(user) == 0 or len(password) == 0:
            messagebox.showerror(_("Collection download"), _("Login credentials incomplete"), parent=self.window)
            return

        result, path = downloadCollection(user, password)

        if result == None:
            self.window.destroy()
            messagebox.showinfo(_("Collection download"), _("Download successful"), parent=self.parent)

            if not self.callback == None:
                self.callback(result, path)
        else:
            messagebox.showerror(_("Collection download"), result, parent=self.window)


######################
# Pop_ItemSearch
# --------------------
class Pop_ItemSearch(object):

    window     = None
    callback   = None

    def __init__(self, parent, treeView, callback = None):
        self.parent   = parent
        self.treeView = treeView
        self.callback = callback

    def show(self):

        # Get selected row
        selection = self.treeView.focus()

        if len(selection):
            self.startIndex = self.treeView.index(selection)
        else:
            self.startIndex = -1

        # Close previous window
        self.close()

        # Create new window
        self.window = Toplevel(bg=VAR.GUI_COLOR_PRIMARY)
        self.window.withdraw()
        self.window.wm_title(_("Search for item"))
        self.window.resizable(False, False)

        if not platform.system() == "Darwin":
            self.window.iconphoto(False, loadIcon("search-outline", 512, 512))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        # Functions
        # ------------------
        self.input_frame  = Frame(self.window, bg=VAR.GUI_COLOR_PRIMARY)
        self.button_frame = Frame(self.window, bg=VAR.GUI_COLOR_SECONDARY)

        self.input_frame.grid(row=0, column=0, sticky="nwse")
        self.button_frame.grid(row=1, column=0, sticky="nwse")

        self.button_frame.columnconfigure(1, weight=1)

        self.label_search = Label_(self.input_frame, anchor="w", text=_("Search for"), bg=VAR.GUI_COLOR_PRIMARY)
        self.input_search = Entry_(self.input_frame, width=35, relief="solid")
        self.label_info   = Label_(self.input_frame, width=35, anchor="w", fg="#F00", bg=VAR.GUI_COLOR_PRIMARY)

        self.btn_cancel   = Button_(self.button_frame, width=15, text=_("Cancel"), relief="groove", bg=VAR.BUTTON_COLOR_BAD, command=self.close)
        self.btn_spacer   = Label_(self.button_frame, bg=VAR.GUI_COLOR_SECONDARY)
        self.btn_search   = Button_(self.button_frame, width=15, text=_("Search"), relief="groove", bg=VAR.BUTTON_COLOR_GOOD, command=self.search)

        self.label_search.grid(row=0, column=0, pady=(15,10), padx=(15, 5), sticky="w")
        self.input_search.grid(row=0, column=1, pady=(15,10), padx=(5, 15), sticky="w")
        self.label_info.grid(row=1, column=0, pady=(0, 10), padx=15, sticky="nwse", columnspan=2)

        self.btn_cancel.grid(row=2, column=0, pady=20, padx=15, sticky="e")
        self.btn_spacer.grid(row=2, column=1)
        self.btn_search.grid(row=2, column=2, pady=20, padx=15, sticky="w")

        self.input_search.bind('<Return>', self.search)
        self.input_search.focus()

        self.center()

        self.window.deiconify()

        # Run main loop of new window
        self.window.mainloop()

    def center(self):
        centerPopup(self.window, self.parent)

    def close(self):
        if not self.window == None:
            self.window.destroy()

    def setCallback(self, callback):
        self.callback = callback

    def search(self, a = None):

        # Read user input
        searchString = self.input_search.get()

        # Reset info label
        self.label_info.set("")

        # Clear row IDs
        rowIDs = []

        if len(searchString.strip()) > 0:
            index = self.startIndex
            found = False

            for item in self.treeView.get_children():
                # When data is grouped
                if item[0] == "#":
                    # Iterate child elements
                    for child in self.treeView.get_children(item):
                        rowIDs.append(child)
                else:
                    rowIDs.append(item)

            while True:
                index += 1

                if index > len(rowIDs)-1:
                    index = 0
                    if self.startIndex == -1:
                        break

                if searchString.lower() in self.treeView.item(rowIDs[index])["values"][2].lower():
                    found           = True
                    self.startIndex = index
                    break

                if index == self.startIndex:
                    break

            if found:
                # Select row in treeview
                self.treeView.focus(str(rowIDs[index]))
                self.treeView.selection_set(str(rowIDs[index]))
                self.treeView.see(str(rowIDs[index]))
            else:
                # Show error
                self.label_info.set(_("Couldn't find") + " \"" + searchString + "\"")

            if not self.callback == None:
                self.callback(found, index)


######################
# Pop_FilterSelect
# --------------------
class Pop_FilterSelect(object):

    window = None

    def __init__(self, parent, callback = None):

        self.parent   = parent
        self.callback = callback

    def show(self, options, activeOptions, filterType, maxCol = 0):
        # Close previous window
        self.close()

        # Create new window
        self.window = Toplevel(bg=VAR.GUI_COLOR_PRIMARY)
        self.window.withdraw()
        self.window.wm_title(_("Select ") + filterType)
        self.window.resizable(False, False)

        if not platform.system() == "Darwin":
            self.window.iconphoto(False, loadIcon("filter-outline", 512, 512))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        self.frame_options = Frame(self.window, bg=VAR.GUI_COLOR_PRIMARY)
        self.frame_buttons = Frame(self.window, bg=VAR.GUI_COLOR_SECONDARY)

        self.frame_options.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        self.frame_buttons.grid(row=1, column=0, sticky="nesw")

        self.btn_cancel= Button_(self.frame_buttons, width=20, text=_("Cancel"), relief="groove", command=self.close, bg=VAR.BUTTON_COLOR_BAD)
        self.btn_reset = Button_(self.frame_buttons, width=20, text=_("Reset"), relief="groove", command=self.reset, bg=VAR.INPUT_COLOR)
        self.btn_all   = Button_(self.frame_buttons, width=20, text=_("Select all"), relief="groove", command=self.selectAll, bg=VAR.INPUT_COLOR)
        self.btn_ok    = Button_(self.frame_buttons, width=20, text=_("OK"), relief="groove", command=self.confirm, bg=VAR.BUTTON_COLOR_GOOD)

        self.btn_cancel.grid(row=0, column=0, padx=10, pady=20, sticky="w")
        self.btn_reset.grid(row=0, column=1, padx=10, pady=20, sticky="w")
        self.btn_all.grid(row=0, column=2, padx=10, pady=20, sticky="e")
        self.btn_ok.grid(row=0, column=3, padx=10, pady=20, sticky="e")

        self.frame_buttons.columnconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(3, weight=1)

        row = 0
        col = 0

        self.widgets = {}

        # Options
        # ------------------

        # Find longest text
        maxLen = 0

        for option, data in options:
            if len(option) > maxLen:
                maxLen = len(option)

        if maxCol == 0:
            maxCol = int(150 / maxLen)

        # Create togglebuttons
        for option, data in options:
            self.widgets[option] = BorderButton_(self.frame_options, text=option, bg=VAR.GUI_COLOR_PRIMARY, width=maxLen, relief="groove", toggle=True)
            self.widgets[option].grid(row=row, column=col, sticky="w", padx=5, pady=5)

            if option in activeOptions:
                self.widgets[option].setToggle(True)

            col += 1

            if col > maxCol:
                col  = 0
                row += 1

        # Center window
        self.center()

        # Show window
        self.window.deiconify()

        # Run main loop of new window
        self.window.mainloop()

    def center(self):
        centerPopup(self.window, self.parent)

    def close(self):
        if not self.window == None:
            self.window.destroy()

    def reset(self):
        for widget in self.widgets:
            self.widgets[widget].setToggle(False)

    def selectAll(self):
        for widget in self.widgets:
            self.widgets[widget].setToggle(True)

    def confirm(self):
        selectedOptions = []

        for widget in self.widgets:
            if self.widgets[widget].toggleState == True:
                selectedOptions.append(widget)

        if not self.callback == None:
            self.callback(selectedOptions)

        self.close()


######################
# Pop_ItemDetails
# --------------------
class Pop_ItemDetails(object):

    window = None

    def __init__(self, parent):

        self.parent = parent
        self.getOnlineItemData = parent.getOnlineItemData

    def show(self, item):
        self.item = item

        # Close previous window
        self.close()

        # Create new window
        self.window = Toplevel(bg=VAR.GUI_COLOR_PRIMARY)
        self.window.withdraw()
        self.window.wm_title(_("Detailed item info for ") + self.item.name)
        self.window.resizable(False, False)

        if not platform.system() == "Darwin":
            self.window.iconphoto(False, loadIcon("information-outline", 512, 512))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        self.container       = Frame(self.window, bg=VAR.GUI_COLOR_PRIMARY)
        self.titleFrame      = Frame(self.container, bg=VAR.GUI_COLOR_PRIMARY)
        self.infoframe_      = Frame(self.container, bg=VAR.GUI_COLOR_PRIMARY, highlightthickness=1, highlightbackground="black")
        self.infoFrame       = Frame(self.infoframe_, bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfoFrame_= Frame(self.container, bg=VAR.GUI_COLOR_PRIMARY, highlightthickness=1, highlightbackground="black")
        self.onlineInfoFrame = Frame(self.onlineInfoFrame_, bg=VAR.GUI_COLOR_PRIMARY)
        self.coverFrame      = Frame(self.container, bg=VAR.GUI_COLOR_PRIMARY)
        self.buttonFrame     = Frame(self.container, bg=VAR.GUI_COLOR_SECONDARY)

        self.container.grid(row=0, column=0, sticky="nwse")
        self.titleFrame.grid(row=0, column=0, sticky="nw", padx=20, pady=5, columnspan=2)
        self.infoframe_.grid(row=1, column=0, sticky="nw", padx=(20,5), pady=5)
        self.infoFrame.grid(row=0, column=0, sticky="nwse", padx=10, pady=10)
        self.onlineInfoFrame_.grid(row=2, column=0, sticky="nw", padx=(20,5), pady=(5,15))
        self.onlineInfoFrame.grid(row=0, column=0, sticky="nwse", padx=10, pady=10)
        self.coverFrame.grid(row=1, column=1, sticky="nw", padx=(5,20), pady=(5,20), rowspan=2)
        self.buttonFrame.grid(row=3, column=0, sticky="nwse", columnspan=2)

        # Title
        self.info_name = Label_(self.titleFrame, bg=VAR.GUI_COLOR_PRIMARY, text=self.item.name, font=(15))
        self.info_name.grid(row=0, column=0, sticky="nw", columnspan=2)

        # Info
        self.info_platform_txt       = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=_("Platform"))
        self.info_platform           = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=self.item.platform)
        self.info_region_txt         = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=_("Region"))
        self.info_region             = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=self.item.region)
        self.info_platformHolder_txt = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=_("Platform holder"))
        self.info_platformHolder     = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=self.item.platformHolder)
        self.info_price_txt          = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=_("Purchase price"))
        self.info_price              = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=self.item.price)
        self.info_date_txt           = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=_("Purchased"))
        self.info_date               = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=self.item.date)
        self.info_dateAdded_txt      = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=_("Added"))
        self.info_dateAdded          = Label_(self.infoFrame, bg=VAR.GUI_COLOR_PRIMARY, text=self.item.dateTimeAdded)

        self.info_platform_txt.grid(row=1, column=0, sticky="nw")
        self.info_platform.grid(row=1, column=1, sticky="nw")
        self.info_region_txt.grid(row=2, column=0, sticky="nw")
        self.info_region.grid(row=2, column=1, sticky="nw")
        self.info_platformHolder_txt.grid(row=3, column=0, sticky="nw")
        self.info_platformHolder.grid(row=3, column=1, sticky="nw")
        self.info_price_txt.grid(row=4, column=0, sticky="nw")
        self.info_price.grid(row=4, column=1, sticky="nw")
        self.info_date_txt.grid(row=5, column=0, sticky="nw")
        self.info_date.grid(row=5, column=1, sticky="nw")
        self.info_dateAdded_txt.grid(row=6, column=0, sticky="nw")
        self.info_dateAdded.grid(row=6, column=1, sticky="nw")

        # Online info
        self.button_getOnlineInfo        = Button_(self.onlineInfoFrame, text=_("Get VGC data"), bg=VAR.GUI_COLOR_PRIMARY, width=25, relief="groove", command=self.getOnline)
        self.onlineInfo_altname_text     = Label_(self.onlineInfoFrame, text=_("Alt-Name"), bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_altname          = Label_(self.onlineInfoFrame, bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_releasetype_text = Label_(self.onlineInfoFrame, text=_("Release Type"), bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_releasetype      = Label_(self.onlineInfoFrame, bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_developer_text   = Label_(self.onlineInfoFrame, text=_("Developer(s)"), bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_developer        = Label_(self.onlineInfoFrame, bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_publisher_text   = Label_(self.onlineInfoFrame, text=_("Publisher(s)"), bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_publisher        = Label_(self.onlineInfoFrame, bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_genre_text       = Label_(self.onlineInfoFrame, text=_("Genre"), bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_genre            = Label_(self.onlineInfoFrame, bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_rating_text      = Label_(self.onlineInfoFrame, text=_("Rating"), bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_rating           = Label_(self.onlineInfoFrame, bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_itemnumber_text  = Label_(self.onlineInfoFrame, text=_("Item Number"), bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_itemnumber       = Label_(self.onlineInfoFrame, bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_barcode_text     = Label_(self.onlineInfoFrame, text=_("Barcode"), bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_barcode          = Label_(self.onlineInfoFrame, bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_releasedate_text = Label_(self.onlineInfoFrame, text=_("Release Date"), bg=VAR.GUI_COLOR_PRIMARY)
        self.onlineInfo_releasedate      = Label_(self.onlineInfoFrame, bg=VAR.GUI_COLOR_PRIMARY)

        self.showOnline()

        # Covers
        self.cover_front = Label_(self.coverFrame, imgdef=VAR.IMG_COVER_NONE, imgwidth=VAR.COVER_WIDTH*2)
        self.cover_back  = Label_(self.coverFrame, imgdef=VAR.IMG_COVER_NONE, imgwidth=VAR.COVER_WIDTH*2)
        self.cover_cart  = Label_(self.coverFrame, imgdef=VAR.IMG_COVER_NONE, imgwidth=VAR.COVER_WIDTH*2)

        if os.path.exists(VAR.IMG_CACHE_FRONT + str(self.item.VGC_id) + ".jpg"):
            self.cover_front.setImage(VAR.IMG_CACHE_FRONT + str(self.item.VGC_id) + ".jpg")
            self.cover_front.grid(row=0, column=0, padx=5, sticky="nw")
        if os.path.exists(VAR.IMG_CACHE_BACK + str(self.item.VGC_id) + ".jpg"):
            self.cover_back.setImage(VAR.IMG_CACHE_BACK + str(self.item.VGC_id) + ".jpg")
            self.cover_back.grid(row=0, column=1, padx=5, sticky="nw")
        if os.path.exists(VAR.IMG_CACHE_CART + str(self.item.VGC_id) + ".jpg"):
            self.cover_cart.setImage(VAR.IMG_CACHE_CART + str(self.item.VGC_id) + ".jpg")
            self.cover_cart.grid(row=0, column=2, padx=5, sticky="nw")

        # Buttons
        self.buttonFrame.columnconfigure(0, weight=1)
        self.button_close = Button_(self.buttonFrame, text="Close", width=25, command=self.close, bg=VAR.GUI_COLOR_PRIMARY, relief="groove")
        self.button_close.grid(row=0, column=0, padx=10, pady=20)

        # Center window
        self.center()

        # Show window
        self.window.deiconify()

        # Run main loop of new window
        self.window.mainloop()

    def center(self):
        centerPopup(self.window, self.parent)

    def close(self):
        if not self.window == None:
            self.window.destroy()

    def getOnline(self):
        self.item.onlineData = self.getOnlineItemData()

        self.showOnline()

    def showOnline(self):
        if len(self.item.onlineData):
            self.onlineInfo_altname.set(self.item.getOnlineData("Alt-Name"))
            self.onlineInfo_releasetype.set(self.item.getOnlineData("Release Type"))
            self.onlineInfo_developer.set(self.item.getOnlineData("Developer(s)"))
            self.onlineInfo_publisher.set(self.item.getOnlineData("Publisher(s)"))
            self.onlineInfo_genre.set(self.item.getOnlineData("Genre"))
            self.onlineInfo_rating.set(self.item.getOnlineData("Rating"))
            self.onlineInfo_itemnumber.set(self.item.getOnlineData("Item Number"))
            self.onlineInfo_barcode.set(self.item.getOnlineData("Barcode"))
            self.onlineInfo_releasedate.set(self.item.getOnlineData("Release Date"))
            self.button_getOnlineInfo.config(text=_("Refresh VGC data"))

            self.onlineInfo_altname_text.grid(row=0, column=0, sticky="nw")
            self.onlineInfo_altname.grid(row=0, column=1, sticky="nw")
            self.onlineInfo_releasetype_text.grid(row=1, column=0, sticky="nw")
            self.onlineInfo_releasetype.grid(row=1, column=1, sticky="nw")
            self.onlineInfo_developer_text.grid(row=2, column=0, sticky="nw")
            self.onlineInfo_developer.grid(row=2, column=1, sticky="nw")
            self.onlineInfo_publisher_text.grid(row=3, column=0, sticky="nw")
            self.onlineInfo_publisher.grid(row=3, column=1, sticky="nw")
            self.onlineInfo_genre_text.grid(row=4, column=0, sticky="nw")
            self.onlineInfo_genre.grid(row=4, column=1, sticky="nw")
            self.onlineInfo_rating_text.grid(row=5, column=0, sticky="nw")
            self.onlineInfo_rating.grid(row=5, column=1, sticky="nw")
            self.onlineInfo_itemnumber_text.grid(row=6, column=0, sticky="nw")
            self.onlineInfo_itemnumber.grid(row=6, column=1, sticky="nw")
            self.onlineInfo_barcode_text.grid(row=7, column=0, sticky="nw")
            self.onlineInfo_barcode.grid(row=7, column=1, sticky="nw")
            self.onlineInfo_releasedate_text.grid(row=8, column=0, sticky="nw")
            self.onlineInfo_releasedate.grid(row=8, column=1, sticky="nw")
            self.button_getOnlineInfo.grid(row=9, column=0, columnspan=2, sticky="nwse", pady=(10,0))

            self.window.update()
            self.window.geometry("{0}x{1}".format(self.container.winfo_reqwidth(), self.container.winfo_reqheight()))
            self.center()
        else:
            self.button_getOnlineInfo.grid(row=0, column=0, sticky="nwse")


######################
# Pop_About
# --------------------
class Pop_About(object):

    window   = None
    parent   = None

    def __init__(self, parent):
        self.parent = parent

    def show(self):

        self.close()

        # Create new window
        self.window = Toplevel(bg=VAR.GUI_COLOR_PRIMARY)
        self.window.withdraw()
        self.window.wm_title(_("About VGC Analyze"))
        self.window.resizable(False, False)

        if not platform.system() == "Darwin":
            self.window.iconphoto(False, loadIcon("game-controller-outline", 512, 512))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        self.window.columnconfigure(0, weight=1)

        # Functions
        # ------------------
        self.label_frame  = Frame(self.window, bg=VAR.GUI_COLOR_PRIMARY)
        self.button_frame = Frame(self.window, bg=VAR.GUI_COLOR_SECONDARY)

        self.label_frame.grid(row=0, column=0, sticky="nwse")
        self.button_frame.grid(row=1, column=0, sticky="nwse")

        self.button_frame.columnconfigure(0, weight=1)

        self.label_title = Label_(self.label_frame, text="VGC Analyzer", font=(20), bg=VAR.GUI_COLOR_PRIMARY)
        self.label_description = Label_(self.label_frame, text=_("A data analyzer for your VGCollect.com video game collection"), bg=VAR.GUI_COLOR_PRIMARY)
        self.label_disclamer = Label_(self.label_frame, text=_("VGC Analyze is a hobby project, not affiliated with or endorsed by VGCollect.com"), bg=VAR.GUI_COLOR_PRIMARY)
        self.label_license = Label_(self.label_frame, bg=VAR.GUI_COLOR_PRIMARY)
        self.label_link = Label_(self.label_frame, bg=VAR.GUI_COLOR_PRIMARY)
        self.btn_close = Button_(self.button_frame, width=18, text=_("Close"), relief="groove", bg=VAR.GUI_COLOR_PRIMARY, command=self.close)

        self.label_license.set( 'MIT License\n\n'
                                'Copyright (c) 2021 x211321, pfochel\n\n'
                                'Permission is hereby granted, free of charge, to any person obtaining a copy\n'
                                'of this software and associated documentation files (the "Software"), to deal\n'
                                'in the Software without restriction, including without limitation the rights\n'
                                'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n'
                                'copies of the Software, and to permit persons to whom the Software is\n'
                                'furnished to do so, subject to the following conditions:\n\n'
                                'The above copyright notice and this permission notice shall be included in all\n'
                                'copies or substantial portions of the Software.\n\n'
                                'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n'
                                'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n'
                                'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n'
                                'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n'
                                'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n'
                                'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n'
                                'SOFTWARE.')

        self.label_link.set(_("VGC Analyze GitHub"))
        self.label_link.config(fg="blue", cursor="hand2")
        self.label_link.bind("<Button-1>", openGithub)

        self.label_title.grid(row=0, column=0, padx=10, pady=10)
        self.label_description.grid(row=1, column=0, padx=10, pady=10)
        self.label_disclamer.grid(row=2, column=0, padx=10, pady=10)
        self.label_link.grid(row=3, column=0, padx=10, pady=10)
        self.label_license.grid(row=4, column=0, padx=10, pady=10)
        self.btn_close.grid(row=0, column=0, pady=20)


        self.center()

        self.window.deiconify()

        # Run main loop of new window
        self.window.mainloop()

    def center(self):
        centerPopup(self.window, self.parent)

    def close(self):
        if not self.window == None:
            self.window.destroy()


######################
# Pop_DatePicker
# --------------------
class Pop_DatePicker(object):

    window = None

    def __init__(self, parent, callback = None):

        self.daylabels = {}

        self.calendar = calendar.Calendar()

        self.dateSelected  = date.today()
        self.indexSelected = 0

        self.setDate(self.dateSelected)

        self.parent   = parent
        self.callback = callback
        self.iconPrev = loadIcon("chevron-back-outline", 20, 20)
        self.iconNext = loadIcon("chevron-forward-outline", 20, 20)

    def show(self, widget=None, restore_date=None):
        # Attach coresponding entry widget
        self.widget = widget

        # Position next to corresponding entry widget
        xPos = 0
        yPos = 0

        if not self.widget == None:
            xPos = self.widget.winfo_rootx() + self.widget.winfo_width()
            yPos = self.widget.winfo_rooty()

        # Close previous window
        self.close()

        # Restore date
        if not restore_date == None and not len(restore_date) == 0:
            self.dateSelected = date.fromisoformat(restore_date)
            self.setDate(self.dateSelected)

        # Create new window
        self.window = Toplevel(bg=VAR.GUI_COLOR_PRIMARY)
        self.window.withdraw()
        self.window.wm_title(_("Select date"))
        self.window.resizable(False, False)

        if not platform.system() == "Darwin":
            self.window.iconphoto(False, loadIcon("calendar-outline", 512, 512))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        self.window.rowconfigure(1, weight=1)

        # Main Frames
        self.frame_calendar = Frame(self.window, bg=VAR.GUI_COLOR_PRIMARY)
        self.frame_spacer   = Frame(self.window, bg=VAR.GUI_COLOR_PRIMARY)
        self.frame_buttons  = Frame(self.window, bg=VAR.GUI_COLOR_SECONDARY)

        self.frame_calendar.grid(row=0, column=0, padx=10, pady=10, sticky="nwse")
        self.frame_spacer.grid(row=1, column=0, sticky="nwse")
        self.frame_buttons.grid(row=2, column=0, sticky="nwse")

        self.frame_calendar.columnconfigure(0, weight=1)

        # Year Frame
        self.frame_year     = Frame(self.frame_calendar, bg=VAR.GUI_COLOR_PRIMARY)
        self.frame_year.grid(row=0, column=0, sticky="nwse", pady=(0, 5))
        self.frame_year.columnconfigure(1, weight=1)

        self.button_prev_year = Button_(self.frame_year, width=30, image=self.iconPrev, relief="groove", bg=VAR.GUI_COLOR_PRIMARY, command=lambda:self.changeYear(-1))
        self.label_year       = Label_(self.frame_year, bg=VAR.GUI_COLOR_PRIMARY, text=str(self.year), font=(20))
        self.button_next_year = Button_(self.frame_year, width=30, image=self.iconNext, relief="groove", bg=VAR.GUI_COLOR_PRIMARY, command=lambda:self.changeYear(+1))

        self.button_prev_year.grid(row=0, column=0)
        self.label_year.grid(row=0, column=1)
        self.button_next_year.grid(row=0, column=2)

        # Month Frame
        self.frame_month     = Frame(self.frame_calendar, bg=VAR.GUI_COLOR_PRIMARY)
        self.frame_month.grid(row=1, column=0, sticky="nwse", pady=(0, 5))
        self.frame_month.columnconfigure(1, weight=1)

        self.button_prev_month = Button_(self.frame_month, width=30, image=self.iconPrev, relief="groove", bg=VAR.GUI_COLOR_PRIMARY, command=lambda:self.changeMonth(-1))
        self.label_month       = Label_(self.frame_month, bg=VAR.GUI_COLOR_PRIMARY, text=self.month_name, font=(15))
        self.button_next_month = Button_(self.frame_month, width=30, image=self.iconNext, relief="groove", bg=VAR.GUI_COLOR_PRIMARY, command=lambda:self.changeMonth(+1))

        self.button_prev_month.grid(row=0, column=0)
        self.label_month.grid(row=0, column=1)
        self.button_next_month.grid(row=0, column=2)

        # Days Frame
        self.frame_days      = Frame(self.frame_calendar, bg=VAR.GUI_COLOR_PRIMARY)
        self.frame_days.grid(row=2, column=0, sticky="nwse")

        # Buttons
        self.btn_cancel= Button_(self.frame_buttons, width=15, text=_("Cancel"), relief="groove", command=self.close, bg=VAR.BUTTON_COLOR_BAD)
        self.btn_ok    = Button_(self.frame_buttons, width=15, text=_("OK"), relief="groove", command=self.confirm, bg=VAR.BUTTON_COLOR_GOOD)

        self.btn_cancel.grid(row=0, column=0, padx=10, pady=20, sticky="w")
        self.btn_ok.grid(row=0, column=1, padx=10, pady=20, sticky="e")

        self.frame_buttons.columnconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(1, weight=1)

        # Show initial days
        self.showDays()

        # Set window position
        self.window.geometry("+{0}+{1}".format(xPos, yPos))

        # Show window
        self.window.deiconify()

        # Run main loop of new window
        self.window.mainloop()


    def close(self):
        if not self.window == None:
            self.window.destroy()


    def confirm(self):
        if not self.widget == None:
            self.widget.set(self.dateSelected)

        if not self.callback == None:
            self.callback()

        self.close()


    def setDate(self, date, refresh=False):
        self.dateSelected = date

        self.year  = int(date.year)
        self.month = int(date.month)
        self.day   = int(date.day)

        self.month_name = calendar.month_name[self.month]

        if refresh:
            self.showYear()
            self.showMonth()


    def changeYear(self, ammount):
        self.year = self.year + ammount
        self.showYear()


    def showYear(self):
        self.label_year.set(str(self.year))
        self.showDays()


    def changeMonth(self, ammount):
        newMonth = self.month + ammount

        if newMonth < 1:
            newMonth = 12 + newMonth
            self.changeYear(-1)
        if newMonth > 12:
            newMonth = newMonth - 12
            self.changeYear(+1)

        self.month = newMonth
        self.showMonth()


    def showMonth(self):
        self.month_name = calendar.month_name[self.month]
        self.label_month.set(self.month_name)
        self.showDays()


    def showDays(self):
        col = 0
        row = 0

        # reset
        for index in self.daylabels:
            self.daylabels[index].destroy()

        self.daylabels = {}

        # generate day labels for current month
        for i, day in enumerate(self.calendar.itermonthdates(self.year, self.month)):

            index = i+1

            bg           = self.getDayBG(day)
            highlight_bg = self.getDayHighlightBG(day)

            self.daylabels[index] = Label_(self.frame_days, text=day.day, width=5, height=2, anchor="center", bg=bg, highlight_bg=highlight_bg)
            self.daylabels[index].grid(row=row, column=col, padx=1, pady=1)
            self.daylabels[index].bind("<Enter>", lambda a, index=index:self.dayLabelEnter(a, index))
            self.daylabels[index].bind("<Leave>", lambda a, index=index:self.dayLabelLeave(a, index))
            self.daylabels[index].bind("<Button-1>", lambda a, index=index, day=day:self.dayLabelSelect(a, index, day))
            self.daylabels[index].bind("<Double-1>", lambda a, index=index, day=day:self.dayLabelSelect(a, index, day, True))

            col += 1

            # Select current date
            if day == self.dateSelected:
                self.dayLabelSelect(None, index, day)

            # Change row after every week
            if index % 7 == 0:
                row += 1
                col  = 0

        # Add empty row for month with only 5 weeks
        if row == 5:
            self.daySpacer = Label_(self.frame_days, height=2, bg=VAR.GUI_COLOR_PRIMARY)
            self.daySpacer.grid(row=row, column=0, padx=1, pady=1)


    def getDayBG(self, day):
        if day.month == self.month:
            return VAR.CAL_COLOR_PRIMARY
        else:
            return VAR.CAL_COLOR_SECONDARY


    def getDayHighlightBG(self, day):
        if day.month == self.month:
            return VAR.CAL_COLOR_HIGH_PRIMARY
        else:
            return VAR.CAL_COLOR_HIGH_SECONDARY


    def dayLabelEnter(self, a, index):
        self.daylabels[index].highlight()


    def dayLabelLeave(self, a, index):
        self.daylabels[index].restore_bg()


    def dayLabelSelect(self, a, index, day, confirm=False):
        self.dateSelected  = day

        if day.year < self.year or (day.year == self.year and day.month < self.month):
            self.changeMonth(-1)
            return
        if day.year > self.year or (day.year == self.year and day.month > self.month):
            self.changeMonth(+1)
            return


        if self.indexSelected in self.daylabels:
            self.daylabels[self.indexSelected].set_bg(VAR.CAL_COLOR_PRIMARY)

        self.indexSelected = index
        self.daylabels[index].set_bg(VAR.CAL_COLOR_SELECTED)

        if confirm:
            self.confirm()

