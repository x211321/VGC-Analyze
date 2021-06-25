import lib.Var as VAR
from tkinter import ttk

def initStyles():
    STYLE_FRAME_DEFAULT = ttk.Style()
    STYLE_FRAME_DEFAULT.configure("TFrame", background=VAR.GUI_COLOR_PRIMARY)

    # STYLE_FRAME_PRIMARY = ttk.Style()
    # STYLE_FRAME_PRIMARY.configure(VAR.FRAME_STYLE_PRIMARY, background=VAR.GUI_COLOR_PRIMARY)

    STYLE_FRAME_SECONDARY = ttk.Style()
    STYLE_FRAME_SECONDARY.configure(VAR.FRAME_STYLE_SECONDARY, background=VAR.GUI_COLOR_SECONDARY)