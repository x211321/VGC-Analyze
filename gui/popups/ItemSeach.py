from lib.Img import loadIcon
from lib.Widgets import *

######################
# ItemSeach
# --------------------
class ItemSeach(object):

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
        # self.window.wm_overrideredirect(True)
        self.window.withdraw()
        self.window.wm_title(_("Search for item"))
        self.window.resizable(False, False)

        if not platform.system() == "Darwin":
            self.window.iconphoto(False, loadIcon("search-outline", 512, 512))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        # Functions
        # ------------------
        self.main_frame   = Frame_(self.window, borderwidth=2, relief="groove")
        self.input_frame  = Frame_(self.main_frame)
        self.button_frame = Frame_(self.main_frame, style=VAR.FRAME_STYLE_SECONDARY)

        self.main_frame.grid(row=0, column=0, sticky="nwse")
        self.input_frame.grid(row=0, column=0, sticky="nwse")
        self.button_frame.grid(row=1, column=0, sticky="nwse")

        self.button_frame.columnconfigure(1, weight=1)

        self.label_search = Label_(self.input_frame, anchor="w", text=_("Search for"))
        self.input_search = Entry_(self.input_frame, width=35)
        self.label_info   = Label_(self.input_frame, width=35, anchor="w", style=VAR.LABEL_STYLE_WARN_TEXT_PRIMARY)

        self.btn_cancel   = LabelButton_(self.button_frame, width=15, text=_("Cancel"), style=VAR.LABELBUTTON_STYLE_CANCEL, command=self.close)
        self.btn_spacer   = Label_(self.button_frame, style=VAR.LABEL_STYLE_SECONDARY)
        self.btn_search   = LabelButton_(self.button_frame, width=15, text=_("Search"), style=VAR.LABELBUTTON_STYLE_CONFIRM, command=self.search)

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
    # Update window
        self.window.update()

        # Get window size
        w = self.window.winfo_reqwidth()
        h = self.window.winfo_reqheight()

        # Calculate position relative to main parent
        x = int(self.parent.winfo_x() + (self.parent.winfo_width() / 2) - (w / 2))
        y = int(self.parent.winfo_y() + (self.parent.winfo_height() / 2) - (h / 2))

        # Position window
        self.window.geometry("{0}x{1}+{2}+{3}".format(w, h, x, y))

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