from lib.Locale import _
from lib.Locale import locCurrency

try:
    import PIL
except ImportError:
    pillow_available = False
else:
    pillow_available = True

if pillow_available:
    try:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
    except ImportError:
        matplotlib_available = False
        print("Matplotlib not found")
    else:
        matplotlib_available = True
else:
    matplotlib_available = False

from tkinter import *
from tkinter import ttk

import lib.Var as VAR

from lib.Widgets import Frame_
from lib.Widgets import Label_
from lib.Widgets import Combobox_
from lib.Widgets import Checkbutton_


######################
# GUI_Graph
# --------------------
class GUI_Graph(Frame_):

    def __init__(self, master, width=0, height=0):
        super().__init__(master=master, width=width, height=height, style=VAR.FRAME_STYLE_SECONDARY)

        self.setDefaultLabelStyle(VAR.LABEL_STYLE_SECONDARY)

        self.collectionData = master.collectionData

        self.activeGraphType    = ""
        self.activeGraphContent = ""

        self.init()


    def init(self):
        # Graph
        # ------------------
        self.graph_tool_frame = Frame_(self, style=VAR.FRAME_STYLE_SECONDARY)
        self.graph_sub_frame  = Frame_(self, style=VAR.FRAME_STYLE_SECONDARY, borderwidth=1, relief="groove", height=350)

        self.graph_tool_frame.grid(row=0, column=0, sticky="nwse", padx=(0,17), pady=10)
        self.graph_sub_frame.grid(row=1, column=0, sticky="nwse", padx=(0,17))

        self.graph_tool_frame.grid_columnconfigure(6, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.graph_type_txt    = Label_(self.graph_tool_frame, text=_("Graph type:"))
        self.graph_type        = Combobox_(self.graph_tool_frame, width=10, state="readonly")
        self.graph_type.bind("<<ComboboxSelected>>", self.onGraphTypeSelect)

        self.graph_content_txt = Label_(self.graph_tool_frame, text=_("Content:"))
        self.graph_content     = Combobox_(self.graph_tool_frame, width=20, state="readonly")
        self.graph_content.bind("<<ComboboxSelected>>", self.onGraphContentSelect)

        self.graph_data_txt    = Label_(self.graph_tool_frame, text=_("Data:"))
        self.graph_data        = Combobox_(self.graph_tool_frame, width=35, state="readonly")
        self.graph_data.set(VAR.GRAPH_DATA_ITEMCOUNT)
        self.graph_data.bind("<<ComboboxSelected>>", self.onGraphDataSelect)

        self.graph_show_grid   = Checkbutton_(self.graph_tool_frame, label=_("Show grid"), command=self.displayGraphs, style=VAR.CHECKBOX_STYLE_SECUNDARY)

        self.graph_hover_info  = Label_(self.graph_tool_frame)

        self.graph_type_txt.grid(row=0, column=0, padx=(0,10))
        self.graph_type.grid(row=0, column=1, sticky="w", padx=(0,20))

        self.graph_content_txt.grid(row=0, column=2, padx=(0,10))
        self.graph_content.grid(row=0, column=3, sticky="w", padx=(0,20))

        self.graph_data_txt.grid(row=0, column=4, padx=(0,10))
        self.graph_data.grid(row=0, column=5, sticky="w", padx=(0,20))

        self.graph_show_grid.grid(row=0, column=6, sticky="w")

        self.graph_hover_info.grid(row=0, column=7)

        if matplotlib_available:
            self.graph_canvas = FigureCanvasTkAgg(master=self.graph_sub_frame, figure=Figure())
            self.graph_sub_frame.pack_propagate(False)
            self.graph_canvas.get_tk_widget().pack(expand=True, fill="both")
        else:
            self.label_matplotlib_missing = Label_(self.graph_sub_frame,
                                                   font=(20), style=VAR.LABEL_STYLE_WARNING,
                                                   text=_("matplotlib module not found, can't render graphs."))

            self.label_matplotlib_missing.pack(pady=20)

        self.fillGraphTypeCombobox()
        self.fillGraphContentCombobox()
        self.fillGraphDataCombobox()


    ######################
    # fillGraphTypeCombobox
    # --------------------
    def fillGraphTypeCombobox(self):
        types = []
        self.graph_type.delete(0, END)

        types.append(VAR.GRAPH_TYPE_BAR)
        types.append(VAR.GRAPH_TYPE_PIE)
        types.append(VAR.GRAPH_TYPE_AREA)
        types.append(VAR.GRAPH_TYPE_LINE)

        self.graph_type.setValues(types)
        self.graph_type.set(VAR.GRAPH_TYPE_BAR)


    ######################
    # fillGraphContentCombobox
    # --------------------
    def fillGraphContentCombobox(self):
        content   = []
        graphType = self.graph_type.get()

        self.graph_content.delete(0, END)

        if not graphType == VAR.GRAPH_TYPE_AREA and not graphType == VAR.GRAPH_TYPE_LINE:
            content.append(VAR.GRAPH_CONTENT_YEARS)
            content.append(VAR.GRAPH_CONTENT_MONTHS)
            content.append(VAR.GRAPH_CONTENT_YEARS_ADDED)
            content.append(VAR.GRAPH_CONTENT_MONTHS_ADDED)
        content.append(VAR.GRAPH_CONTENT_REGIONS)
        content.append(VAR.GRAPH_CONTENT_PLATFORMS)
        content.append(VAR.GRAPH_CONTENT_PLATFORM_HOLDERS)

        self.graph_content.setValues(content)

        if len(self.activeGraphContent) and self.activeGraphContent in self.graph_content["values"]:
            self.graph_content.set(self.activeGraphContent)
        else:
            if not graphType == VAR.GRAPH_TYPE_AREA and not graphType == VAR.GRAPH_TYPE_LINE:
                self.graph_content.set(VAR.GRAPH_CONTENT_YEARS)
            else:
                self.graph_content.set(VAR.GRAPH_CONTENT_REGIONS)

        self.activeGraphContent = self.graph_content.get()


    ######################
    # fillGraphDataCombobox
    # --------------------
    def fillGraphDataCombobox(self):
        data      = []
        graphType = self.graph_type.get()

        self.graph_data.delete(0, END)

        if graphType == VAR.GRAPH_TYPE_AREA or graphType == VAR.GRAPH_TYPE_LINE:
            data.append(VAR.GRAPH_DATA_ITEMCOUNTGROWTH_PURCHASE)
            data.append(VAR.GRAPH_DATA_ITEMCOUNTGROWTH_ADDED)
            data.append(VAR.GRAPH_DATA_TOTALPRICEGROWTH_PURCHASE)
            data.append(VAR.GRAPH_DATA_TOTALPRICEGROWTH_ADDED)
            self.graph_data.set(VAR.GRAPH_DATA_ITEMCOUNTGROWTH_PURCHASE)
        else:
            data.append(VAR.GRAPH_DATA_ITEMCOUNT)
            data.append(VAR.GRAPH_DATA_TOTALPRICE)
            self.graph_data.set(VAR.GRAPH_DATA_ITEMCOUNT)

        self.graph_data.setValues(data)


    ######################
    # onGraphTypeSelect
    # --------------------
    def onGraphTypeSelect(self, a = None):
        newType =self.graph_type.get()

        if (((newType == VAR.GRAPH_TYPE_AREA or newType == VAR.GRAPH_TYPE_LINE) and
           (self.activeGraphType == VAR.GRAPH_TYPE_BAR or self.activeGraphType == VAR.GRAPH_TYPE_PIE or self.activeGraphType == "")) or
           ((self.activeGraphType == VAR.GRAPH_TYPE_AREA or self.activeGraphType == VAR.GRAPH_TYPE_LINE) and
           (newType == VAR.GRAPH_TYPE_BAR or newType == VAR.GRAPH_TYPE_PIE))):

            self.fillGraphContentCombobox()
            self.fillGraphDataCombobox()

        if newType == VAR.GRAPH_TYPE_PIE:
            self.graph_show_grid.config(state=DISABLED)
        else:
            self.graph_show_grid.config(state=NORMAL)

        self.activeGraphType = self.graph_type.get()

        self.displayGraphs()


    ######################
    # onGraphContentSelect
    # --------------------
    def onGraphContentSelect(self, a = None):
        self.activeGraphContent = self.graph_content.get()
        self.displayGraphs()


    ######################
    # onGraphDataSelect
    # --------------------
    def onGraphDataSelect(self, a = None):
        self.displayGraphs()


    ######################
    # displayGraphs
    # --------------------
    def displayGraphs(self):
        if matplotlib_available:
            canvas       = self.graph_canvas
            graphType    = self.graph_type.get()
            graphContent = self.graph_content.get()
            graphData    = self.graph_data.get()

            group    = ""
            subGroup = ""

            # Group data
            if graphContent == VAR.GRAPH_CONTENT_YEARS:
                group = VAR.GROUP_BY_YEAR
            if graphContent == VAR.GRAPH_CONTENT_MONTHS:
                group = VAR.GROUP_BY_MONTH
            if graphContent == VAR.GRAPH_CONTENT_YEARS_ADDED:
                group = VAR.GROUP_BY_YEAR_ADDED
            if graphContent == VAR.GRAPH_CONTENT_MONTHS_ADDED:
                group = VAR.GROUP_BY_MONTH_ADDED
            if graphContent == VAR.GRAPH_CONTENT_PLATFORMS:
                group = VAR.GROUP_BY_PLATFORM
                if graphData == VAR.GRAPH_DATA_ITEMCOUNTGROWTH_PURCHASE or graphData == VAR.GRAPH_DATA_TOTALPRICEGROWTH_PURCHASE:
                    subGroup = VAR.GROUP_BY_YEAR
                if graphData == VAR.GRAPH_DATA_ITEMCOUNTGROWTH_ADDED or graphData == VAR.GRAPH_DATA_TOTALPRICEGROWTH_ADDED:
                    subGroup = VAR.GROUP_BY_YEAR_ADDED
            if graphContent == VAR.GRAPH_CONTENT_REGIONS:
                group = VAR.GROUP_BY_REGION
                if graphData == VAR.GRAPH_DATA_ITEMCOUNTGROWTH_PURCHASE or graphData == VAR.GRAPH_DATA_TOTALPRICEGROWTH_PURCHASE:
                    subGroup = VAR.GROUP_BY_YEAR
                if graphData == VAR.GRAPH_DATA_ITEMCOUNTGROWTH_ADDED or graphData == VAR.GRAPH_DATA_TOTALPRICEGROWTH_ADDED:
                    subGroup = VAR.GROUP_BY_YEAR_ADDED
            if graphContent == VAR.GRAPH_CONTENT_PLATFORM_HOLDERS:
                group = VAR.GROUP_BY_PLATFORMHOLDER
                if graphData == VAR.GRAPH_DATA_ITEMCOUNTGROWTH_PURCHASE or graphData == VAR.GRAPH_DATA_TOTALPRICEGROWTH_PURCHASE:
                    subGroup = VAR.GROUP_BY_YEAR
                if graphData == VAR.GRAPH_DATA_ITEMCOUNTGROWTH_ADDED or graphData == VAR.GRAPH_DATA_TOTALPRICEGROWTH_ADDED:
                    subGroup = VAR.GROUP_BY_YEAR_ADDED

            self.collectionData.groupGraphData(group, subGroup = subGroup)

            if graphType == VAR.GRAPH_TYPE_BAR:
                self.drawBarGraph(self.collectionData, canvas, graphContent, graphData)
            if graphType == VAR.GRAPH_TYPE_PIE:
                self.drawPieChart(self.collectionData, canvas, graphContent, graphData)
            if graphType == VAR.GRAPH_TYPE_AREA:
                self.drawStackPlot(self.collectionData, canvas, graphContent, graphData)
            if graphType == VAR.GRAPH_TYPE_LINE:
                self.drawLinePlot(self.collectionData, canvas, graphContent, graphData)


    ######################
    # widthPercentage
    # --------------------
    def widthPercentage(self, canvasWidth, width):
        return (1 / canvasWidth) * width


    ######################
    # drawBarGraph
    # --------------------
    def drawBarGraph(self, data, canvas, graphContent, graphData):

        # Notification handler
        def onNotify(event):
            active = False

            if event.inaxes == ax:
                for i, bar in enumerate(bars):
                    if bar.contains_point([event.x, event.y]):
                        active = True
                        value  = str(values[i])

                        if not int(values[i]) == values[i]:
                            value = locCurrency(values[i])

                        # Set hover info
                        self.graph_hover_info.set(labels[i] + ": " + value)
                        # Set active color
                        bar.set_facecolor(VAR.GRAPH_BAR_COLOR_ACTIVE)
                    else:
                        bar.set_facecolor(VAR.GRAPH_BAR_COLOR)

                if active == False:
                    # Reset hover info
                    self.graph_hover_info.set("")

                # Update graph
                canvas.draw_idle()


        if not len(data.graph_groups):
            canvas.figure = Figure()
            canvas.draw()
        else:
            # Get canvas dimensions
            canvasWidth  = canvas.get_tk_widget().winfo_width()
            canvasHeight = canvas.get_tk_widget().winfo_height()

            values = []
            labels = []

            maxLabelLen = 0

            # Get values and labels
            for groupKey in sorted(data.graph_groups.keys()):
                if graphData == VAR.GRAPH_DATA_ITEMCOUNT:
                    itemValue = data.graph_groups[groupKey].item_count
                if graphData == VAR.GRAPH_DATA_TOTALPRICE:
                    itemValue = data.graph_groups[groupKey].total_price

                values.append(itemValue)
                labels.append(groupKey)

                if len(groupKey) > maxLabelLen:
                    maxLabelLen = len(groupKey)


            # Setup graph
            fig = Figure(figsize=(canvasWidth/100, canvasHeight/100), dpi=100)
            fig.tight_layout()
            fig.subplots_adjust(left   = self.widthPercentage(canvasWidth, 90),
                                bottom = self.widthPercentage(canvasHeight, 40) + self.widthPercentage(canvasHeight, maxLabelLen*2),
                                right  = (1-self.widthPercentage(canvasWidth, 20)),
                                top    = (1-self.widthPercentage(canvasHeight, 35)))

            ax = fig.add_subplot()

            if self.graph_show_grid.get():
                ax.grid(color="#95A5A6", linestyle="--", linewidth=2, axis="y", alpha=0.7)
            ax.margins(x=0.005, y=0.05)
            ax.autoscale(True)
            ax.set_ylabel(graphData)
            ax.set_title(graphContent)
            ax.set_xticks(range(len(values)))
            ax.set_xticklabels(labels, rotation=330, ha="left", fontsize=6)
            bars = ax.bar(range(len(values)), values, color=VAR.GRAPH_BAR_COLOR, alpha=1)

            canvas.figure = fig
            canvas.mpl_connect("motion_notify_event", onNotify)
            canvas.draw()


    ######################
    # drawPieChart
    # --------------------
    def drawPieChart(self, data, canvas, graphContent, graphData):

        # Notification handler
        def onNotify(event):
            active = False

            if event.inaxes == ax:
                for i, wedge in enumerate(wedges):
                    if wedge.contains_point([event.x, event.y]):
                        active = True
                        value  = str(values[i])

                        if not int(values[i]) == values[i]:
                            value = locCurrency(values[i])

                        # Set hover info
                        self.graph_hover_info.set(labels[i] + ": " + value + " (" + "{:.2f}".format(percentages[i]) + "%)")
                        # Set active color
                        wedge.set_alpha(1)
                    else:
                        wedge.set_alpha(0.75)

                if active == False:
                    # Reset hover info
                    self.graph_hover_info.set("")

                # Update graph
                canvas.draw_idle()

        if not len(data.graph_groups):
            canvas.figure = Figure()
            canvas.draw()
        else:

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
                if graphData == VAR.GRAPH_DATA_ITEMCOUNT:
                    totalValue += data.graph_groups[groupKey].item_count
                if graphData == VAR.GRAPH_DATA_TOTALPRICE:
                    totalValue += data.graph_groups[groupKey].total_price

            if totalValue:
                for groupKey in sorted(data.graph_groups.keys()):

                    if graphData == VAR.GRAPH_DATA_ITEMCOUNT:
                        itemValue = data.graph_groups[groupKey].item_count
                    if graphData == VAR.GRAPH_DATA_TOTALPRICE:
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
            fig.subplots_adjust(left   = self.widthPercentage(canvasWidth, 90),
                                bottom = self.widthPercentage(canvasHeight, 35),
                                right  = (1-self.widthPercentage(canvasWidth, 20)),
                                top    = (1-self.widthPercentage(canvasHeight, 35)))

            ax = fig.add_subplot()
            ax.margins(x=0.005, y=0.05)
            ax.autoscale(True)
            ax.set_title(graphContent)

            wedges, temp = ax.pie(percentages, labels=displayLabels, explode=explode, startangle=90, wedgeprops={'alpha':0.75})

            colors = [w.get_facecolor() for w in wedges]

            canvas.figure = fig
            canvas.mpl_connect("motion_notify_event", onNotify)
            canvas.draw()


    ######################
    # drawStackPlot
    # --------------------
    def drawStackPlot(self, data, canvas, graphContent, graphData):

        if not len(data.graph_groups):
            canvas.figure = Figure()
            canvas.draw()
        else:

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
                        if graphData == VAR.GRAPH_DATA_ITEMCOUNTGROWTH_PURCHASE or graphData == VAR.GRAPH_DATA_ITEMCOUNTGROWTH_ADDED:
                            sum += data.graph_groups[groupKey].sub[date].item_count
                        if graphData == VAR.GRAPH_DATA_TOTALPRICEGROWTH_PURCHASE or graphData == VAR.GRAPH_DATA_TOTALPRICEGROWTH_ADDED:
                            sum += data.graph_groups[groupKey].sub[date].total_price

                    values[groupKey].append(sum)

            # Setup graph
            fig = Figure(figsize=(canvasWidth/100, canvasHeight/100), dpi=100)
            fig.tight_layout()
            fig.subplots_adjust(left   = self.widthPercentage(canvasWidth, 90),
                                bottom = self.widthPercentage(canvasHeight, 40),
                                right  = (1-self.widthPercentage(canvasWidth, 20)),
                                top    = (1-self.widthPercentage(canvasHeight, 35)))

            ax = fig.add_subplot()
            ax.margins(x=0, y=0)
            ax.autoscale(True)
            ax.set_ylabel(graphData)
            ax.set_title(graphContent)

            if self.graph_show_grid.get():
                ax.grid(color="#95A5A6", linestyle="--", linewidth=2, axis="y", alpha=0.7)

            stacks = ax.stackplot(dates, values.values(), labels=values.keys())

            ax.legend(loc='upper left', ncol=5, fontsize=6)

            canvas.figure = fig
            canvas.draw()


    ######################
    # drawLinePlot
    # --------------------
    def drawLinePlot(self, data, canvas, graphContent, graphData):

        if not len(data.graph_groups):
            canvas.figure = Figure()
            canvas.draw()
        else:

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
                        if graphData == VAR.GRAPH_DATA_ITEMCOUNTGROWTH_PURCHASE or graphData == VAR.GRAPH_DATA_ITEMCOUNTGROWTH_ADDED:
                            sum += data.graph_groups[groupKey].sub[date].item_count
                        if graphData == VAR.GRAPH_DATA_TOTALPRICEGROWTH_PURCHASE or graphData == VAR.GRAPH_DATA_TOTALPRICEGROWTH_ADDED:
                            sum += data.graph_groups[groupKey].sub[date].total_price

                    values[groupKey].append(sum)

            # Setup graph
            fig = Figure(figsize=(canvasWidth/100, canvasHeight/100), dpi=100)
            fig.tight_layout()
            fig.subplots_adjust(left   = self.widthPercentage(canvasWidth, 90),
                                bottom = self.widthPercentage(canvasHeight, 40),
                                right  = (1-self.widthPercentage(canvasWidth, 20)),
                                top    = (1-self.widthPercentage(canvasHeight, 35)))

            ax = fig.add_subplot()
            ax.margins(x=0, y=0)
            ax.autoscale(True)
            ax.set_ylabel(graphData)
            ax.set_title(graphContent)

            if self.graph_show_grid.get():
                ax.grid(color="#95A5A6", linestyle="--", linewidth=2, axis="y", alpha=0.7)


            for groupKey in sorted(data.graph_groups.keys()):
                ax.plot(dates, values[groupKey], label=groupKey)

            ax.legend(loc='upper left', ncol=5, fontsize=6)

            canvas.figure = fig
            canvas.draw()
