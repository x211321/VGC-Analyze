import platform
from datetime import date
import calendar

from lib.Lib import guessDate
from lib.Img import loadIcon
from lib.Widgets  import *

######################
# DatePicker
# --------------------
class DatePicker(object):

    window = None

    def __init__(self, parent, callback = None):

        self.daylabels = {}

        self.rowHeight = 35
        self.colWidth  = 40

        self.calendar = calendar.Calendar()

        self.dateSelected  = date.today()
        self.indexSelected = 0

        self.setDate(self.dateSelected)

        self.parent   = parent
        self.callback = callback
        self.iconPrev = loadIcon("chevron-back-outline", 20, 20)
        self.iconNext = loadIcon("chevron-forward-outline", 20, 20)

    def show(self, widget=None, focusWidget=None, restore_date=None, mode="start"):
        # Attach coresponding entry widget
        self.widget      = widget
        self.focusWidget = focusWidget

        # Position next to focus widget
        xPos = 0
        yPos = 0

        if not self.focusWidget == None:
            xPos = self.focusWidget.winfo_rootx() + self.focusWidget.winfo_width()
            yPos = self.focusWidget.winfo_rooty()

        # Close previous window
        self.close()

        # Restore date
        restore_date = guessDate(restore_date, mode)

        if not restore_date == None and len(restore_date) == 10:
            try:
                self.dateSelected = date.fromisoformat(restore_date)
            except ValueError:
                self.dateSelected = date.today()
            self.setDate(self.dateSelected)

        # Create new window
        self.window = Toplevel(bg=VAR.GUI_COLOR_PRIMARY)
        if not platform.system() == "Darwin":
            self.window.wm_overrideredirect(True)
        self.window.withdraw()
        self.window.wm_title(_("Select date"))
        self.window.resizable(False, False)

        if not platform.system() == "Darwin":
            self.window.iconphoto(False, loadIcon("calendar-outline", 512, 512))
        self.window.bind('<Escape>', lambda x:self.close())
        self.window.focus_force()

        self.window.rowconfigure(1, weight=1)

        # Main Frames
        self.frame_main     = Frame_(self.window, borderwidth=2, relief="groove")

        self.frame_calendar = Frame_(self.frame_main)
        self.frame_spacer   = Frame_(self.frame_main)
        self.frame_buttons  = Frame_(self.frame_main, style=VAR.FRAME_STYLE_SECONDARY)

        self.frame_main.grid(row=0, column=0, sticky="nwse")
        self.frame_calendar.grid(row=0, column=0, padx=10, pady=10, sticky="nwse")
        self.frame_spacer.grid(row=1, column=0, sticky="nwse")
        self.frame_buttons.grid(row=2, column=0, sticky="nwse")

        self.frame_calendar.columnconfigure(0, weight=1)

        # Year Frame
        self.frame_year     = Frame_(self.frame_calendar)
        self.frame_year.grid(row=0, column=0, sticky="nwse", pady=(0, 5))
        self.frame_year.columnconfigure(1, weight=1)

        self.button_prev_year = LabelButton_(self.frame_year, width=30, image=self.iconPrev, command=lambda:self.changeYear(-1))
        self.label_year       = Label_(self.frame_year, text=str(self.year), font=(20))
        self.button_next_year = LabelButton_(self.frame_year, width=30, image=self.iconNext, command=lambda:self.changeYear(+1))

        self.button_prev_year.grid(row=0, column=0)
        self.label_year.grid(row=0, column=1)
        self.button_next_year.grid(row=0, column=2)

        # Month Frame
        self.frame_month     = Frame_(self.frame_calendar)
        self.frame_month.grid(row=1, column=0, sticky="nwse", pady=(0, 5))
        self.frame_month.columnconfigure(1, weight=1)

        self.button_prev_month = LabelButton_(self.frame_month, width=30, image=self.iconPrev, command=lambda:self.changeMonth(-1))
        self.label_month       = Label_(self.frame_month, text=self.month_name, font=(15))
        self.button_next_month = LabelButton_(self.frame_month, width=30, image=self.iconNext, command=lambda:self.changeMonth(+1))

        self.button_prev_month.grid(row=0, column=0)
        self.label_month.grid(row=0, column=1)
        self.button_next_month.grid(row=0, column=2)

        # Days Frame
        self.frame_days      = Frame_(self.frame_calendar)
        self.frame_days.grid(row=2, column=0, sticky="nwse")

        # Buttons
        self.btn_cancel= LabelButton_(self.frame_buttons, width=15, text=_("Cancel"), command=self.close, style=VAR.LABELBUTTON_STYLE_CANCEL)
        self.btn_ok    = LabelButton_(self.frame_buttons, width=15, text=_("OK"), command=self.confirm, style=VAR.LABELBUTTON_STYLE_CONFIRM)

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

            self.frame_days.rowconfigure(row, minsize=self.rowHeight)
            self.frame_days.columnconfigure(col, minsize=self.colWidth)

            style           = self.getDayStyle(day)
            highlight_style = self.getDayHighlightStyle(day)

            self.daylabels[index] = Label_(self.frame_days, text=day.day, anchor="center", style=style, _highlight_style=highlight_style)
            self.daylabels[index].grid(row=row, column=col, padx=1, pady=1, sticky="nwse")
            self.daylabels[index].bind("<Enter>", lambda a, index=index:self.dayLabelEnter(a, index))
            self.daylabels[index].bind("<Leave>", lambda a, index=index:self.dayLabelLeave(a, index))
            self.daylabels[index].bind("<Button-1>", lambda a, index=index, day=day:self.dayLabelSelect(a, index, day))
            self.daylabels[index].bind("<Double-1>", lambda a, index=index, day=day:self.dayLabelSelect(a, index, day, True))

            col += 1

            # Select current date
            if day == self.dateSelected and day.month == self.month:
                self.dayLabelSelect(None, index, day)

            # Change row after every week
            if index % 7 == 0:
                row += 1
                col  = 0

        # Add empty row for month with only 5 weeks
        if row == 5:
            self.frame_days.rowconfigure(row, minsize=self.rowHeight)
            self.daySpacer = Label_(self.frame_days)
            self.daySpacer.grid(row=row, column=0, padx=1, pady=1)


    def getDayStyle(self, day):
        if day.month == self.month:
            return VAR.LABEL_STYLE_CAL_PRIMARY
        else:
            return VAR.LABEL_STYLE_CAL_SECONDARY


    def getDayHighlightStyle(self, day):
        if day.month == self.month:
            return VAR.LABEL_STYLE_CAL_HIGH_PRIMARY
        else:
            return VAR.LABEL_STYLE_CAL_HIGH_SECONDARY


    def dayLabelEnter(self, a, index):
        self.daylabels[index].highlight()


    def dayLabelLeave(self, a, index):
        self.daylabels[index].restore_style()


    def dayLabelSelect(self, a, index, day, confirm=False):
        self.dateSelected  = day

        if day.year < self.year or (day.year == self.year and day.month < self.month):
            self.changeMonth(-1)
            return
        if day.year > self.year or (day.year == self.year and day.month > self.month):
            self.changeMonth(+1)
            return


        if self.indexSelected in self.daylabels:
            self.daylabels[self.indexSelected].set_style(VAR.LABEL_STYLE_CAL_PRIMARY)

        self.indexSelected = index
        self.daylabels[index].set_style(VAR.LABEL_STYLE_CAL_SELECTED)

        if confirm:
            self.confirm()
