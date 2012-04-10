"""
Item Browser
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Jan. 2012
"""

def name():
    return "ItemBrowser"
def description():
    return "Browse a multiple selection with auto-zooming to feature and an option to open feature form."
def version():
    return "Version 1.6.0"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.7"
def classFactory(iface):
    from itembrowser import itemBrowser
    return itemBrowser(iface)
