
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure
import numpy as np

from tkinter import *
from tkinter import ttk

from VGC_Var import GRAPH_TYPE_BAR
from VGC_Var import GRAPH_TYPE_PIE
from VGC_Var import GRAPH_TYPE_STACK
from VGC_Var import GRAPH_TYPE_LINE
from VGC_Var import GRAPH_CONTENT_YEARS
from VGC_Var import GRAPH_CONTENT_MONTHS
from VGC_Var import GRAPH_CONTENT_PLATFORMS
from VGC_Var import GRAPH_CONTENT_REGIONS
from VGC_Var import GRAPH_CONTENT_PLATFORM_HOLDERS
from VGC_Var import GRAPH_DATA_ITEMCOUNT
from VGC_Var import GRAPH_DATA_TOTALPRICE
from VGC_Var import GRAPH_DATA_ITEMCOUNTGROWTH
from VGC_Var import GRAPH_DATA_TOTALPRICEGROWTH
from VGC_Var import GRAPH_BAR_COLOR
from VGC_Var import GRAPH_BAR_COLOR_ACTIVE

from VGC_Widgets import Label_
from VGC_Widgets import Combobox_
from VGC_Widgets import Checkbutton_

######################
# initGraph
# --------------------
def initGraph(gui):

    # Graph
    # ------------------
    gui.graph_tool_frame = Frame(gui.graph_frame)
    gui.graph_sub_frame  = Frame(gui.graph_frame, highlightthickness=1, highlightbackground="black", height=350)

    gui.graph_tool_frame.grid(row=0, column=0, sticky="nwse", padx=(0,17), pady=10)
    gui.graph_sub_frame.grid(row=1, column=0, sticky="nwse", padx=(0,17))

    gui.graph_tool_frame.grid_columnconfigure(6, weight=1)

    gui.graph_frame.grid_rowconfigure(0, weight=1)
    gui.graph_frame.grid_rowconfigure(1, weight=0)
    gui.graph_frame.grid_columnconfigure(0, weight=1)

    gui.graph_type_txt = Label_(gui.graph_tool_frame, text="Graph type:")
    gui.graph_type     = Combobox_(gui.graph_tool_frame, width=10)
    gui.graph_type.bind("<<ComboboxSelected>>", gui.onGraphTypeSelect)

    gui.graph_content_txt = Label_(gui.graph_tool_frame, text="Content:")
    gui.graph_content     = Combobox_(gui.graph_tool_frame, width=20)
    gui.graph_content.bind("<<ComboboxSelected>>", gui.onGraphContentSelect)

    gui.graph_data_txt    = Label_(gui.graph_tool_frame, text="Data:")
    gui.graph_data        = Combobox_(gui.graph_tool_frame, width=20)
    gui.graph_data.set(GRAPH_DATA_ITEMCOUNT)
    gui.graph_data.bind("<<ComboboxSelected>>", gui.onGraphDataSelect)

    gui.graph_show_grid   = Checkbutton_(gui.graph_tool_frame, label="Show grid", command=gui.displayGraphs)

    gui.graph_hover_info  = Label_(gui.graph_tool_frame)

    gui.graph_type_txt.grid(row=0, column=0, padx=(0,10))
    gui.graph_type.grid(row=0, column=1, sticky="w", padx=(0,20))

    gui.graph_content_txt.grid(row=0, column=2, padx=(0,10))
    gui.graph_content.grid(row=0, column=3, sticky="w", padx=(0,20))

    gui.graph_data_txt.grid(row=0, column=4, padx=(0,10))
    gui.graph_data.grid(row=0, column=5, sticky="w", padx=(0,20))

    gui.graph_show_grid.grid(row=0, column=6, sticky="w")

    gui.graph_hover_info.grid(row=0, column=7)

    gui.graph_canvas = FigureCanvasTkAgg(master=gui.graph_sub_frame)
    gui.graph_sub_frame.pack_propagate(False)
    gui.graph_canvas.get_tk_widget().pack(expand=True, fill="both")

    gui.graph_frame.grid_forget()

    fillGraphTypeCombobox(gui)
    fillGraphContentCombobox(gui, gui.graph_type.get())
    fillGraphDataCombobox(gui, gui.graph_type.get())

    gui.activeGraphType = gui.graph_type.get()


######################
# fillGraphTypeCombobox
# --------------------
def fillGraphTypeCombobox(gui):
    types = []
    gui.graph_type.delete(0, END)

    types.append(GRAPH_TYPE_BAR)
    types.append(GRAPH_TYPE_PIE)
    types.append(GRAPH_TYPE_STACK)
    types.append(GRAPH_TYPE_LINE)

    gui.graph_type.setValues(types)
    gui.graph_type.set(GRAPH_TYPE_BAR)


######################
# fillGraphContentCombobox
# --------------------
def fillGraphContentCombobox(gui, graphType):
    content = []
    gui.graph_content.delete(0, END)

    if not graphType == GRAPH_TYPE_STACK and not graphType == GRAPH_TYPE_LINE:
        content.append(GRAPH_CONTENT_YEARS)
        content.append(GRAPH_CONTENT_MONTHS)
    content.append(GRAPH_CONTENT_REGIONS)
    content.append(GRAPH_CONTENT_PLATFORMS)
    content.append(GRAPH_CONTENT_PLATFORM_HOLDERS)

    gui.graph_content.setValues(content)

    if len(gui.activeGraphContent) and gui.activeGraphContent in gui.graph_content["values"]:
        gui.graph_content.set(gui.activeGraphContent)
    else:
        if not graphType == GRAPH_TYPE_STACK and not graphType == GRAPH_TYPE_LINE:
            gui.graph_content.set(GRAPH_CONTENT_YEARS)
        else:
            gui.graph_content.set(GRAPH_CONTENT_REGIONS)

    gui.activeGraphContent = gui.graph_content.get()


######################
# fillGraphDataCombobox
# --------------------
def fillGraphDataCombobox(gui, graphType):
    data = []
    gui.graph_data.delete(0, END)

    if graphType == GRAPH_TYPE_STACK or graphType == GRAPH_TYPE_LINE:
        data.append(GRAPH_DATA_ITEMCOUNTGROWTH)
        data.append(GRAPH_DATA_TOTALPRICEGROWTH)
        gui.graph_data.set(GRAPH_DATA_ITEMCOUNTGROWTH)
    else:
        data.append(GRAPH_DATA_ITEMCOUNT)
        data.append(GRAPH_DATA_TOTALPRICE)
        gui.graph_data.set(GRAPH_DATA_ITEMCOUNT)

    gui.graph_data.setValues(data)


######################
# drawGraph
# --------------------
def drawGraph(gui, data, canvas, graphType, graphContent, graphData):
    group    = ""
    subGroup = ""

    # Group data
    if graphContent == GRAPH_CONTENT_YEARS:
        group = "year"
    if graphContent == GRAPH_CONTENT_MONTHS:
        group = "month"
    if graphContent == GRAPH_CONTENT_PLATFORMS:
        group = "platform"
        if graphData == GRAPH_DATA_ITEMCOUNTGROWTH or graphData == GRAPH_DATA_TOTALPRICEGROWTH:
            subGroup = "year"
    if graphContent == GRAPH_CONTENT_REGIONS:
        group = "region"
        if graphData == GRAPH_DATA_ITEMCOUNTGROWTH or graphData == GRAPH_DATA_TOTALPRICEGROWTH:
            subGroup = "year"
    if graphContent == GRAPH_CONTENT_PLATFORM_HOLDERS:
        group = "platform holder"
        if graphData == GRAPH_DATA_ITEMCOUNTGROWTH or graphData == GRAPH_DATA_TOTALPRICEGROWTH:
            subGroup = "year"

    data.groupGraphData(group, subGroup = subGroup)

    if graphType == GRAPH_TYPE_BAR:
        drawBarGraph(gui, data, canvas, graphContent, graphData)
    if graphType == GRAPH_TYPE_PIE:
        drawPieChart(gui, data, canvas, graphContent, graphData)
    if graphType == GRAPH_TYPE_STACK:
        drawStackPlot(gui, data, canvas, graphContent, graphData)
    if graphType == GRAPH_TYPE_LINE:
        drawLinePlot(gui, data, canvas, graphContent, graphData)


######################
# widthPercentage
# --------------------
def widthPercentage(canvasWidth, width):
    return (1 / canvasWidth) * width


######################
# drawBarGraph
# --------------------
def drawBarGraph(gui, data, canvas, graphContent, graphData):

    # Notification handler
    def onNotify(event):
        active = False

        if event.inaxes == ax:
            for i, bar in enumerate(bars):
                if bar.contains_point([event.x, event.y]):
                    active = True
                    value  = str(values[i])

                    if not int(values[i]) == values[i]:
                        value = "{:.2f}".format(values[i])

                    # Set hover info
                    gui.graph_hover_info.set(labels[i] + ": " + value)
                    # Set active color
                    bar.set_facecolor(GRAPH_BAR_COLOR_ACTIVE)
                else:
                    bar.set_facecolor(GRAPH_BAR_COLOR)

            if active == False:
                # Reset hover info
                gui.graph_hover_info.set("")

            # Update graph
            canvas.draw_idle()


    # Get canvas dimensions
    canvasWidth  = canvas.get_tk_widget().winfo_width()
    canvasHeight = canvas.get_tk_widget().winfo_height()

    values = []
    labels = []

    maxLabelLen = 0
    barWidth    = int(canvasWidth/len(data.graph_groups))

    # Get values and labels
    for groupKey in sorted(data.graph_groups.keys()):
        if graphData == GRAPH_DATA_ITEMCOUNT:
            itemValue = data.graph_groups[groupKey].item_count
        if graphData == GRAPH_DATA_TOTALPRICE:
            itemValue = data.graph_groups[groupKey].total_price

        values.append(itemValue)
        labels.append(groupKey)

        if len(groupKey) > maxLabelLen:
            maxLabelLen = len(groupKey)


    # Setup graph
    fig = Figure(figsize=(canvasWidth/100, canvasHeight/100), dpi=100)
    fig.tight_layout()
    fig.subplots_adjust(left   = widthPercentage(canvasWidth, 90),
                        bottom = widthPercentage(canvasHeight, 40) + widthPercentage(canvasHeight, maxLabelLen*2),
                        right  = (1-widthPercentage(canvasWidth, 20)),
                        top    = (1-widthPercentage(canvasHeight, 35)))

    ax = fig.add_subplot()

    if gui.graph_show_grid.get():
        ax.grid(color="#95A5A6", linestyle="--", linewidth=2, axis="y", alpha=0.7)
    ax.margins(x=0.005, y=0.05)
    ax.autoscale(True)
    ax.set_ylabel(graphData)
    ax.set_title(graphContent)
    ax.set_xticks(np.arange(len(values)))
    ax.set_xticklabels(labels, rotation=330, ha="left", fontsize=6)
    bars = ax.bar(range(len(values)), values, color=GRAPH_BAR_COLOR, alpha=1)

    canvas.figure = fig
    canvas.mpl_connect("motion_notify_event", onNotify)
    canvas.draw()


######################
# drawPieChart
# --------------------
def drawPieChart(gui, data, canvas, graphContent, graphData):

    # Notification handler
    def onNotify(event):
        active = False

        if event.inaxes == ax:
            for i, wedge in enumerate(wedges):
                if wedge.contains_point([event.x, event.y]):
                    active = True
                    value  = str(values[i])

                    if not int(values[i]) == values[i]:
                        value = "{:.2f}".format(values[i])

                    # Set hover info
                    gui.graph_hover_info.set(labels[i] + ": " + value + " (" + "{:.2f}".format(percentages[i]) + "%)")
                    # Set active color
                    wedge.set_alpha(1)
                else:
                    wedge.set_alpha(0.75)

            if active == False:
                # Reset hover info
                gui.graph_hover_info.set("")

            # Update graph
            canvas.draw_idle()


    # Get canvas dimensions
    canvasWidth  = canvas.get_tk_widget().winfo_width()
    canvasHeight = canvas.get_tk_widget().winfo_height()

    labels        = []
    displayLabels = []
    values        = []
    percentages   = []
    explode       = []

    totalValue = 0

    # Find total value to be displayed in the chart
    for groupKey in data.graph_groups.keys():
        if graphData == GRAPH_DATA_ITEMCOUNT:
            totalValue += data.graph_groups[groupKey].item_count
        if graphData == GRAPH_DATA_TOTALPRICE:
            totalValue += data.graph_groups[groupKey].total_price

    if totalValue:
        for groupKey in sorted(data.graph_groups.keys()):

            if graphData == GRAPH_DATA_ITEMCOUNT:
                itemValue = data.graph_groups[groupKey].item_count
            if graphData == GRAPH_DATA_TOTALPRICE:
                itemValue = data.graph_groups[groupKey].total_price

            # Calculate group percentage
            percent = 100 / totalValue * itemValue

            percentages.append(percent)
            values.append(itemValue)
            explode.append(0.1)

            labels.append(groupKey)

            if percent > 5:
                displayLabels.append(groupKey)
            else:
                displayLabels.append("")

    # Setup graph
    fig = Figure(figsize=(canvasWidth/100, canvasHeight/100), dpi=100)
    fig.tight_layout()
    fig.subplots_adjust(left   = widthPercentage(canvasWidth, 90),
                        bottom = widthPercentage(canvasHeight, 35),
                        right  = (1-widthPercentage(canvasWidth, 20)),
                        top    = (1-widthPercentage(canvasHeight, 35)))

    ax = fig.add_subplot()
    ax.margins(x=0.005, y=0.05)
    ax.autoscale(True)
    ax.set_title(graphContent)

    wedges, temp = ax.pie(percentages, labels=displayLabels, explode=explode, startangle=90, normalize=True, wedgeprops={'alpha':0.75})

    colors = [w.get_facecolor() for w in wedges]

    canvas.figure = fig
    canvas.mpl_connect("motion_notify_event", onNotify)
    canvas.draw()


######################
# drawStackPlot
# --------------------
def drawStackPlot(gui, data, canvas, graphContent, graphData):

    # Get canvas dimensions
    canvasWidth  = canvas.get_tk_widget().winfo_width()
    canvasHeight = canvas.get_tk_widget().winfo_height()

    dates  = []
    values = {}

    # Find all dates
    for groupKey in sorted(data.graph_groups.keys()):
        for subGroup in sorted(data.graph_groups[groupKey].sub.keys()):
            dates.append(subGroup)

    # Remove duplicated dates
    dates = sorted(list(set(dates)))

    # Sum data
    for groupKey in sorted(data.graph_groups.keys()):
        values[groupKey] = []
        sum = 0

        for date in dates:
            if date in data.graph_groups[groupKey].sub.keys():
                if graphData == GRAPH_DATA_ITEMCOUNTGROWTH:
                    sum += data.graph_groups[groupKey].sub[date].item_count
                if graphData == GRAPH_DATA_TOTALPRICEGROWTH:
                    sum += data.graph_groups[groupKey].sub[date].total_price

            values[groupKey].append(sum)

    # Setup graph
    fig = Figure(figsize=(canvasWidth/100, canvasHeight/100), dpi=100)
    fig.tight_layout()
    fig.subplots_adjust(left   = widthPercentage(canvasWidth, 90),
                        bottom = widthPercentage(canvasHeight, 40),
                        right  = (1-widthPercentage(canvasWidth, 20)),
                        top    = (1-widthPercentage(canvasHeight, 35)))

    ax = fig.add_subplot()
    ax.margins(x=0, y=0)
    ax.autoscale(True)
    ax.set_ylabel(graphData)
    ax.set_title(graphContent)

    if gui.graph_show_grid.get():
        ax.grid(color="#95A5A6", linestyle="--", linewidth=2, axis="y", alpha=0.7)

    stacks = ax.stackplot(dates, values.values(), labels=values.keys())

    ax.legend(loc='upper left', ncol=5, fontsize=6)

    canvas.figure = fig
    canvas.draw()


######################
# drawLinePlot
# --------------------
def drawLinePlot(gui, data, canvas, graphContent, graphData):

    # Get canvas dimensions
    canvasWidth  = canvas.get_tk_widget().winfo_width()
    canvasHeight = canvas.get_tk_widget().winfo_height()

    dates  = []
    values = {}

    # Find all dates
    for groupKey in sorted(data.graph_groups.keys()):
        for subGroup in sorted(data.graph_groups[groupKey].sub.keys()):
            dates.append(subGroup)

    # Remove duplicated dates
    dates = sorted(list(set(dates)))

    # Sum Data
    for groupKey in sorted(data.graph_groups.keys()):
        values[groupKey] = []
        sum = 0

        for date in dates:
            if date in data.graph_groups[groupKey].sub.keys():
                if graphData == GRAPH_DATA_ITEMCOUNTGROWTH:
                    sum += data.graph_groups[groupKey].sub[date].item_count
                if graphData == GRAPH_DATA_TOTALPRICEGROWTH:
                    sum += data.graph_groups[groupKey].sub[date].total_price

            values[groupKey].append(sum)

    # Setup graph
    fig = Figure(figsize=(canvasWidth/100, canvasHeight/100), dpi=100)
    fig.tight_layout()
    fig.subplots_adjust(left   = widthPercentage(canvasWidth, 90),
                        bottom = widthPercentage(canvasHeight, 40),
                        right  = (1-widthPercentage(canvasWidth, 20)),
                        top    = (1-widthPercentage(canvasHeight, 35)))

    ax = fig.add_subplot()
    ax.margins(x=0, y=0)
    ax.autoscale(True)
    ax.set_ylabel(graphData)
    ax.set_title(graphContent)

    if gui.graph_show_grid.get():
        ax.grid(color="#95A5A6", linestyle="--", linewidth=2, axis="y", alpha=0.7)


    for groupKey in sorted(data.graph_groups.keys()):
        ax.plot(dates, values[groupKey], label=groupKey, alpha=0.5)

    ax.legend(loc='upper left', ncol=5, fontsize=6)

    canvas.figure = fig
    canvas.draw()
