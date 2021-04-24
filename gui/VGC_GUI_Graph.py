from tkinter import *
from tkinter import ttk

from VGC_Var import GRAPH_CONTENT_YEARS
from VGC_Var import GRAPH_CONTENT_PLATFORMS
from VGC_Var import GRAPH_CONTENT_REGIONS
from VGC_Var import GRAPH_CONTENT_PLATFORM_HOLDERS
from VGC_Var import GRAPH_DATA_ITEMCOUNT
from VGC_Var import GRAPH_DATA_TOTALPRICE

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

    gui.graph_tool_frame.grid(row=0, column=0, sticky="nwse", padx=(0,17), pady=10)
    gui.graph_sub_frame.grid(row=1, column=0, sticky="nwse")

    gui.graph_tool_frame.grid_columnconfigure(3, weight=1)

    gui.graph_frame.grid_rowconfigure(0, weight=1)
    gui.graph_frame.grid_rowconfigure(1, weight=1)
    gui.graph_frame.grid_columnconfigure(0, weight=1)

    gui.graph_content_txt = Label_(gui.graph_tool_frame, text="Graph content:")
    gui.graph_content     = Combobox_(gui.graph_tool_frame, values=(GRAPH_CONTENT_YEARS, GRAPH_CONTENT_PLATFORMS, GRAPH_CONTENT_PLATFORM_HOLDERS, GRAPH_CONTENT_REGIONS), width=15)
    gui.graph_content.set(GRAPH_CONTENT_YEARS)
    gui.graph_content.bind("<<ComboboxSelected>>", gui.displayGraphs)

    gui.graph_data_txt    = Label_(gui.graph_tool_frame, text="Data:")
    gui.graph_data        = Combobox_(gui.graph_tool_frame, values=(GRAPH_DATA_ITEMCOUNT, GRAPH_DATA_TOTALPRICE), width=15)
    gui.graph_data.set(GRAPH_DATA_ITEMCOUNT)
    gui.graph_data.bind("<<ComboboxSelected>>", gui.displayGraphs)

    gui.graph_hover_info  = Label_(gui.graph_tool_frame)

    gui.graph_content_txt.grid(row=0, column=0, padx=(0,10))
    gui.graph_content.grid(row=0, column=1, sticky="w", padx=(0,20))

    gui.graph_data_txt.grid(row=0, column=2, padx=(0,10))
    gui.graph_data.grid(row=0, column=3, sticky="w")

    gui.graph_hover_info.grid(row=0, column=4)

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
def drawBarGraph(gui, data, canvas, graphContent, graphData):

    # Get canvas dimensions
    canvasWidth  = canvas.winfo_width()
    canvasHeight = canvas.winfo_height()

    # Group data
    if graphContent == GRAPH_CONTENT_YEARS:
        gui.collectionData.groupGraphData("year")
    if graphContent == GRAPH_CONTENT_PLATFORMS:
        gui.collectionData.groupGraphData("platform")
    if graphContent == GRAPH_CONTENT_REGIONS:
        gui.collectionData.groupGraphData("region")
    if graphContent == GRAPH_CONTENT_PLATFORM_HOLDERS:
        gui.collectionData.groupGraphData("platform holder")

    # Clear canvas
    canvas.delete("all")

    paddingTop    = 20
    paddingBottom = 60
    paddingLeft   = 50
    paddingRight  = 20

    paddingXAxis      = 10
    paddingXAxisLabel =  5
    paddingYAxis      = 10
    paddingYAxisLabel = 10

    maxValue = 0

    stepSize = 20

    startX = paddingLeft
    startY = canvasHeight - paddingBottom

    maxBarWidth  = canvasWidth  - paddingLeft - paddingRight
    maxBarHeight = canvasHeight - paddingTop - paddingBottom

    barWidth  = int(maxBarWidth/len(data.graph_groups))
    barHeight = 0

    # Find maximum value to be displayed in the graph
    for groupKey in data.graph_groups.keys():
        if graphData == GRAPH_DATA_ITEMCOUNT:
            if data.graph_groups[groupKey].item_count > maxValue:
                maxValue = data.graph_groups[groupKey].item_count
        if graphData == GRAPH_DATA_TOTALPRICE:
            if data.graph_groups[groupKey].total_price > maxValue:
                maxValue = data.graph_groups[groupKey].total_price

    # Draw axes
    # X
    canvas.create_line(startX-paddingYAxis, startY+paddingXAxis, startX+maxBarWidth, startY+paddingXAxis, width="2")
    # Y
    canvas.create_line(startX-paddingYAxis, startY+paddingXAxis, startX-paddingYAxis, startY-maxBarHeight, width="2")

    # Draw y-axis labels
    stepCount = int((maxBarHeight) / stepSize) + 1

    for i in range(stepCount+1):

        if i > 0 and str(int((maxValue/stepCount) * i)) == lastText:
            text = ""
        else:
            text = str(int((maxValue/stepCount) * i))
            lastText = text

        canvas.create_text(startX-paddingYAxis-paddingYAxisLabel, startY+paddingXAxis-(stepSize*i), text=text, width=paddingLeft, anchor="e")

    # Draw graph
    if maxValue:
        for groupKey in sorted(data.graph_groups.keys()):

            if graphData == GRAPH_DATA_ITEMCOUNT:
                itemValue = data.graph_groups[groupKey].item_count
            if graphData == GRAPH_DATA_TOTALPRICE:
                itemValue = data.graph_groups[groupKey].total_price

            barHeight = int(maxBarHeight / maxValue * itemValue)

            endX = startX + barWidth
            endY = startY - barHeight

            # Draw bar
            index = canvas.create_rectangle(startX, startY+paddingXAxis-1, endX, endY, fill="#FFD754", outline="#000", activefill="#547CFF")

            def handler(event, self=gui, group=groupKey, itemValue=itemValue):
                return gui.onGraphEnter(event, group, itemValue)

            canvas.tag_bind(index, "<Enter>", handler)
            canvas.tag_bind(index, "<Leave>", gui.onGraphLeave)

            # Draw x-axis label
            if barWidth < 40 and len(groupKey) > 4:
                words   = groupKey.replace("(", "").replace("-", "").replace("/", " ").split()
                letters = [word[0] for word in words]
                text    =  "".join(letters)[0:4]
            else:
                text = groupKey

            canvas.create_text(startX+(barWidth/2), startY+paddingXAxis+paddingXAxisLabel, text=text, width=barWidth-2, anchor="n", font=("", 8))

            startX = endX