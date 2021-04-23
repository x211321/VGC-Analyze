from tkinter import *
from tkinter import ttk

from VGC_Var import GRAPH_CONTENT_TOTALPRICE_YEAR
from VGC_Var import GRAPH_CONTENT_ITEMCOUNT_YEAR

from VGC_Widgets import Label_
from VGC_Widgets import Combobox_


######################
# initGraph
# --------------------
def initGraph(gui):

    # Graph
    # ------------------
    gui.graph_tool_frame = Frame(gui.graph_frame)
    gui.graph_sub_frame  = Frame(gui.graph_frame)

    gui.graph_tool_frame.grid(row=0, column=0, sticky="nwse", padx=10, pady=10)
    gui.graph_sub_frame.grid(row=1, column=0, sticky="nwse")

    gui.graph_frame.grid_rowconfigure(0, weight=1)
    gui.graph_frame.grid_rowconfigure(1, weight=1)
    gui.graph_frame.grid_columnconfigure(0, weight=1)

    gui.graph_content_txt = Label_(gui.graph_tool_frame, text="Chart content:")
    gui.graph_content     = Combobox_(gui.graph_tool_frame, values=(GRAPH_CONTENT_TOTALPRICE_YEAR, GRAPH_CONTENT_ITEMCOUNT_YEAR), width=15)
    gui.graph_content.set(GRAPH_CONTENT_TOTALPRICE_YEAR)
    gui.graph_content.item.bind("<<ComboboxSelected>>", gui.displayGraphs)

    gui.graph_content_txt.item.grid(row=0, column=0, padx=(0,10))
    gui.graph_content.item.grid(row=0, column=1)

    gui.graph_canvas = Canvas(gui.graph_sub_frame, bg="#FFF", highlightthickness=1, highlightbackground="black")
    gui.graph_canvas.pack(expand=True, fill="both", padx=(0, 17), pady=(0,0))
    gui.graph_canvas.bind("<Configure>", lambda x:onGraphResiz(gui))

    gui.graph_frame.grid_forget()


######################
# onGraphResiz
# --------------------
def onGraphResiz(gui):
    if gui.graph_frame.winfo_ismapped:
        gui.displayGraphs()


######################
# drawBarGraph
# --------------------
def drawBarGraph(data, canvas, mode):

    # Get canvas dimensions
    canvasWidth  = canvas.winfo_width()
    canvasHeight = canvas.winfo_height()

    # Clear canvas
    canvas.delete("all")

    paddingTop    = 20
    paddingBottom = 50
    paddingLeft   = 50
    paddingRight  = 20

    paddingXAxis      = 10
    paddingXAxisLabel = 20
    paddingYAxis      = 10
    paddingYAxisLabel = 10

    maxValue = 0

    stepSize = 20

    startX    = paddingLeft
    startY    = canvasHeight - paddingBottom

    maxBarWidth  = canvasWidth  - paddingLeft - paddingRight
    maxBarHeight = canvasHeight - paddingTop - paddingBottom

    barWidth  = int(maxBarWidth/len(data.graph_groups))
    barHeight = 0

    # Find maximum value to be displayed in the graph
    for groupKey in data.graph_groups.keys():
        if mode == GRAPH_CONTENT_ITEMCOUNT_YEAR:
            if data.graph_groups[groupKey].item_count > maxValue:
                maxValue = data.graph_groups[groupKey].item_count
        if mode == GRAPH_CONTENT_TOTALPRICE_YEAR:
            if data.graph_groups[groupKey].total_price > maxValue:
                maxValue = data.graph_groups[groupKey].total_price

    # Draw axes
    # X
    canvas.create_line(startX-paddingYAxis, startY+paddingXAxis, startX+maxBarWidth, startY+paddingXAxis, width="2")
    # Y
    canvas.create_line(startX-paddingYAxis, startY+paddingXAxis, startX-paddingYAxis, startY-maxBarHeight, width="2")

    # Draw y-axis labels
    stepCount = int((maxBarHeight) / stepSize) + 1

    for i in range(stepCount):

        text = int((maxValue/stepCount) * i)

        canvas.create_text(startX-paddingYAxis-paddingYAxisLabel, startY-(stepSize*i), text=text, width=paddingLeft, anchor="e")

    # Draw graph
    if maxValue:
        for groupKey in sorted(data.graph_groups.keys()):

            if mode == GRAPH_CONTENT_ITEMCOUNT_YEAR:
                itemValue = data.graph_groups[groupKey].item_count
            if mode == GRAPH_CONTENT_TOTALPRICE_YEAR:
                itemValue = data.graph_groups[groupKey].total_price

            barHeight = int(maxBarHeight / maxValue * itemValue)

            endX = startX + barWidth
            endY = startY - barHeight

            # Draw bar
            canvas.create_rectangle(startX, startY, endX, endY, fill="#FF0", outline="black", activefill="#00F")

            # Draw x-axis label
            canvas.create_text(startX+(barWidth/2), startY+paddingXAxis+paddingXAxisLabel, text=groupKey, width=barWidth-2)

            startX = endX