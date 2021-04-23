

######################
# initHotkeys
# --------------------
def initHotkeys(gui):
    gui.bind("<Control-f>", lambda x:gui.pop_itemSearch.show())
    gui.bind("<Control-d>", lambda x:gui.pop_collectionDownload.show())
    gui.bind("<Control-q>", lambda x:gui.destroy())