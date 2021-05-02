import lib.Settings as settings
import os
import lib.Var as VAR
from lib.Browser import openBrowser

class Export_HTML(object):

    def __init__(self, itemView):
        self.itemView = itemView


    def export(self):
        rows = []

        for item in self.itemView.get_children():
            # When data is grouped
            if item[0] == "#":
                # Append group
                rows.append({"key": item, "data": self.itemView.item(item)})

                # Iterate child elements
                for child in self.itemView.get_children(item):
                    rows.append({"key": child, "data": self.itemView.item(child)})
            else:
                rows.append({"key": item, "data": self.itemView.item(item)})




        # Get active columns
        temp = settings.get("display", "columns", [])
        activeColumns = []

        if "" in temp:
            temp.remove("")

        for column in VAR.VIEW_COLUMNS:
            if column in temp or len(temp) == 0:
                activeColumns.append(column)


        # Generate HTML
        htmlContent  = '<html>\n'
        htmlContent += '\t<head>\n'
        htmlContent += '\t\t<link rel="stylesheet" href="export.css">\n'
        htmlContent += '\t</head>\n'
        htmlContent += '\t<body>\n'
        htmlContent += '\t\t<table class="table">\n'
        htmlContent += '\t\t\t<tr class="header_row">\n'

        for column in activeColumns:
            htmlContent += '\t\t\t\t<th class="header_cell" id="'+self.getID(column)+'">' + VAR.VIEW_COLUMNS[column]["name"] + '</th>\n'
        htmlContent += '\t\t\t</tr>\n'

        for row in rows:
            if row["key"][0] == "#":
                htmlContent += '\t\t\t<tr class="group_header_row">\n'
                htmlContent += '\t\t\t\t<td class="group_header" colspan="'+str(len(activeColumns))+'">' + row["key"][1:] + ' ' + self.getColumnValue("Title", row) + ' ' + self.getColumnValue("Price", row) + '</td>\n'
                htmlContent += '\t\t\t</tr>\n'
            else:
                htmlContent += '\t\t\t<tr class="item_row">\n'

                for column in activeColumns:
                    htmlContent += '\t\t\t\t<td class="item_cell" id="'+self.getID(column)+'">' + self.getColumnValue(column, row) + '</td>\n'

                htmlContent += '\t\t\t</tr>\n'

        htmlContent += '\t\t</table>\n'
        htmlContent += "\t</body>\n"
        htmlContent += "</html>\n"

        # Save to file
        if not os.path.exists(VAR.EXPORT_PATH):
            os.makedirs(VAR.EXPORT_PATH)

        file = open (VAR.EXPORT_PATH + "collection_export.html", "w", encoding="utf-8")
        file.write(htmlContent)
        file.close()

        # Generate css
        self.generateCss()

        # Open in browser
        openBrowser(os.path.realpath(file.name))

    def getColumnValue(self, columnKey, row):
        index = list(VAR.VIEW_COLUMNS.keys()).index(columnKey) + 2
        return row["data"]["values"][index]

    def getID(self, column):
        return column.lower().replace(" ", "_").replace("(", "").replace(")", "")

    def generateCss(self):
        css = """
                table {
                    margin-left: auto;
                    margin-right: auto;
                    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
                }

                table, th, td {
                    border-bottom: 1px solid #C0C0C0;
                }

                th {
                    text-align:left;
                }

                td, th {
                    padding-right: 2rem;
                }

                #price{
                    text-align: right;
                }

                .group_header {
                    background-color: #F0F0F0;
                    font-weight: 700;
                    font-size: larger;
                }
              """

        if not os.path.exists(VAR.EXPORT_PATH):
            os.path.makedirs(VAR.EXPORT_PATH)

        # Only write css when file doesn't exist yet
        # gives the user the option to place custom css
        if not os.path.exists(VAR.EXPORT_PATH + "export.css"):
            file = open(VAR.EXPORT_PATH + "export.css", "w")
            file.write(css)
            file.close()

