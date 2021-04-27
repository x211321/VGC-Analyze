

######################
# initHotkeys
# --------------------
def initHotkeys(gui):
    gui.bind("<Control-f>", lambda x:gui.pop_itemSearch.show())
    gui.bind("<Control-d>", lambda x:gui.pop_collectionDownload.show())
    gui.bind("<Control-q>", lambda x:gui.destroy())

    gui.bind("<Alt-f>", lambda x:gui.toggleFilterFrame())
    gui.bind("<Alt-i>", lambda x:gui.toggleItemInfoFrame())
    gui.bind("<Alt-g>", lambda x:gui.toggleGraphFrame())
