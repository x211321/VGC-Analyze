

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
        if mode == "count":
            if data.graph_groups[groupKey].item_count > maxValue:
                maxValue = data.graph_groups[groupKey].item_count
        if mode == "price":
            if data.graph_groups[groupKey].total_price > maxValue:
                maxValue = data.graph_groups[groupKey].total_price

    print(maxValue)

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
    for groupKey in sorted(data.graph_groups.keys()):

        if mode == "count":
            itemValue = data.graph_groups[groupKey].item_count
        if mode == "price":
            itemValue = data.graph_groups[groupKey].total_price

        barHeight = int(maxBarHeight / maxValue * itemValue)

        endX = startX + barWidth
        endY = startY - barHeight

        # Draw bar
        canvas.create_rectangle(startX, startY, endX, endY, fill="#FF0", outline="black", activefill="#00F")

        # Draw x-axis label
        canvas.create_text(startX+(barWidth/2), startY+paddingXAxis+paddingXAxisLabel, text=groupKey, width=barWidth-2)

        startX = endX