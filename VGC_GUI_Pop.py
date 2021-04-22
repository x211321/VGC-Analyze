
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from VGC_Var import IMG_CASHE_FRONT
from VGC_Var import IMG_CASHE_BACK
from VGC_Var import IMG_CASHE_CART
from VGC_Var import IMG_COVER_NONE

from VGC_Img import loadIcon

from VGC_Widgets import Label_
from VGC_Widgets import Entry_

from VGC_Data import FilterData

from VGC_Browser import openUserProfileInBrowser

from VGC_Download import downloadCollection


######################
# Pop_CoverViewer
# --------------------
class Pop_CoverViewer(object):

    window = None
    parent = None

    def __init__(self, parent):
        self.parent = parent

    def show(self, coverType, item = None):
        coverSize = 500

        self.close()

        if not item == None:
            # Get cover path
            if coverType == "front":
                img = IMG_CASHE_FRONT + str(item.id) + ".jpg"
            if coverType == "back":
                img = IMG_CASHE_BACK + str(item.id) + ".jpg"
            if coverType == "cart":
                img = IMG_CASHE_CART + str(item.id) + ".jpg"

            # Calculate position relative to main parent
            x = self.parent.winfo_x() + self.parent.winfo_width() - 210 - coverSize
            y = self.parent.winfo_y() + 50

            # Create new window
            self.window = Toplevel()
            self.window.wm_title(item.name + " - " + coverType + " cover")
            self.window.geometry("+"+str(x)+"+"+str(y))
            self.window.resizable(False, False)
            self.window.iconphoto(False, loadIcon("eye-outline", 15, 15))
            self.window.bind('<Escape>', lambda x:self.close())
            self.window.focus_force()

            # Create and place cover label
            coverViewer_cover = Label_(self.window, img=img, imgwidth=coverSize)
            coverViewer_cover.item.pack(expand="Yes")

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

        w = 315
        h = 400

        self.close()

        # Calculate position relative to main parent
        x = int(self.parent.winfo_x() + (self.parent.winfo_width() / 2) - (w / 2))
        y = int(self.parent.winfo_y() + (self.parent.winfo_height() / 2) - (h / 2))

        # Create new window
        self.window = Toplevel()
        self.window.wm_title("Download collection")
        self.window.geometry(str(w)+"x"+str(h)+"+"+str(x)+"+"+str(y))
        self.window.resizable(False, False)
        self.window.iconphoto(False, loadIcon("cloud-download-outline", 15, 15))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        # Functions
        # ------------------
        label_user      = Label_(self.window, anchor="w", text="Username")
        self.input_user = Entry_(self.window, width=35)
        label_pass      = Label_(self.window, anchor="w", text="Password")
        self.input_pass = Entry_(self.window, width=35, show="*")
        btn_download    = Button(self.window, text="Download", relief="groove")
        label_info      = Label_(self.window, width=35)
        label_link      = Label_(self.window, width=35, anchor="center")

        label_user.item.grid(row=0, column=0, pady=(15,10), padx=10, sticky="w")
        self.input_user.item.grid(row=0, column=1, pady=(15,10), padx=10, sticky="w")

        label_pass.item.grid(row=1, column=0, pady=(0,10), padx=10, sticky="w")
        self.input_pass.item.grid(row=1, column=1, pady=(0,10), padx=10, sticky="w")

        btn_download.grid(row=2, column=0, pady=(0,10), padx=10, sticky="nwse", columnspan=2)

        label_info.item.grid(row=3, column=0, pady=10, padx=10, sticky="nwse", columnspan=2)
        label_link.item.grid(row=4, column=0, pady=(0, 10), padx=10, sticky="nwse", columnspan=2)

        label_info.set("The provided login credentials will be used to\n"
                       "download a backup of your collection from\n" +
                       "your VGCollect.com user profile.\n\n" +
                       "Your login information will not be saved or used\n" +
                       "for any other purpose.\n\n" +
                       "You can also provide your collection data manually:\n\n" +
                       " 1) \tExport your collection from your\n" +
                       "\tVGCollect.com user profile\n\n" +
                       " 2) \tPlace the resulting file into the \n" +
                       "\tVGC Analyze program folder\n\n" +
                       " 3) \tRestart VGC Analyzer")

        label_link.set("VGCollect.com user profile")
        label_link.item.config(fg="blue", cursor="hand2")
        label_link.item.bind("<Button-1>", openUserProfileInBrowser)

        self.input_pass.item.bind('<Return>', self.download)

        btn_download.config(command=self.download)

        self.input_user.item.focus()

        # Run main loop of new window
        self.window.mainloop()

    def close(self):
        if not self.window == None:
            self.window.destroy()

    def setCallback(self, callback):
        self.callback = callback

    def download(self, a = None):
        temp     = FilterData()
        user     = self.input_user.get()
        password = self.input_pass.get()

        temp.guiMode = True

        if len(user) == 0 or len(password) == 0:
            messagebox.showerror("Collection download", "Login credentials incomplete", parent=self.window)
            return

        result = downloadCollection(temp, user, password)

        if result == None:
            self.window.destroy()
            messagebox.showinfo("Collection download", "Download successful", parent=self.parent)

            if not self.callback == None:
                self.callback(result, temp.filePath)
        else:
            messagebox.showerror("Collection download", result, parent=self.window)


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

        w = 310
        h = 110

        # Get selected row
        selection = self.treeView.focus()

        if len(selection):
            self.startIndex = self.treeView.index(selection)
        else:
            self.startIndex = -1

        # Close previous window
        self.close()

        # Calculate position relative to main parent
        x = int(self.parent.winfo_x() + (self.parent.winfo_width() / 2) - (w / 2))
        y = int(self.parent.winfo_y() + (self.parent.winfo_height() / 2) - (h / 2))

        # Create new window
        self.window = Toplevel()
        self.window.wm_title("Search for item")
        self.window.geometry(str(w)+"x"+str(h)+"+"+str(x)+"+"+str(y))
        self.window.resizable(False, False)
        self.window.iconphoto(False, loadIcon("search-outline", 15, 15))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        # Functions
        # ------------------
        label_search      = Label_(self.window, anchor="w", text="Search for")
        self.input_search = Entry_(self.window, width=35)
        self.label_info   = Label_(self.window, anchor="w", fg="#F00")
        btn_search        = Button(self.window, text="Search", relief="groove")

        label_search.item.grid(row=0, column=0, pady=(15,10), padx=10, sticky="w")
        self.input_search.item.grid(row=0, column=1, pady=(15,10), padx=10, sticky="w")
        self.label_info.item.grid(row=1, column=0, padx=10, sticky="nwse", columnspan=2)

        btn_search.grid(row=2, column=0, pady=(10,10), padx=10, sticky="nwse", columnspan=2)

        self.input_search.item.bind('<Return>', self.search)

        btn_search.config(command=self.search)

        self.input_search.item.focus()

        # Run main loop of new window
        self.window.mainloop()

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
                self.treeView.selection_set(str(rowIDs[index]))
                self.treeView.see(str(rowIDs[index]))
            else:
                # Show error
                self.label_info.set("Couldn't find \"" + searchString + "\"")

            if not self.callback == None:
                self.callback(found, index)
