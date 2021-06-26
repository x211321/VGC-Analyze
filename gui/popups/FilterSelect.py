import platform
from lib.Img import loadIcon
from lib.Widgets  import *

######################
# FilterSelect
# --------------------
class FilterSelect(object):

    window = None

    def __init__(self, parent, callback = None):

        self.parent   = parent
        self.callback = callback

    def show(self, options, activeOptions, filterType, maxCol = 0, focusWidget=None, align=""):

        # Close previous window
        self.close()

        # Attach to focus widget
        self.focusWidget = focusWidget

        # Create new window
        self.window = Toplevel(bg=VAR.GUI_COLOR_PRIMARY)
        self.window.wm_overrideredirect(True)
        self.window.withdraw()
        self.window.wm_title(_("Select ") + filterType)
        self.window.resizable(False, False)

        if not platform.system() == "Darwin":
            self.window.iconphoto(False, loadIcon("filter-outline", 512, 512))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        # Main Frames
        self.frame_main    = Frame_(self.window, borderwidth=2, relief="groove")

        self.frame_options = Frame_(self.frame_main)
        self.frame_buttons = Frame_(self.frame_main, style=VAR.FRAME_STYLE_SECONDARY)

        self.frame_main.grid(row=0, column=0, sticky="nwse")

        self.frame_options.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        self.frame_buttons.grid(row=1, column=0, sticky="nesw")

        self.btn_cancel= LabelButton_(self.frame_buttons, width=20, text=_("Cancel"), command=self.close, style=VAR.LABELBUTTON_STYLE_CANCEL)
        self.btn_reset = LabelButton_(self.frame_buttons, width=20, text=_("Reset"), command=self.reset)
        self.btn_all   = LabelButton_(self.frame_buttons, width=20, text=_("Select all"), command=self.selectAll)
        self.btn_ok    = LabelButton_(self.frame_buttons, width=20, text=_("OK"), command=self.confirm, style=VAR.LABELBUTTON_STYLE_CONFIRM)

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
            self.widgets[option] = LabelButton_(self.frame_options, text=option, width=maxLen, _toggle=True)
            self.widgets[option].grid(row=row, column=col, sticky="w", padx=5, pady=5)

            if option in activeOptions:
                self.widgets[option].setToggle(True)

            col += 1

            if col > maxCol:
                col  = 0
                row += 1

        # Position next to focus widget
        xPos = 0
        yPos = 0

        self.window.update()

        if not self.focusWidget == None:
            if align == "left":
                xPos = self.focusWidget.winfo_rootx() - self.window.winfo_reqwidth()
                yPos = self.focusWidget.winfo_rooty()
            else:
                xPos = self.focusWidget.winfo_rootx() + self.focusWidget.winfo_width()
                yPos = self.focusWidget.winfo_rooty()

        # Set window position
        self.window.geometry("+{0}+{1}".format(xPos, yPos))

        # Show window
        self.window.deiconify()

        # Run main loop of new window
        self.window.mainloop()

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
            if self.widgets[widget]._toggleState == True:
                selectedOptions.append(widget)

        if not self.callback == None:
            self.callback(selectedOptions)

        self.close()