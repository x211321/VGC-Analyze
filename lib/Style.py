import lib.Var as VAR
from tkinter import ttk

def initStyles():
    ttk.Style().configure("TFrame", background=VAR.GUI_COLOR_PRIMARY)
    ttk.Style().configure(VAR.FRAME_STYLE_PRIMARY, background=VAR.GUI_COLOR_PRIMARY)
    ttk.Style().configure(VAR.FRAME_STYLE_SECONDARY, background=VAR.GUI_COLOR_SECONDARY)

    ttk.Style().configure("TLabel", background=VAR.GUI_COLOR_PRIMARY)
    ttk.Style().configure(VAR.LABEL_STYLE_PRIMARY, background=VAR.GUI_COLOR_PRIMARY)
    ttk.Style().configure(VAR.LABEL_STYLE_SECONDARY, background=VAR.GUI_COLOR_SECONDARY)
    ttk.Style().configure(VAR.LABEL_STYLE_WARNING, background=VAR.GUI_COLOR_WARNING)
    ttk.Style().configure(VAR.LABEL_STYLE_WARN_TEXT_PRIMARY, foreground=VAR.LABEL_COLOR_WARN_TEXT, background=VAR.GUI_COLOR_PRIMARY)
    ttk.Style().configure(VAR.LABEL_STYLE_WARN_TEXT_SECONDARY, foreground=VAR.LABEL_COLOR_WARN_TEXT, background=VAR.GUI_COLOR_SECONDARY)
    ttk.Style().configure(VAR.LABEL_STYLE_LINK_PRIMARY, foreground="blue", background=VAR.GUI_COLOR_PRIMARY)
    ttk.Style().configure(VAR.LABEL_STYLE_LINK_SECONDARY, foreground="blue", background=VAR.GUI_COLOR_SECONDARY)
    ttk.Style().configure(VAR.LABEL_STYLE_CAL_PRIMARY, background=VAR.CAL_COLOR_PRIMARY)
    ttk.Style().configure(VAR.LABEL_STYLE_CAL_SECONDARY, background=VAR.CAL_COLOR_SECONDARY)
    ttk.Style().configure(VAR.LABEL_STYLE_CAL_HIGH_PRIMARY, background=VAR.CAL_COLOR_HIGH_PRIMARY)
    ttk.Style().configure(VAR.LABEL_STYLE_CAL_HIGH_SECONDARY, background=VAR.CAL_COLOR_HIGH_SECONDARY)
    ttk.Style().configure(VAR.LABEL_STYLE_CAL_SELECTED, background=VAR.CAL_COLOR_SELECTED)

    ttk.Style().configure("TCheckbutton", background=VAR.GUI_COLOR_PRIMARY)
    ttk.Style().configure(VAR.CHECKBOX_STYLE_PRIMARY, background=VAR.GUI_COLOR_PRIMARY)
    ttk.Style().configure(VAR.CHECKBOX_STYLE_SECUNDARY, background=VAR.GUI_COLOR_SECONDARY)

    ttk.Style().configure(VAR.LABELBUTTON_STYLE        , padding=5, relief="groove", anchor="center")
    ttk.Style().configure(VAR.LABELBUTTON_STYLE_DEFAULT, background=VAR.BUTTON_COLOR_DEFAULT)
    ttk.Style().configure(VAR.LABELBUTTON_STYLE_HOVER  , background=VAR.BUTTON_COLOR_HOVER)
    ttk.Style().configure(VAR.LABELBUTTON_STYLE_PRESSED, background=VAR.BUTTON_COLOR_PRESSED)
    ttk.Style().configure(VAR.LABELBUTTON_STYLE_TOGGLED, background=VAR.BUTTON_COLOR_TOGGLED)
    ttk.Style().configure(VAR.LABELBUTTON_STYLE_CONFIRM, background=VAR.BUTTON_COLOR_CONFIRM)
    ttk.Style().configure(VAR.LABELBUTTON_STYLE_CANCEL , background=VAR.BUTTON_COLOR_CANCEL)




