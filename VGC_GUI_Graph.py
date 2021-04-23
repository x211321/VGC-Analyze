

######################
# drawBarGraph
# --------------------
def drawBarGraph(data, canvas):

    # Get canvas dimensions
    canvasWidth  = canvas.winfo_width()
    canvasHeight = canvas.winfo_height()

    print(canvasWidth)

    # Clear canvas
    canvas.delete("all")

    paddingTop    = 20
    paddingBottom = 20
    paddingLeft   = 20
    paddingRight  = 20

    paddingXAxis  = 10
    paddingYAxis  = 10

    maxValue = 0

    startX    = paddingLeft
    startY    = canvasHeight - paddingBottom

    maxBarWidth  = canvasWidth  - paddingLeft - paddingRight
    maxBarHeight = canvasHeight - paddingTop - paddingBottom

    barWidth  = int(maxBarWidth/len(data.graph_groups))
    barHeight = 0

    # Find maximum value to be displayed in the graph
    for groupKey in data.graph_groups.keys():
        if data.graph_groups[groupKey].item_count > maxValue:
            maxValue = data.graph_groups[groupKey].item_count

    # Draw axes
    # X
    canvas.create_line(startX-paddingYAxis, startY+paddingXAxis, startX+maxBarWidth, startY+paddingXAxis, width="2")
    # Y
    canvas.create_line(startX-paddingYAxis, startY+paddingXAxis, startX-paddingYAxis, startY-maxBarHeight, width="2")

    # Draw graph
    for groupKey in sorted(data.graph_groups.keys()):

        barHeight = int(maxBarHeight / maxValue * data.graph_groups[groupKey].item_count)

        endX = startX + barWidth
        endY = startY - barHeight

        canvas.create_rectangle(startX, startY, endX, endY, fill="#FF0", outline="#F00", activefill="#00F")

        startX = endX