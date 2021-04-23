

######################
# initHotkeys
# --------------------
def initHotkeys(gui):
    gui.main_window.bind("<Control-f>", lambda x:gui.pop_itemSearch.show())
    gui.main_window.bind("<Control-d>", lambda x:gui.pop_collectionDownload.show())
    gui.main_window.bind("<Control-q>", lambda x:gui.main_window.destroy())