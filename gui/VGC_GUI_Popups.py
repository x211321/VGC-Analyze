from VGC_Locale import _

import os

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import VGC_Var as VAR

from VGC_Img import loadIcon

from VGC_Widgets  import Label_
from VGC_Widgets  import Entry_
from VGC_Widgets  import Checkbutton_
from VGC_Data     import FilterData
from VGC_Browser  import openUserProfileInBrowser
from VGC_Download import downloadCollection


######################
# initPopups
# --------------------
def initPopups(gui):
    gui.pop_collectionDownload = Pop_CollectionDownload(gui, gui.collectionDownload_callback)
    gui.pop_itemSearch         = Pop_ItemSearch(gui, gui.view_frame.item_view)


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
                self.window.iconphoto(False, loadIcon("eye-outline", 15, 15))
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
        self.window.iconphoto(False, loadIcon("cloud-download-outline", 15, 15))
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

        self.label_user   = Label_(self.input_frame, anchor="w", text=_("VGC Username"), bg=VAR.GUI_COLOR_PRIMARY)
        self.input_user   = Entry_(self.input_frame, width=31, relief="solid")
        self.label_pass   = Label_(self.input_frame, anchor="w", text=_("Password"), bg=VAR.GUI_COLOR_PRIMARY)
        self.input_pass   = Entry_(self.input_frame, width=31, relief="solid", show="*")
        self.btn_cancel   = Button(self.button_frame, width=18, text=_("Cancel"), relief="groove", bg=VAR.BUTTON_COLOR_BAD, command=self.close)
        self.btn_spacer   = Label_(self.button_frame, bg=VAR.GUI_COLOR_SECONDARY)
        self.btn_download = Button(self.button_frame, width=18, text=_("Download"), relief="groove", bg=VAR.BUTTON_COLOR_GOOD, command=self.download)
        self.label_info   = Label_(self.button_frame, width=35)
        self.label_link   = Label_(self.button_frame, width=35, anchor="center")

        self.label_user.grid(row=0, column=0, pady=(15,10), padx=10, sticky="w")
        self.input_user.grid(row=0, column=1, pady=(15,10), padx=10, sticky="w")

        self.label_pass.grid(row=1, column=0, pady=(0,10), padx=10, sticky="w")
        self.input_pass.grid(row=1, column=1, pady=(0,15), padx=10, sticky="w")

        self.btn_cancel.grid(row=0, column=0, pady=20, padx=10, sticky="e")
        self.btn_spacer.grid(row=0, column=1)
        self.btn_download.grid(row=0, column=2, pady=20, padx=10, sticky="w")

        self.label_info.grid(row=1, column=0, pady=0, padx=10, sticky="nwse", columnspan=3)
        self.label_link.grid(row=2, column=0, pady=(5, 10), padx=10, sticky="nwse", columnspan=3)

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
        self.window.iconphoto(False, loadIcon("search-outline", 15, 15))
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

        self.btn_cancel   = Button(self.button_frame, width=15, text=_("Cancel"), relief="groove", bg=VAR.BUTTON_COLOR_BAD, command=self.close)
        self.btn_spacer   = Label_(self.button_frame, bg=VAR.GUI_COLOR_SECONDARY)
        self.btn_search   = Button(self.button_frame, width=15, text=_("Search"), relief="groove", bg=VAR.BUTTON_COLOR_GOOD, command=self.search)

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

                if searchString.lower() in self.treeView.item(rowIDs[index])["values"][1].lower():
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

    def show(self, options, activeOptions, filterType):
        # Close previous window
        self.close()

        # Create new window
        self.window = Toplevel(bg=VAR.GUI_COLOR_PRIMARY)
        self.window.wm_title(_("Select ") + filterType)
        self.window.resizable(False, False)
        self.window.iconphoto(False, loadIcon("filter-outline", 15, 15))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        self.frame_options = Frame(self.window, bg=VAR.GUI_COLOR_PRIMARY)
        self.frame_buttons = Frame(self.window, bg=VAR.GUI_COLOR_SECONDARY)

        self.frame_options.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        self.frame_buttons.grid(row=1, column=0, sticky="nesw")

        self.btn_cancel= Button(self.frame_buttons, width=20, text=_("Cancel"), relief="groove", command=self.close, bg=VAR.BUTTON_COLOR_BAD)
        self.btn_reset = Button(self.frame_buttons, width=20, text=_("Reset"), relief="groove", command=self.reset, bg=VAR.INPUT_COLOR)
        self.btn_all   = Button(self.frame_buttons, width=20, text=_("Select all"), relief="groove", command=self.selectAll, bg=VAR.INPUT_COLOR)
        self.btn_ok    = Button(self.frame_buttons, width=20, text=_("OK"), relief="groove", command=self.confirm, bg=VAR.BUTTON_COLOR_GOOD)

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

        for option, data in sorted(options):
            if len(option) > maxLen:
                maxLen = len(option)

        maxCol = int(150 / maxLen)

        print(maxCol)

        # Create checkbuttons
        for option, data in sorted(options):
            self.widgets[option] = Checkbutton_(self.frame_options, label=option, bg=VAR.GUI_COLOR_PRIMARY, width=maxLen, anchor="w")
            self.widgets[option].grid(row=row, column=col, sticky="w", padx=5, pady=5)

            if option in activeOptions:
                self.widgets[option].set(True)

            col += 1

            if col > maxCol:
                col  = 0
                row += 1

        # Run main loop of new window
        self.window.mainloop()

    def close(self):
        if not self.window == None:
            self.window.destroy()

    def reset(self):
        for widget in self.widgets:
            self.widgets[widget].set(False)

    def selectAll(self):
        for widget in self.widgets:
            self.widgets[widget].set(True)

    def confirm(self):
        selectedOptions = []

        for widget in self.widgets:
            if self.widgets[widget].get() == True:
                selectedOptions.append(widget)

        if not self.callback == None:
            self.callback(selectedOptions)

        self.close()
